import psycopg

from importer import parsers

UPSERT_PRODUCT = """
    INSERT INTO product (id_sor, name, producer, permit_number, permit_valid_until,
        sale_allowed_until, use_allowed_until, for_amateurs, packaging, label_url, base_product_name)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_sor) DO UPDATE SET
        name = EXCLUDED.name, producer = EXCLUDED.producer,
        permit_number = EXCLUDED.permit_number,
        permit_valid_until = EXCLUDED.permit_valid_until,
        sale_allowed_until = EXCLUDED.sale_allowed_until,
        use_allowed_until = EXCLUDED.use_allowed_until,
        for_amateurs = EXCLUDED.for_amateurs, packaging = EXCLUDED.packaging,
        label_url = EXCLUDED.label_url, base_product_name = EXCLUDED.base_product_name
"""


def load(conn: psycopg.Connection, files: dict[str, bytes]) -> dict:
    basic = parsers.read_xlsx("basic", files["basic"])
    cards = {r["id_sor"]: r for r in parsers.read_csv("cards", files["cards"])}

    rows = []
    type_links = set()
    for p in basic:
        card = cards.get(p["id_sor"])
        if card is None:
            raise ValueError(f"product {p['id_sor']} ({p['nazwa']}) is missing from the cards register")
        rows.append((p["id_sor"], p["nazwa"], p["producent_prosty"], p["NrZezw"], p["TerminZezw"],
                     p["TerminDopSprzedazy"], p["TerminDopuszczenia"],
                     card["Zastosowanie"] in parsers.AMATEUR_USE, p["Op"], p["etykieta"],
                     p["BazowySor"]))
        # Rodzaj can be multiple: "Akarycyd, Insektycyd"
        for name in (p["Rodzaj"] or "").split(","):
            if name.strip():
                type_links.add((p["id_sor"], name.strip()))

    with conn.transaction(), conn.cursor() as cur:
        cur.executemany(UPSERT_PRODUCT, rows)

        cur.executemany("INSERT INTO product_type (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                        [(name,) for name in sorted({name for _, name in type_links})])
        type_ids = dict(cur.execute("SELECT name, id FROM product_type").fetchall())
        cur.execute("DELETE FROM product_product_type")
        cur.executemany("INSERT INTO product_product_type (product_id, product_type_id) VALUES (%s, %s)",
                        [(product_id, type_ids[name]) for product_id, name in type_links])

    return {"products": len(rows), "for_amateurs": sum(r[7] for r in rows),
            "types": len(type_ids), "type_links": len(type_links)}
