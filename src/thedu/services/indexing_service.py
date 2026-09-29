from __future__ import annotations

from dataclasses import dataclass

from thedu.config import Settings, ensure_runtime_dirs
from thedu.core.index_artifacts import IndexArtifacts, IndexMetadata
from thedu.core.inverted_index import InvertedIndex
from thedu.core.tokenizer import Tokenizer
from thedu.storage.repositories import DocumentRepository


@dataclass(frozen=True)
class IndexStatus:
    available: bool
    document_count: int | None = None
    unique_terms: int | None = None
    total_tokens: int | None = None
    average_document_length: float | None = None


class IndexingService:
    def __init__(self, settings: Settings, repository: DocumentRepository) -> None:
        ensure_runtime_dirs(settings)
        self._settings = settings
        self._repo = repository
        self._artifacts = IndexArtifacts(settings.index_meta_path, settings.index_data_path)

    def status(self) -> IndexStatus:
        if not self._artifacts.exists():
            return IndexStatus(available=False)

        _, meta = self._artifacts.load()
        return IndexStatus(
            available=True,
            document_count=meta.document_count,
            unique_terms=meta.unique_terms,
            total_tokens=meta.total_tokens,
            average_document_length=meta.average_document_length,
        )

    def rebuild(self) -> IndexMetadata:
        tokenizer = Tokenizer(stopwords_enabled=self._settings.stopwords_enabled)

        docs = self._repo.list_documents(limit=1_000_000, offset=0)
        documents = [(doc.id, doc.content) for doc in docs]

        index = InvertedIndex()
        index.build(documents, tokenizer=tokenizer)

        meta = IndexMetadata.from_stats(
            index.stats(),
            stopwords_enabled=self._settings.stopwords_enabled,
        )
        self._artifacts.save(index, meta)
        return meta