from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from thedu import __version__
from thedu.core.inverted_index import IndexStats, InvertedIndex

INDEX_VERSION = 1


@dataclass(frozen=True)
class IndexMetadata:
    index_version: int
    created_at: str
    thedu_version: str
    document_count: int
    unique_terms: int
    total_tokens: int
    average_document_length: float
    stopwords_enabled: bool

    @classmethod
    def from_stats(cls, stats: IndexStats, *, stopwords_enabled: bool) -> IndexMetadata:
        return cls(
            index_version=INDEX_VERSION,
            created_at=datetime.now(UTC).isoformat(),
            thedu_version=__version__,
            document_count=stats.document_count,
            unique_terms=stats.unique_terms,
            total_tokens=stats.total_tokens,
            average_document_length=stats.average_document_length,
            stopwords_enabled=stopwords_enabled,
        )


class IndexArtifacts:
    """Persistence layer for the inverted index.

    SECURITY: index.pkl is pickle. Load only from trusted local artifacts.
    """

    def __init__(self, meta_path: Path, data_path: Path) -> None:
        self.meta_path = meta_path
        self.data_path = data_path

    def exists(self) -> bool:
        return self.meta_path.is_file() and self.data_path.is_file()

    def save(self, index: InvertedIndex, metadata: IndexMetadata) -> None:
        self.meta_path.parent.mkdir(parents=True, exist_ok=True)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)

        self.meta_path.write_text(json.dumps(asdict(metadata), indent=2), encoding="utf-8")
        self.data_path.write_bytes(pickle.dumps(index))

    def load(self) -> tuple[InvertedIndex, IndexMetadata]:
        meta_raw = json.loads(self.meta_path.read_text(encoding="utf-8"))
        if int(meta_raw.get("index_version", -1)) != INDEX_VERSION:
            raise ValueError("Incompatible index metadata version.")
        metadata = IndexMetadata(**meta_raw)

        index = pickle.loads(self.data_path.read_bytes())
        if not isinstance(index, InvertedIndex):
            raise TypeError("Index artifact is not an InvertedIndex.")
        return index, metadata