"""Budowanie warunków WHERE dla /search (bez FastAPI - łatwe do testowania)."""
from typing import Optional

from app.sql_helpers import (
    NO_MATCH,
    Mode,
    SearchTerm,
    fuzzy_distance,
    resolve_ids,
    strict_match,
    strict_rank,
    text_match,
)

_SUBSTANCES_OF_PRODUCT = """
    FROM product_substance ps
    JOIN active_substance s ON s.id = ps.substance_id
    WHERE ps.product_id = p.id_sor"""


def text_condition(mode: Mode) -> str:
    """Środek pasuje, gdy zapytanie pasuje do jego nazwy LUB do jednej z substancji czynnych."""
    return (
        f"({text_match(mode, 'p.name')} "
        f"OR EXISTS (SELECT 1 {_SUBSTANCES_OF_PRODUCT} AND {text_match(mode, 's.name')}))"
    )


def text_order(mode: Mode) -> str:
    """ORDER BY ASC dla zapytania tekstowego: dopasowania po nazwie przed dopasowaniami po substancji."""
    if mode == "strict":
        return (
            f"CASE WHEN {strict_match('p.name')} "
            f"THEN {strict_rank('p.name')} ELSE 5 END"
        )
    return (
        f"LEAST(COALESCE({fuzzy_distance('p.name')}, {NO_MATCH}), "
        f"COALESCE((SELECT min({fuzzy_distance('s.name')}) {_SUBSTANCES_OF_PRODUCT}), "
        f"{NO_MATCH}) + 1)"
    )


def has_strict_matches(db, term: SearchTerm) -> bool:
    """
    Czy wpisany tekst pasuje (dokładnie, bez literówek) do jakiegokolwiek środka
    lub substancji w rejestrze - niezależnie od pozostałych filtrów i roli.
    Gdy tak, wyszukiwanie zostaje w trybie strict: puste wyniki oznaczają wtedy
    "filtry za ostre", a nie "literówka".
    """
    row = db.execute(
        f"SELECT EXISTS (SELECT 1 FROM product p WHERE {text_condition('strict')}) AS found",
        term.params,
    ).fetchone()
    return row["found"]


def build_filters(
    db,
    *,
    term: Optional[SearchTerm],
    crops: Optional[list[str]],
    pests: Optional[list[str]],
    product_types: Optional[list[str]],
    role: str,
    mode: Mode = "strict",
) -> tuple[str, dict]:
    """
    Zwraca (warunek_sql, parametry) do wstawienia po "WHERE". Parametry są
    nazwane (%(nazwa)s), więc kolejność fragmentów nie ma znaczenia.

    Zasady:
    - wiele wartości tego samego filtra = LUB, różne filtry = ORAZ,
    - uprawa i agrofag muszą być spełnione przez TO SAMO zastosowanie (WF-04),
    - rola "amateur" zostawia tylko środki dla użytkowników nieprofesjonalnych (WF-05),
    - tekst (term) jest dopasowywany w trybie mode: "strict" albo "fuzzy".
    """
    where = ["TRUE"]
    params: dict = {}

    if role == "amateur":
        where.append("p.for_amateurs")

    if term:
        where.append(text_condition(mode))
        params.update(term.params)

    if product_types:
        where.append(
            """EXISTS (
                SELECT 1 FROM product_product_type ppt
                WHERE ppt.product_id = p.id_sor AND ppt.product_type_id = ANY(%(type_ids)s)
            )"""
        )
        params["type_ids"] = resolve_ids(db, "product_type", product_types)

    usage_conditions = []
    if crops:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_crop uc
                WHERE uc.usage_id = u.id AND uc.crop_id = ANY(%(crop_ids)s)
            )"""
        )
        params["crop_ids"] = resolve_ids(db, "crop", crops)
    if pests:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_pest up
                WHERE up.usage_id = u.id AND up.pest_id = ANY(%(pest_ids)s)
            )"""
        )
        params["pest_ids"] = resolve_ids(db, "pest", pests)
    if usage_conditions:
        where.append(
            "EXISTS (SELECT 1 FROM usage u WHERE u.product_id = p.id_sor AND "
            + " AND ".join(usage_conditions)
            + ")"
        )

    return " AND ".join(where), params