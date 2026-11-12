"""Małe fragmenty SQL używane w wielu endpointach (wyszukiwanie z literówkami)."""
from app.constants import SIMILARITY_THRESHOLD


def norm(expr: str) -> str:
    """Wyrażenie SQL: tekst bez polskich znaków i wielkości liter."""
    return f"unaccent(lower({expr}))"


def fuzzy_match(column: str) -> str:
    """
    Warunek WHERE: kolumna zawiera wpisany tekst albo jest do niego podobna.
    Potrzebuje 3 parametrów - patrz fuzzy_params().
    """
    return (
        f"({norm(column)} LIKE '%%' || {norm('%s')} || '%%' "
        f"OR similarity({norm(column)}, {norm('%s')}) > %s)"
    )


def fuzzy_params(q: str) -> list:
    return [q, q, SIMILARITY_THRESHOLD]


def similarity_rank(column: str) -> str:
    """Wyrażenie do ORDER BY (najbardziej podobne pierwsze). Potrzebuje 1 parametru: q."""
    return f"similarity({norm(column)}, {norm('%s')})"


def resolve_ids(db, table: str, values: list[str]) -> list[int]:
    """
    Zamienia wpisane nazwy na ID ze słownika (crop, pest, product_type).
    Frontend wysyła też tekst, którego użytkownik nie wybrał z podpowiedzi
    (np. z literówką), więc: najpierw dokładne dopasowanie (bez polskich znaków
    i wielkości liter), a jeśli go nie ma - najbardziej podobna nazwa.
    """
    ids: list[int] = []
    for value in values:
        rows = db.execute(
            f"SELECT id FROM {table} WHERE {norm('name')} = {norm('%s')}", (value,)
        ).fetchall()
        if not rows:
            rows = db.execute(
                f"""
                SELECT id FROM {table}
                WHERE similarity({norm('name')}, {norm('%s')}) > %s
                ORDER BY similarity({norm('name')}, {norm('%s')}) DESC
                LIMIT 1
                """,
                (value, SIMILARITY_THRESHOLD, value),
            ).fetchall()
        ids += [r["id"] for r in rows]
    return ids