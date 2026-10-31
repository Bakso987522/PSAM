import psycopg
from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="Agrolupa API")


@app.get("/health")
def health():
    try:
        with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        db_ok = True
    except psycopg.Error:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "db": db_ok}
