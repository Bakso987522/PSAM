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
INSERT_USAGE = """
    INSERT INTO usage (id, product_id, group_id, dose, timing, method, combined_use, minor_use)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

def merge_names(dictionary_names: list[str], used: list[list[str]]) -> tuple[list[str], int]:
    names = {parsers.norm(name): name for name in dictionary_names}
    outside = 0
    for parts in used:
        for name in parts:
            if parsers.norm(name) not in names:
                names[parsers.norm(name)] = name
                outside += 1
    return list(names.values()), outside


def load(conn: psycopg.Connection, files: dict[str, bytes]) -> dict:
    basic = parsers.read_xlsx("basic", files["basic"])
    cards = {r["id_sor"]: r for r in parsers.read_csv("cards", files["cards"])}
    substances = [r["Nazwa_SBCZ"] for r in parsers.read_csv("substances", files["substances"])]
    pattern = parsers.composition_pattern(substances)
    usages = parsers.read_xlsx("usages", files["usages"])
    groups = parsers.read_csv("groups", files["groups"])
    crops = [r["uprawa"] for r in parsers.read_csv("crops", files["crops"])]
    pests = [r["agrofag"] for r in parsers.read_csv("pests", files["pests"])]

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

    product_ids = {p["id_sor"] for p in basic}
    crops_with_comma = [name for name in crops if "," in name]
    pests_with_comma = [name for name in pests if "," in name]
    usage_rows = []
    usage_crops = []
    usage_pests = []
    for u in usages:
        if u["id_sor"] not in product_ids:
            raise ValueError(f"usage refers to product {u['id_sor']} missing from the basic register")
        usage_rows.append((
            u["id_sor"],
            u["grupa"],
            u["dawka"],
            u["termin"],
            u["metody_stosowania"],
            u["laczne_stosowanie"],
            u["maloobszarowe"] == 1,
        ))
        usage_crops.append(parsers.split_list(u["uprawa"], crops_with_comma))
        usage_pests.append(parsers.split_list(u["agrofag"], pests_with_comma))

    crop_names, crops_outside = merge_names(crops, usage_crops)
    pest_names, pests_outside = merge_names(pests, usage_pests)    
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
        cur.executemany(
            "INSERT INTO application_group (id, name) VALUES (%s, %s)"
            " ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
            [(int(g["grupa"]), g["nazwa_grupy"]) for g in groups],
        )
        cur.execute("DELETE FROM usage")
        usage_ids = [
            usage_id
            for (usage_id,) in cur.execute(
                "SELECT nextval(pg_get_serial_sequence('usage', 'id')) FROM generate_series(1, %s)",
                (len(usage_rows),),
            )
        ]
        cur.executemany(
            INSERT_USAGE,
            [(usage_id, *row) for usage_id, row in zip(usage_ids, usage_rows)],
        )

        crop_ids = dictionary(cur, "crop", crop_names)
        crop_links = {
            (usage_id, crop_ids[parsers.norm(name)])
            for usage_id, names in zip(usage_ids, usage_crops)
            for name in names
        }
        cur.executemany(
            "INSERT INTO usage_crop (usage_id, crop_id) VALUES (%s, %s)",
            crop_links,
        )

        pest_ids = dictionary(cur, "pest", pest_names)
        pest_links = {
            (usage_id, pest_ids[parsers.norm(name)])
            for usage_id, names in zip(usage_ids, usage_pests)
            for name in names
        }
        cur.executemany(
            "INSERT INTO usage_pest (usage_id, pest_id) VALUES (%s, %s)",
            pest_links,
        )

    return {
        "products": len(rows),
        "for_amateurs": sum(r[7] for r in rows),
        "types": len(type_ids),
        "type_links": len(type_links),
        "substances": len(substance_ids),
        "composition": len(composition),
        "groups": len(groups),
        "usages": len(usage_rows),
        "crops": len(crop_ids),
        "crops_outside_dictionary": crops_outside,
        "crop_links": len(crop_links),
        "pests": len(pest_ids),
        "pests_outside_dictionary": pests_outside,
        "pest_links": len(pest_links),
    }