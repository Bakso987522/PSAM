from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db

router = APIRouter(tags=["alternatives"])

ALTERNATIVES_SQL = """
    WITH target AS (
        SELECT array_agg(substance_id ORDER BY substance_id) AS sub_ids,
               array_agg(content ORDER BY substance_id)      AS contents
        FROM product_substance WHERE product_id = %s
    ),
    candidates AS (
        SELECT product_id,
               array_agg(substance_id ORDER BY substance_id) AS sub_ids,
               array_agg(content ORDER BY substance_id)      AS contents
        FROM product_substance
        GROUP BY product_id
    )
    SELECT p.id_sor, p.name, p.packaging, p.for_amateurs, p.use_allowed_until,
           c.contents AS content,
           (c.contents IS NOT DISTINCT FROM t.contents) AS same_content
    FROM candidates c
    CROSS JOIN (SELECT * FROM target WHERE sub_ids IS NOT NULL) t
    JOIN product p ON p.id_sor = c.product_id
    WHERE {where}
    ORDER BY same_content DESC, p.name, p.id_sor
    LIMIT 20
"""


@router.get("/sor/{id_sor}/alternatives")
def get_alternatives(
    id_sor: str,
    crop: Optional[str] = None,
    role: Literal["professional", "amateur"] = "professional",
    db=Depends(get_db),
):
    """Zamienniki o tym samym zestawie substancji czynnych (WF-10)."""
    exists = db.execute(
        "SELECT 1 FROM product WHERE id_sor = %s", (id_sor,)
    ).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="Nie znaleziono środka o podanym ID.")

    where = [
        "p.id_sor <> %s",
        "p.use_allowed_until >= CURRENT_DATE",  # bez środków po terminie stosowania
        "p.removed_at IS NULL",
        "c.sub_ids = t.sub_ids",  # dokładnie ten sam zestaw substancji
    ]
    params: list = [id_sor]

    if role == "amateur":
        where.append("p.for_amateurs")

    if crop:
        where.append(
            """EXISTS (
                SELECT 1 FROM usage u
                JOIN usage_crop uc ON uc.usage_id = u.id
                JOIN crop cr ON cr.id = uc.crop_id
                WHERE u.product_id = p.id_sor AND lower(cr.name) = lower(%s)
            )"""
        )
        params.append(crop)

    # Kolejność placeholderów: najpierw CTE "target" (id_sor), potem WHERE.
    alternatives = db.execute(
        ALTERNATIVES_SQL.format(where=" AND ".join(where)), [id_sor] + params
    ).fetchall()

    return {"alternatives": alternatives}