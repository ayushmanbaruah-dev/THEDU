from __future__ import annotations

import sqlite3
from datetime import datetime

from .models import Document, utc_now


class DocumentRepository:
    """SQLite-backed CRUD repository for THEDU documents."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, document: Document) -> Document:
        """Insert a document or update an existing document with the same ID."""
        existing = self.get(document.id)
        created_at = existing.created_at if existing is not None else document.created_at
        updated_at = utc_now()

        self._connection.execute(
            """
            INSERT INTO documents (
                id, title, content, source_path, source_type,
                content_hash, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                content = excluded.content,
                source_path = excluded.source_path,
                source_type = excluded.source_type,
                content_hash = excluded.content_hash,
                updated_at = excluded.updated_at
            """,
            (
                document.id,
                document.title,
                document.content,
                document.source_path,
                document.source_type,
                document.content_hash,
                created_at.isoformat(),
                updated_at.isoformat(),
            ),
        )
        self._connection.commit()

        return Document(
            id=document.id,
            title=document.title,
            content=document.content,
            source_path=document.source_path,
            source_type=document.source_type,
            content_hash=document.content_hash,
            created_at=created_at,
            updated_at=updated_at,
        )

    def get(self, document_id: str) -> Document | None:
        """Return a document by ID, or None if it does not exist."""
        row = self._connection.execute(
            """
            SELECT id, title, content, source_path, source_type,
                   content_hash, created_at, updated_at
            FROM documents
            WHERE id = ?
            """,
            (document_id,),
        ).fetchone()

        return _row_to_document(row) if row is not None else None

    def list_documents(self, *, limit: int = 100, offset: int = 0) -> list[Document]:
        """Return documents in deterministic order."""
        rows = self._connection.execute(
            """
            SELECT id, title, content, source_path, source_type,
                   content_hash, created_at, updated_at
            FROM documents
            ORDER BY updated_at DESC, id ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()

        return [_row_to_document(row) for row in rows]

    def count(self) -> int:
        """Return the total number of stored documents."""
        row = self._connection.execute(
            "SELECT COUNT(*) AS document_count FROM documents"
        ).fetchone()
        return int(row["document_count"])

    def delete(self, document_id: str) -> bool:
        """Delete a document. Return True only when a row was deleted."""
        cursor = self._connection.execute(
            "DELETE FROM documents WHERE id = ?",
            (document_id,),
        )
        self._connection.commit()
        return cursor.rowcount > 0


def _row_to_document(row: sqlite3.Row) -> Document:
    return Document(
        id=str(row["id"]),
        title=str(row["title"]),
        content=str(row["content"]),
        source_path=str(row["source_path"]) if row["source_path"] is not None else None,
        source_type=str(row["source_type"]),
        content_hash=str(row["content_hash"]),
        created_at=datetime.fromisoformat(str(row["created_at"])),
        updated_at=datetime.fromisoformat(str(row["updated_at"])),
    )