from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from thedu.ingestion.loader import LoaderRegistry, iter_files
from thedu.storage.repositories import DocumentRepository

logger = logging.getLogger(__name__)


@dataclass
class IngestionReport:
    discovered_files: int = 0
    supported_files: int = 0
    processed_files: int = 0
    stored_documents: int = 0
    skipped_unchanged: int = 0
    skipped_unsupported: int = 0
    skipped_malformed: int = 0
    errors: int = 0


class IngestionService:
    """Coordinates discovery + parsing + storage."""

    def __init__(
        self,
        repository: DocumentRepository,
        registry: LoaderRegistry | None = None,
    ) -> None:
        self._repository = repository
        self._registry = registry or LoaderRegistry.default()

    def ingest(self, target: Path) -> IngestionReport:
        report = IngestionReport()

        for file_path in iter_files(target):
            report.discovered_files += 1

            loader = self._registry.get_loader(file_path)
            if loader is None:
                report.skipped_unsupported += 1
                continue

            report.supported_files += 1

            try:
                loaded = loader.load(file_path)
            except Exception:
                report.errors += 1
                logger.exception("Failed to load file: %s", file_path)
                continue

            report.processed_files += 1

            if not loaded:
                report.skipped_malformed += 1
                continue

            for item in loaded:
                doc = item.document
                existing = self._repository.get(doc.id)
                if existing is not None and existing.content_hash == doc.content_hash:
                    report.skipped_unchanged += 1
                    continue

                self._repository.upsert(doc)
                report.stored_documents += 1

        return report