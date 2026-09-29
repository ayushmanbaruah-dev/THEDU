from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from thedu.core.tokenizer import Tokenizer


@dataclass(frozen=True)
class Posting:
    document_id: str
    term_frequency: int


@dataclass(frozen=True)
class IndexStats:
    document_count: int
    unique_terms: int
    total_tokens: int
    average_document_length: float


class InvertedIndex:
    """Deterministic inverted index (Phase 1).

    postings[term][document_id] = term_frequency
    """

    def __init__(self) -> None:
        self.postings: dict[str, dict[str, int]] = {}
        self.document_lengths: dict[str, int] = {}
        self.total_tokens: int = 0

    def build(self, documents: Iterable[tuple[str, str]], tokenizer: Tokenizer) -> None:
        self.postings.clear()
        self.document_lengths.clear()
        self.total_tokens = 0

        docs = sorted(documents, key=lambda x: x[0])  # deterministic

        for document_id, content in docs:
            tokens = tokenizer.tokenize(content)
            self.document_lengths[document_id] = len(tokens)
            self.total_tokens += len(tokens)

            tf_map: dict[str, int] = {}
            for token in tokens:
                tf_map[token] = tf_map.get(token, 0) + 1

            for term, tf in tf_map.items():
                bucket = self.postings.setdefault(term, {})
                bucket[document_id] = tf

    def stats(self) -> IndexStats:
        doc_count = len(self.document_lengths)
        unique_terms = len(self.postings)
        avgdl = (self.total_tokens / doc_count) if doc_count else 0.0
        return IndexStats(
            document_count=doc_count,
            unique_terms=unique_terms,
            total_tokens=self.total_tokens,
            average_document_length=avgdl,
        )

    def get_postings(self, term: str) -> list[Posting]:
        bucket = self.postings.get(term, {})
        return [Posting(document_id=doc_id, term_frequency=bucket[doc_id]) for doc_id in sorted(bucket)]