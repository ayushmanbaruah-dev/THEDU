from __future__ import annotations

import unicodedata


def normalize_text(text: str) -> str:
    """Deterministically normalize text.

    - Unicode normalization: NFKC
    - Lowercase
    """
    normalized = unicodedata.normalize("NFKC", text)
    return normalized.lower()