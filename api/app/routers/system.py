from fastapi import APIRouter, Depends

from app.db import get_db

router = APIRouter(tags=["system"])


@router.get("/health")
def health(db=Depends(get_db)):
    db.execute("SELECT 1")
    return {"status": "ok", "db": True}


@router.get("/data-version")
def data_version(db=Depends(get_db)):
    """Data publikacji wersji danych, z której korzysta system (WF-14)."""
    row = db.execute(
        """
        SELECT published_at
        FROM import_history
        WHERE published_at IS NOT NULL AND status = 'success'
        ORDER BY imported_at DESC
        LIMIT 1
        """
    ).fetchone()
    return {"publishedAt": row["published_at"] if row else None}