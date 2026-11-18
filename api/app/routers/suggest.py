"""Podpowiedzi przy wpisywaniu. Zwracają zwykłą listę [{id, kind, label}]."""
from fastapi import APIRouter, Depends, Query

from app.db import get_db
from app.sql_helpers import SearchTerm, find_by_name, find_by_name_with_fallback

router = APIRouter(prefix="/suggest", tags=["suggest"])


def suggest_from_table(db, table: str, kind: str, q: str, limit: int = 10):
    term = SearchTerm.from_raw(db, q)
    if not term:
        return []
    rows = find_by_name_with_fallback(db, table, term, limit=limit)
    return [{"id": r["id"], "kind": kind, "label": r["name"]} for r in rows]


@router.get("/names")
def suggest_names(q: str = Query(..., min_length=2), db=Depends(get_db)):
    """Nazwy handlowe środków i substancje czynne."""
    term = SearchTerm.from_raw(db, q)
    if not term:
        return []

    # Tryb (dokładny / z literówkami) wybieramy raz dla obu list razem - inaczej
    # poprawnie wpisana nazwa środka dostawałaby "podobne" substancje czynne.
    products, substances = [], []
    for mode in ("strict", "fuzzy"):
        products = find_by_name(db, "product", term, mode, id_col="id_sor", limit=8)
        substances = find_by_name(db, "active_substance", term, mode, limit=5)
        if products or substances:
            break

    return [
        {"id": p["id"], "kind": "product", "label": p["name"]} for p in products
    ] + [{"id": s["id"], "kind": "substance", "label": s["name"]} for s in substances]


@router.get("/crops")
def suggest_crops(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_from_table(db, "crop", "crop", q)


@router.get("/pests")
def suggest_pests(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_from_table(db, "pest", "pest", q)


@router.get("/product-types")
def suggest_product_types(q: str = Query(..., min_length=1), db=Depends(get_db)):
    return suggest_from_table(db, "product_type", "productType", q)