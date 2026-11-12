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

def dictionary(cur: psycopg.Cursor, table: str, names) -> dict[str, int]:
    cur.executemany(
        f"INSERT INTO {table} (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        [(name,) for name in sorted(names)],
    )
    return {
        parsers.norm(name): row_id
        for name, row_id in cur.execute(f"SELECT name, id FROM {table}")
    }


def load(conn: psycopg.Connection, files: dict[str, bytes]) -> dict:
    basic = parsers.read_xlsx("basic", files["basic"])
    cards = {r["id_sor"]: r for r in parsers.read_csv("cards", files["cards"])}
    substances = [r["Nazwa_SBCZ"] for r in parsers.read_csv("substances", files["substances"])]
    pattern = parsers.composition_pattern(substances)

    rows = []
    type_links = set()
    composition = {}
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
        for name, content, unit in parsers.parse_composition(pattern, p["Zawartosc_SBCZ_prosty"]):
            composition[(p["id_sor"], parsers.norm(name))] = (content, unit)

    with conn.transaction(), conn.cursor() as cur:
        cur.executemany(UPSERT_PRODUCT, rows)

        type_ids = dictionary(cur, "product_type", {name for _, name in type_links})
        cur.execute("DELETE FROM product_product_type")
        cur.executemany(
            "INSERT INTO product_product_type (product_id, product_type_id) VALUES (%s, %s)",
            {(product_id, type_ids[parsers.norm(name)]) for product_id, name in type_links},
        )

        substance_ids = dictionary(cur, "active_substance", substances)
        cur.execute("DELETE FROM product_substance")
        cur.executemany(
            "INSERT INTO product_substance (product_id, substance_id, content, unit)"
            " VALUES (%s, %s, %s, %s)",
            [
                (product_id, substance_ids[key], content, unit)
                for (product_id, key), (content, unit) in composition.items()
            ],
        )

    return {
        "products": len(rows),
        "for_amateurs": sum(r[7] for r in rows),
        "types": len(type_ids),
        "type_links": len(type_links),
        "substances": len(substance_ids),
        "composition": len(composition),
    }