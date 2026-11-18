import argparse
import os

import psycopg
import httpx

from importer import labels, source, loader, parsers

def last_version(conn: psycopg.Connection):
    row = conn.execute(
        "SELECT max(published_at)::date FROM import_history WHERE status = 'success'"
    ).fetchone()
    return row[0]
 
def log(conn: psycopg.Connection, published, status: str, message: str) -> None:
    conn.execute(
        "INSERT INTO import_history (published_at, status, message) VALUES (%s, %s, %s)",
        (published, status, message),
    ) 


def fetch_labels(
    client: httpx.Client,
    conn: psycopg.Connection,
    files: dict[str, bytes],
) -> dict[str, str]:
    pages = {
        p["etykieta"]
        for p in parsers.read_xlsx("basic", files["basic"])
        if p["etykieta"] and not p["etykieta"].lower().endswith(".pdf")
    }

    try:
        return labels.label_index(client, pages)
    except httpx.HTTPError as e:
        print(
            f"import: label pages unavailable ({e}), "
            "keeping labels from the previous import"
        )
        return {
            parsers.norm(name): url
            for name, url in conn.execute(
                "SELECT name, label_url FROM product WHERE label_matched"
            )
        }
    

def run(force: bool) -> None:
    dataset_id = os.environ["DANE_GOV_DATASET_ID"]
    with (
        psycopg.connect(os.environ["DATABASE_URL"], autocommit=True) as conn,
        httpx.Client(timeout=60) as client,
    ):
        published = None
        try:
            published, urls = source.latest_version(client, dataset_id)
            print(f"import: latest version {published}")
            if not force and published == last_version(conn):
                log(conn, published, "unchanged", "version already loaded")
                print(f"import: version {published} already loaded, skipping (use --force to reload)")
                return
            files = source.download_all(client, urls)
            label_urls = fetch_labels(client, conn, files)
            stats = loader.load(conn, files, published, label_urls, force)
        except Exception as e:
            log(conn, published, "failed", f"{type(e).__name__}: {e}")
            raise
        log(conn, published, "success", str(stats))
    print(f"import: version {published} loaded: {stats}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="importer")
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run", help="download and load newest data from register")
    run_parser.add_argument("--force", action="store_true", help="load even if this version is already loaded or smaller than current data")
    args = parser.parse_args()

    if args.command == "run":
        run(args.force)


if __name__ == "__main__":
    main()
