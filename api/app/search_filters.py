"""Budowanie warunków WHERE dla /search (bez FastAPI - łatwe do testowania)."""
from typing import Optional

from app.sql_helpers import fuzzy_match, fuzzy_params, resolve_ids


def build_filters(
    db,
    *,
    q: Optional[str],
    crops: Optional[list[str]],
    pests: Optional[list[str]],
    product_types: Optional[list[str]],
    role: str,
) -> tuple[str, list]:
    """
    Zwraca (warunek_sql, parametry) do wstawienia po "WHERE".

    Zasady:
    - wiele wartości tego samego filtra = LUB, różne filtry = ORAZ,
    - uprawa i agrofag muszą być spełnione przez TO SAMO zastosowanie (WF-04),
    - rola "amateur" zostawia tylko środki dla użytkowników nieprofesjonalnych (WF-05).
    """
    where = ["TRUE"]
    params: list = []

    if role == "amateur":
        where.append("p.for_amateurs")

    if q:
        where.append(
            f"""({fuzzy_match('p.name')}
                OR EXISTS (
                    SELECT 1 FROM product_substance ps
                    JOIN active_substance s ON s.id = ps.substance_id
                    WHERE ps.product_id = p.id_sor AND {fuzzy_match('s.name')}
                ))"""
        )
        params += fuzzy_params(q) + fuzzy_params(q)

    if product_types:
        where.append(
            """EXISTS (
                SELECT 1 FROM product_product_type ppt
                WHERE ppt.product_id = p.id_sor AND ppt.product_type_id = ANY(%s)
            )"""
        )
        params.append(resolve_ids(db, "product_type", product_types))

    usage_conditions = []
    if crops:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_crop uc
                WHERE uc.usage_id = u.id AND uc.crop_id = ANY(%s)
            )"""
        )
        params.append(resolve_ids(db, "crop", crops))
    if pests:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_pest up
                WHERE up.usage_id = u.id AND up.pest_id = ANY(%s)
            )"""
        )
        params.append(resolve_ids(db, "pest", pests))
    if usage_conditions:
        where.append(
            "EXISTS (SELECT 1 FROM usage u WHERE u.product_id = p.id_sor AND "
            + " AND ".join(usage_conditions)
            + ")"
        )

    return " AND ".join(where), params