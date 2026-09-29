from __future__ import annotations

from pathlib import Path

from thedu.storage.models import Document

from .base import LoadedDocument


class TxtLoader:
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".txt"

    def load(self, path: Path) -> list[LoadedDocument]:
        content = path.read_text(encoding="utf-8", errors="replace")
        doc = Document.create(
            title=path.stem,
            content=content,
            source_type="txt",
            source_path=path.as_posix(),
        )
        return [LoadedDocument(document=doc)]