"""Fragmenty SQL używane w wielu endpointach (wyszukiwanie tekstu).

Wyszukiwanie działa w dwóch krokach, a nie "wszystko naraz":

1. tryb "strict" - wpisany tekst jest zawarty w nazwie (bez względu na wielkość
   liter i polskie znaki). Wyniki są sortowane: nazwa równa zapytaniu,
   nazwa zaczynająca się od zapytania, wyraz zaczynający się od zapytania,
   zapytanie gdziekolwiek w nazwie.
2. tryb "fuzzy" - uruchamiany TYLKO wtedy, gdy tryb "strict" nic nie znalazł.
   Dopuszcza literówki: odległość edycyjna <= FUZZY_MAX_DISTANCE (WF-02),
   liczona dla całego początku nazwy i osobno dla każdego wyrazu nazwy.

Wszystkie fragmenty używają nazwanych parametrów (%(nq)s itd.) - wartości
bierze się z SearchTerm.params.
"""
from dataclasses import dataclass
from typing import Literal, Optional

from app.constants import (
    FUZZY_MAX_DISTANCE,
    FUZZY_TWO_TYPOS_MIN_LENGTH,
    MAX_QUERY_LENGTH,
)

Mode = Literal["strict", "fuzzy"]

# Wartość odległości dla "brak dopasowania" przy sortowaniu (większa niż każda realna).
NO_MATCH = 99


def norm(expr: str) -> str:
    """Wyrażenie SQL: tekst bez polskich znaków i wielkości liter."""
    return f"unaccent(lower({expr}))"


def max_typos(length: int) -> int:
    """Ile pomyłek tolerujemy dla zapytania o danej długości (WF-02: najwyżej 2)."""
    if length < FUZZY_TWO_TYPOS_MIN_LENGTH:
        return min(1, FUZZY_MAX_DISTANCE)
    return FUZZY_MAX_DISTANCE


@dataclass(frozen=True)
class SearchTerm:
    """Wpisany przez użytkownika tekst, już znormalizowany (raz, a nie dla każdego wiersza)."""

    text: str  # małe litery, bez polskich znaków
    max_dist: int

    @classmethod
    def from_raw(cls, db, raw: Optional[str]) -> Optional["SearchTerm"]:
        """Zwraca None, gdy po oczyszczeniu nie zostaje nic do wyszukania."""
        if not raw:
            return None
        cleaned = " ".join(raw.split())[:MAX_QUERY_LENGTH]
        if not cleaned:
            return None
        row = db.execute(
            "SELECT unaccent(lower(%s::text)) AS t", (cleaned,)
        ).fetchone()
        text = " ".join(row["t"].split())
        if not text:
            return None
        return cls(text=text, max_dist=max_typos(len(text)))

    @property
    def params(self) -> dict:
        return {"nq": self.text, "nlen": len(self.text), "maxd": self.max_dist}


# --- tryb strict -----------------------------------------------------------


def strict_match(column: str) -> str:
    """Warunek: kolumna zawiera wpisany tekst. (strpos, a nie LIKE - znaki % i _ nie są specjalne)"""
    return f"strpos({norm(column)}, %(nq)s::text) > 0"


def strict_rank(column: str) -> str:
    """Im mniejsza liczba, tym lepsze dopasowanie. Używać razem ze strict_match()."""
    n = norm(column)
    return (
        f"CASE WHEN {n} = %(nq)s::text THEN 0 "
        f"WHEN starts_with({n}, %(nq)s::text) THEN 1 "
        f"WHEN strpos({n}, ' ' || %(nq)s::text) > 0 THEN 2 "
        f"ELSE 3 END"
    )


# --- tryb fuzzy ------------------------------------------------------------


def fuzzy_distance(column: str) -> str:
    """
    Wyrażenie SQL: najmniejsza odległość edycyjna między zapytaniem a
    (a) początkiem całej nazwy albo (b) początkiem któregokolwiek jej wyrazu.
    Porównujemy z początkiem (tyle znaków, ile ma zapytanie), więc częściowo
    wpisana nazwa z literówką ("amistr") też się znajdzie. NULL = brak wyrazów.
    Wartości powyżej maxd nie są dokładne (levenshtein_less_equal) - wystarczy,
    że są większe od maxd.
    """
    n = norm(column)
    lev = "levenshtein_less_equal({}, %(nq)s::text, %(maxd)s::int)"
    return (
        f"LEAST({lev.format(f'left({n}, %(nlen)s::int)')}, "
        f"(SELECT min({lev.format('left(w.word, %(nlen)s::int)')}) "
        f"FROM regexp_split_to_table({n}, '[^a-z0-9]+') AS w(word) "
        f"WHERE w.word <> ''))"
    )


def fuzzy_match(column: str) -> str:
    """Warunek: kolumna jest podobna do wpisanego tekstu (najwyżej maxd pomyłek)."""
    return f"{fuzzy_distance(column)} <= %(maxd)s::int"


# --- wspólne ---------------------------------------------------------------


def text_match(mode: Mode, column: str) -> str:
    return strict_match(column) if mode == "strict" else fuzzy_match(column)


def text_rank(mode: Mode, column: str) -> str:
    """Wyrażenie do ORDER BY ASC (najlepsze dopasowania pierwsze)."""
    if mode == "strict":
        return strict_rank(column)
    return f"COALESCE({fuzzy_distance(column)}, {NO_MATCH})"


def find_by_name(
    db, table: str, term: SearchTerm, mode: Mode, *, id_col: str = "id", limit: int = 10
) -> list[dict]:
    """Wiersze {id, name} ze słownika (lub z tabeli product) pasujące do zapytania w danym trybie."""
    return db.execute(
        f"""
        SELECT {id_col} AS id, name FROM {table}
        WHERE {text_match(mode, 'name')}
        ORDER BY {text_rank(mode, 'name')}, name
        LIMIT %(limit)s
        """,
        {**term.params, "limit": limit},
    ).fetchall()


def find_by_name_with_fallback(
    db, table: str, term: SearchTerm, *, id_col: str = "id", limit: int = 10
) -> list[dict]:
    """Najpierw dopasowanie dokładne; literówki dopiero, gdy nic nie znaleziono."""
    for mode in ("strict", "fuzzy"):
        rows = find_by_name(db, table, term, mode, id_col=id_col, limit=limit)
        if rows:
            return rows
    return []


def resolve_ids(db, table: str, values: list[str]) -> list[int]:
    """
    Zamienia wpisane nazwy na ID ze słownika (crop, pest, product_type).
    Frontend wysyła też tekst, którego użytkownik nie wybrał z podpowiedzi
    (np. z literówką), więc: najpierw dokładna nazwa (bez polskich znaków
    i wielkości liter), a jeśli jej nie ma - najlepsze dopasowanie
    z wyszukiwania dwustopniowego (zawieranie, potem literówki).
    """
    ids: list[int] = []
    for value in values:
        rows = db.execute(
            f"SELECT id FROM {table} WHERE {norm('name')} = {norm('%s')}", (value,)
        ).fetchall()
        if not rows:
            term = SearchTerm.from_raw(db, value)
            if term:
                rows = find_by_name_with_fallback(db, table, term, limit=1)
        ids += [r["id"] for r in rows]
    return ids