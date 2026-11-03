import argparse
import os

import psycopg
import httpx

from importer import source, loader

def run() -> None:
    dataset_id = os.environ.get("DANE_GOV_DATASET_ID")
    with httpx.Client(timeout=60) as client:
        published, urls = source.latest_version(client, dataset_id)
        print(f"import: latest version {published}")
        files = source.download_all(client, urls)

    with psycopg.connect(os.environ["DATABASE_URL"], autocommit=True) as conn:
        try:
            stats = loader.load(conn, files)
        except Exception as e:
            conn.execute(
                "INSERT INTO import_history (published_at, status, message) VALUES (%s, %s, %s)",
                (published, "failed", f"{type(e).__name__}: {e}"),
            )
            raise
        conn.execute(
            "INSERT INTO import_history (published_at, status, message) VALUES (%s, %s, %s)",
            (published, "success", str(stats)),
        )
    print(f"import: version {published} loaded: {stats}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="importer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run", help="download and load newest data from register")
    args = parser.parse_args()

    if args.command == "run":
        run()


if __name__ == "__main__":
    main()
