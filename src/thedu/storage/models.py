from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path


def utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""
    return datetime.now(UTC)


def hash_content(content: str) -> str:
    """Return the SHA-256 hash of UTF-8 document content."""
    return sha256(content.encode("utf-8")).hexdigest()


def stable_document_id(
    *,
    title: str,
    source_type: str,
    content_hash: str,
    source_path: str | None,
) -> str:
    """Create a deterministic ID from document source and content.

    File-backed documents include their source path. Documents without a
    filesystem path use title and content hash as their stable identity.
    """
    if source_path:
        source_key = Path(source_path).as_posix()
        key = f"{source_type}:{source_key}:{content_hash}"
    else:
        key = f"{source_type}:{title}:{content_hash}"

    return sha256(key.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Document:
    """A document stored by THEDU."""

    id: str
    title: str
    content: str
    source_path: str | None
    source_type: str
    content_hash: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        *,
        title: str,
        content: str,
        source_type: str,
        source_path: str | None = None,
        document_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> Document:
        """Create a document with deterministic hash/ID defaults."""
        content_hash = hash_content(content)
        document_id = document_id or stable_document_id(
            title=title,
            source_type=source_type,
            content_hash=content_hash,
            source_path=source_path,
        )

        now = utc_now()
        return cls(
            id=document_id,
            title=title,
            content=content,
            source_path=source_path,
            source_type=source_type,
            content_hash=content_hash,
            created_at=created_at or now,
            updated_at=updated_at or now,
        )