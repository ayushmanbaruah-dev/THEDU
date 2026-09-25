from __future__ import annotations

import re
from dataclasses import dataclass

from .normalizer import normalize_text

# Unicode-aware tokens (letters/digits), excluding underscore.
_TOKEN_RE = re.compile(r"[^\W_]+", flags=re.UNICODE)

_DEFAULT_STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "to",
        "of",
        "in",
        "on",
        "for",
        "with",
        "is",
        "are",
    }
)


@dataclass(frozen=True)
class Tokenizer:
    stopwords_enabled: bool = False
    stopwords: frozenset[str] = _DEFAULT_STOPWORDS

    def tokenize(self, text: str) -> list[str]:
        normalized = normalize_text(text or "")
        tokens = _TOKEN_RE.findall(normalized)

        if not self.stopwords_enabled:
            return tokens

        return [t for t in tokens if t not in self.stopwords]


def tokenize(text: str, *, stopwords_enabled: bool = False) -> list[str]:
    return Tokenizer(stopwords_enabled=stopwords_enabled).tokenize(text)