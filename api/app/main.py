from typing import Literal, Optional

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Query
from psycopg.rows import dict_row

from app.config import settings

app = FastAPI(
    title="Agrolupa API",
    description="Backend API wyszukiwarki środków ochrony roślin (ŚOR)",
    version="1.2.0",
)


SIMILARITY_THRESHOLD = 0.3


def get_db():
    conn = psycopg.connect(settings.database_url, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def norm(column: str) -> str:
    """Wyrażenie SQL: kolumna bez polskich znaków i wielkości liter."""
    return f"unaccent(lower({column}))"


# --- Health i wersja danych ---------------------------------------------------

@app.get("/health")
def health(db=Depends(get_db)):
    db.execute("SELECT 1")
    return {"status": "ok", "db": True}


@app.get("/data-version")
def data_version(db=Depends(get_db)):
    """Data publikacji wersji danych (WF-14). Frontend oczekuje {publishedAt}."""
    row = db.execute(
        """
        SELECT published_at
        FROM import_history
        WHERE published_at IS NOT NULL
          AND status NOT ILIKE 'fail%' AND status NOT ILIKE 'error%'
        ORDER BY imported_at DESC
        LIMIT 1
        """
    ).fetchone()
    return {"publishedAt": row["published_at"] if row else None}


# --- Podpowiedzi (frontend oczekuje zwykłej listy, nie obiektu) ----------------

def suggest_dictionary(db, table: str, kind: str, q: str):
    rows = db.execute(
        f"""
        SELECT id, name
        FROM {table}
        WHERE {norm('name')} LIKE '%%' || {norm('%s')} || '%%'
           OR similarity({norm('name')}, {norm('%s')}) > %s
        ORDER BY similarity({norm('name')}, {norm('%s')}) DESC, name
        LIMIT 10
        """,
        (q, q, SIMILARITY_THRESHOLD, q),
    ).fetchall()
    return [{"id": r["id"], "kind": kind, "label": r["name"]} for r in rows]


@app.get("/suggest/names")
def suggest_names(q: str = Query(..., min_length=2), db=Depends(get_db)):
    """Podpowiedzi: nazwy handlowe środków i substancje czynne."""
    products = db.execute(
        f"""
        SELECT id_sor AS id, name
        FROM product
        WHERE {norm('name')} LIKE '%%' || {norm('%s')} || '%%'
           OR similarity({norm('name')}, {norm('%s')}) > %s
        ORDER BY similarity({norm('name')}, {norm('%s')}) DESC, name
        LIMIT 8
        """,
        (q, q, SIMILARITY_THRESHOLD, q),
    ).fetchall()
    substances = suggest_dictionary(db, "active_substance", "substance", q)[:5]
    return [
        {"id": p["id"], "kind": "product", "label": p["name"]} for p in products
    ] + substances


@app.get("/suggest/crops")
def suggest_crops(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_dictionary(db, "crop", "crop", q)


@app.get("/suggest/pests")
def suggest_pests(q: str = Query(..., min_length=2), db=Depends(get_db)):
    return suggest_dictionary(db, "pest", "pest", q)


@app.get("/suggest/product-types")
def suggest_product_types(q: str = Query(..., min_length=1), db=Depends(get_db)):
    return suggest_dictionary(db, "product_type", "productType", q)


# --- Wyszukiwanie ---------------------------------------------------------------

@app.get("/search")
def search_products(
    q: Optional[str] = None,
    crops: Optional[list[str]] = Query(None),
    pests: Optional[list[str]] = Query(None),
    product_types: Optional[list[str]] = Query(None, alias="productTypes"),
    product_types_snake: Optional[list[str]] = Query(None, alias="product_types"),
    role: Literal["professional", "amateur"] = "professional",
    db=Depends(get_db),
):
    """
    /search?q=Amistar&crops=pszenica&crops=rzepak&pests=mszyce&productTypes=Fungicyd&role=amateur
    Wiele wartości tego samego filtra = LUB, różne filtry = ORAZ.
    Wszystkie kryteria upraw/agrofagów muszą być spełnione przez to samo zastosowanie.
    """
    where = ["TRUE"]
    params: list = []
    product_types = (product_types or []) + (product_types_snake or [])

    if role == "amateur":
        where.append("p.for_amateurs")

    if q:
        where.append(
            f"""(
                {norm('p.name')} LIKE '%%' || {norm('%s')} || '%%'
                OR similarity({norm('p.name')}, {norm('%s')}) > %s
                OR EXISTS (
                    SELECT 1 FROM product_substance ps
                    JOIN active_substance s ON s.id = ps.substance_id
                    WHERE ps.product_id = p.id_sor
                      AND ({norm('s.name')} LIKE '%%' || {norm('%s')} || '%%'
                           OR similarity({norm('s.name')}, {norm('%s')}) > %s)
                )
            )"""
        )
        params += [q, q, SIMILARITY_THRESHOLD, q, q, SIMILARITY_THRESHOLD]

    if product_types:
        where.append(
            """EXISTS (
                SELECT 1 FROM product_product_type ppt
                JOIN product_type pt ON pt.id = ppt.product_type_id
                WHERE ppt.product_id = p.id_sor AND lower(pt.name) = ANY(%s)
            )"""
        )
        params.append([t.lower() for t in product_types])

    usage_conditions = []
    if crops:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_crop uc JOIN crop c ON c.id = uc.crop_id
                WHERE uc.usage_id = u.id AND lower(c.name) = ANY(%s)
            )"""
        )
        params.append([c.lower() for c in crops])
    if pests:
        usage_conditions.append(
            """EXISTS (
                SELECT 1 FROM usage_pest up JOIN pest pe ON pe.id = up.pest_id
                WHERE up.usage_id = u.id AND lower(pe.name) = ANY(%s)
            )"""
        )
        params.append([x.lower() for x in pests])
    if usage_conditions:
        where.append(
            "EXISTS (SELECT 1 FROM usage u WHERE u.product_id = p.id_sor AND "
            + " AND ".join(usage_conditions)
            + ")"
        )

    order = "p.name"
    order_params: list = []
    if q:
        order = f"similarity({norm('p.name')}, {norm('%s')}) DESC, p.name"
        order_params = [q]

    sql = f"""
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
        WHERE {' AND '.join(where)}
        ORDER BY {order}
        LIMIT 50
    """
    results = db.execute(sql, params + order_params).fetchall()

    return {
        "filters_applied": {
            "q": q,
            "crops": crops,
            "pests": pests,
            "productTypes": product_types,
            "role": role,
        },
        "count": len(results),
        "results": results,
    }


# --- Karta środka i zamienniki ----------------------------------------------------

@app.get("/sor/{id_sor}")
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


@app.get("/sor/{id_sor}/alternatives")
def get_alternatives(
    id_sor: str,
    crop: Optional[str] = None,
    role: str = "professional",
    db=Depends(get_db),
):
    """Zamienniki o tym samym zestawie substancji czynnych (WF-10)."""
    exists = db.execute(
        "SELECT 1 FROM product_substance WHERE product_id = %s LIMIT 1", (id_sor,)
    ).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="Brak danych o składzie dla podanego środka.")

    where = [
        "p.id_sor <> %s",
        "p.use_allowed_until >= CURRENT_DATE",
        "p.removed_at IS NULL",
        "c.sub_ids = t.sub_ids",
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

    sql = f"""
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
        WHERE {' AND '.join(where)}
        ORDER BY same_content DESC, p.name
        LIMIT 20
    """
    alternatives = db.execute(sql, [id_sor] + params).fetchall()

    return {"alternatives": alternatives}
