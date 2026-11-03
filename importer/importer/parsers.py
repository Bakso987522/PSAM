import csv
import io

from openpyxl import load_workbook

REQUIRED_COLUMNS = {
    "basic": {"id_sor", "nazwa", "producent_prosty", "NrZezw", "TerminZezw", "TerminDopSprzedazy",
              "TerminDopuszczenia", "etykieta", "Op", "BazowySor"},
    "cards": {"id_sor", "Zastosowanie"},
}
AMATEUR_USE = {"amatorskie", "amatorskie / profesjonalne"}


def _clean(v):
    if isinstance(v, str):
        v = v.replace("_x000D_", "").strip()
        return v or None
    return v


def _check(key: str, header) -> None:
    missing = REQUIRED_COLUMNS[key] - set(header)
    if missing:
        raise ValueError(f"file '{key}': missing columns {sorted(missing)}")


def read_xlsx(key: str, data: bytes) -> list[dict]:
    rows = load_workbook(io.BytesIO(data), read_only=True).worksheets[0].iter_rows(values_only=True)
    header = next(rows)
    _check(key, header)
    return [dict(zip(header, map(_clean, r))) for r in rows if any(r)]


def read_csv(key: str, data: bytes) -> list[dict]:
    reader = csv.reader(io.StringIO(data.decode("cp1250"), newline=""), delimiter=";")
    header = next(reader)
    _check(key, header)
    return [dict(zip(header, map(_clean, r))) for r in reader if any(r)]
