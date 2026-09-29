from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from thedu.storage.models import Document

from .base import LoadedDocument


@dataclass(frozen=True)
class CsvMapping:
    title_column: str | None = "title"
    content_column: str = "content"


class CsvLoader:
    def __init__(self, mapping: CsvMapping | None = None) -> None:
        self.mapping = mapping or CsvMapping()

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".csv"

    def load(self, path: Path) -> list[LoadedDocument]:
        results: list[LoadedDocument] = []

        with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            reader = csv.DictReader(handle)
            for idx, row in enumerate(reader):
                content = (row.get(self.mapping.content_column) or "").strip()
                if not content:
                    continue

                title = ""
                if self.mapping.title_column:
                    title = (row.get(self.mapping.title_column) or "").strip()
                if not title:
                    title = f"{path.stem} [row {idx}]"

                source_path = f"{path.as_posix()}#row={idx}"
                doc = Document.create(
                    title=title,
                    content=content,
                    source_type="csv",
                    source_path=source_path,
                )
                results.append(LoadedDocument(document=doc))

        return results