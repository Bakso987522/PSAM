import argparse
import os

import psycopg
import httpx

from importer import source, parsers

def run() -> None:
    dataset_id = os.environ.get("DANE_GOV_DATASET_ID")
    with httpx.Client(timeout=60) as client:
        published, urls = source.latest_version(client, dataset_id)
        print(f"import: latest version {published}")
        files = source.download_all(client, urls)
    basic = parsers.read_xlsx("basic", files["basic"])
    cards = parsers.read_csv("cards", files["cards"])
    print(f"import: read {len(basic)} products, {len(cards)} cards")

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute(
            "INSERT INTO import_history (published_at, status, message) VALUES (%s, %s, %s)",
            (published, "skipped", "import not implemented yet"),
        )

def main() -> None:
    parser = argparse.ArgumentParser(prog="importer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run", help="download and load newest data from register")
    args = parser.parse_args()

    if args.command == "run":
        run()


if __name__ == "__main__":
    main()
