import csv
import io
import re

from openpyxl import load_workbook
from decimal import Decimal

REQUIRED_COLUMNS = {
    "basic": {"id_sor", "nazwa", "producent_prosty", "NrZezw", "TerminZezw", "TerminDopSprzedazy",
              "TerminDopuszczenia", "etykieta", "Op", "BazowySor", "Rodzaj", "Zawartosc_SBCZ_prosty"},
    "cards": {"id_sor", "Zastosowanie"},
    "substances": {"Nazwa_SBCZ"},
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

def norm(name: str) -> str:
    return " ".join(name.lower().split())

def composition_pattern(substances: list[str]) -> re.Pattern:
    names = "|".join(re.escape(s) for s in sorted(substances, key=len, reverse=True))    
    return re.compile(
        rf"({names})(?:\s+-\s+(\d+(?:,\d+)?)\s*(g|%))?\s*(?:,\s*|$)",
        re.IGNORECASE, 
    ) 

def parse_composition(pattern: re.Pattern, text: str | None) -> list[tuple[str, Decimal | None, str | None]]:
    text = text or ""
    parts = []
    pos = 0
    while pos < len(text):
        m = pattern.match(text, pos)
        if m is None:
            raise ValueError(f"unknown composition {text!r} at position {pos}")
        content = Decimal(m[2].replace(",", ".")) if m[2] else None
        parts.append((m[1], content, m[3]))
        pos = m.end()
    return parts    