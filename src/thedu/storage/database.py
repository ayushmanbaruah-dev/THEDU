from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_path TEXT,
    source_type TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_documents_source_path
ON documents(source_path);

CREATE INDEX IF NOT EXISTS idx_documents_updated_at
ON documents(updated_at);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection configured for row-name access."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    """Create the Phase 1 database schema if it does not already exist."""
    connection.executescript(SCHEMA)
    connection.commit()