import argparse
import os

import psycopg


def run() -> None:
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute(
            "INSERT INTO import_history (status, message) VALUES (%s, %s)",
            ("skipped", "import not implemented yet"),
        )
    print("import: not implemented yet")


def main() -> None:
    parser = argparse.ArgumentParser(prog="importer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run", help="pobierz i wczytaj najnowsze dane rejestru")
    args = parser.parse_args()

    if args.command == "run":
        run()


if __name__ == "__main__":
    main()
