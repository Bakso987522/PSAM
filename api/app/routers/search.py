from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query

from app.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.db import get_db
from app.search_filters import build_filters
from app.sql_helpers import similarity_rank

router = APIRouter(tags=["search"])

PAGE_SQL = """
    SELECT p.id_sor, p.name, p.producer, p.for_amateurs,
           p.use_allowed_until, p.removed_at,
           (SELECT array_agg(pt.name ORDER BY pt.name)
              FROM product_product_type ppt
              JOIN product_type pt ON pt.id = ppt.product_type_id
             WHERE ppt.product_id = p.id_sor) AS product_types,
           (SELECT array_agg(s.name ORDER BY s.name)
              FROM product_substance ps
              JOIN active_substance s ON s.id = ps.substance_id
             WHERE ps.product_id = p.id_sor) AS active_substances
    FROM product p
    WHERE {where}
    ORDER BY {order}
    LIMIT %s OFFSET %s
"""


@router.get("/search")
def search_products(
    q: Optional[str] = None,
    crops: Optional[list[str]] = Query(None),
    pests: Optional[list[str]] = Query(None),
    product_types: Optional[list[str]] = Query(None, alias="productTypes"),
    role: Literal["professional", "amateur"] = "professional",
    page: int = Query(DEFAULT_PAGE, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    # Frontend wysyła tę samą wartość pod nazwą "pageCount" - obie działają.
    page_count: Optional[int] = Query(None, alias="pageCount", ge=1, le=MAX_PAGE_SIZE),
    db=Depends(get_db),
):
    """
    /search?q=Amistar&crops=pszenica&pests=mszyce&productTypes=Fungicyd&role=amateur&page=2&page_size=25
    """
    size = page_count or page_size

    where_sql, params = build_filters(
        db, q=q, crops=crops, pests=pests, product_types=product_types, role=role
    )

    total = db.execute(
        f"SELECT COUNT(*) AS total FROM product p WHERE {where_sql}", params
    ).fetchone()["total"]

    # Stabilna kolejność (id_sor jako ostatni klucz), inaczej strony mogłyby
    # się powtarzać lub gubić środki o tej samej nazwie.
    if q:
        order_sql = f"{similarity_rank('p.name')} DESC, p.name, p.id_sor"
        order_params = [q]
    else:
        order_sql = "p.name, p.id_sor"
        order_params = []

    results = db.execute(
        PAGE_SQL.format(where=where_sql, order=order_sql),
        params + order_params + [size, (page - 1) * size],
    ).fetchall()

    return {
        "filters_applied": {
            "q": q,
            "crops": crops,
            "pests": pests,
            "productTypes": product_types or [],
            "role": role,
        },
        "count": len(results),  # ile środków jest na tej stronie
        "total": total,  # ile środków pasuje łącznie (wszystkie strony)
        "page": page,
        "page_size": size,
        "total_pages": (total + size - 1) // size,
        "results": results,
    }