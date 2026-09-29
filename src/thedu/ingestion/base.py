from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from thedu.storage.models import Document


@dataclass(frozen=True)
class LoadedDocument:
    """A document produced by a loader before storage."""
    document: Document


class DocumentLoader(Protocol):
    """Reads a file and returns one or more loaded documents."""

    def supports(self, path: Path) -> bool: ...

    def load(self, path: Path) -> list[LoadedDocument]: ...