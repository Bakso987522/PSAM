"""Podpowiedzi przy wpisywaniu. Zwracają zwykłą listę [{id, kind, label}]."""
from fastapi import APIRouter, Depends, Query

from app.db import get_db
from app.sql_helpers import fuzzy_match, fuzzy_params, similarity_rank

router = APIRouter(prefix="/suggest", tags=["suggest"])


def suggest_from_table(db, table: str, kind: str, q: str, limit: int = 10):
    rows = db.execute(
        f"""
        SELECT id, name FROM {table}
        WHERE {fuzzy_match('name')}
        ORDER BY {similarity_rank('name')} DESC, name
        LIMIT {int(limit)}
        """,
        fuzzy_params(q) + [q],
    ).fetchall()
    return [{"id": r["id"], "kind": kind, "label": r["name"]} for r in rows]


@router.get("/names")
def suggest_names(q: str = Query(..., min_length=2), db=Depends(get_db)):
    """Nazwy handlowe środków i substancje czynne."""
    products = db.execute(
        f"""
        SELECT id_sor AS id, name FROM product
        WHERE {fuzzy_match('name')}
        ORDER BY {similarity_rank('name')} DESC, name
        LIMIT 8
        """,
        fuzzy_params(q) + [q],
    ).fetchall()
    substances = suggest_from_table(db, "active_substance", "substance", q, limit=5)
    return [
        {"id": p["id"], "kind": "product", "label": p["name"]} for p in products
    ] + substances


@router.get("/crops")
def suggest_crops(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_from_table(db, "crop", "crop", q)


@router.get("/pests")
def suggest_pests(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_from_table(db, "pest", "pest", q)


@router.get("/product-types")
def suggest_product_types(q: str = Query(..., min_length=1), db=Depends(get_db)):
    return suggest_from_table(db, "product_type", "productType", q)