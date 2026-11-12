import psycopg
from psycopg.rows import dict_row

from app.config import settings


def get_db():
    """Połączenie z bazą na czas jednego żądania (wstrzykiwane przez Depends)."""
    conn = psycopg.connect(settings.database_url, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()