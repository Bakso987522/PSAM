from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db

router = APIRouter(tags=["products"])


@router.get("/sor/{id_sor}")
def get_product_card(id_sor: str, db=Depends(get_db)):
    """Karta środka (WF-06, WF-07). id_sor to tekstowy GUID z rejestru."""
    product = db.execute(
        "SELECT * FROM product WHERE id_sor = %s", (id_sor,)
    ).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Nie znaleziono środka o podanym ID.")

    substances = db.execute(
        """
        SELECT s.name, ps.content, ps.unit
        FROM product_substance ps
        JOIN active_substance s ON s.id = ps.substance_id
        WHERE ps.product_id = %s
        ORDER BY s.name
        """,
        (id_sor,),
    ).fetchall()

    product_types = db.execute(
        """
        SELECT pt.name
        FROM product_product_type ppt
        JOIN product_type pt ON pt.id = ppt.product_type_id
        WHERE ppt.product_id = %s
        ORDER BY pt.name
        """,
        (id_sor,),
    ).fetchall()

    usages = db.execute(
        """
        SELECT u.id, u.dose, u.timing, u.method, u.combined_use, u.minor_use,
               u.pre_harvest_days, u.pre_harvest_source,
               (SELECT array_agg(c.name ORDER BY c.name)
                  FROM usage_crop uc JOIN crop c ON c.id = uc.crop_id
                 WHERE uc.usage_id = u.id) AS crops,
               (SELECT array_agg(pe.name ORDER BY pe.name)
                  FROM usage_pest up JOIN pest pe ON pe.id = up.pest_id
                 WHERE up.usage_id = u.id) AS pests
        FROM usage u
        WHERE u.product_id = %s
        ORDER BY u.id
        """,
        (id_sor,),
    ).fetchall()

    return {
        "product": product,
        "product_types": [t["name"] for t in product_types],
        "active_substances": substances,
        "usages": usages,
    }