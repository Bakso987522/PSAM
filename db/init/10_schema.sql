CREATE TABLE IF NOT EXISTS import_history (
    id           SERIAL PRIMARY KEY,
    published_at TIMESTAMPTZ,
    imported_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    status       TEXT NOT NULL,
    message      TEXT
);
