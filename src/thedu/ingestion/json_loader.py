from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from thedu.storage.models import Document

from .base import LoadedDocument


class JsonLoader:
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".json"

    def load(self, path: Path) -> list[LoadedDocument]:
        raw = path.read_text(encoding="utf-8", errors="replace")
        payload: Any = json.loads(raw)

        items: list[dict[str, Any]]
        if isinstance(payload, dict):
            items = [payload]
        elif isinstance(payload, list):
            items = [x for x in payload if isinstance(x, dict)]
        else:
            items = []

        results: list[LoadedDocument] = []
        for idx, item in enumerate(items):
            content = str(item.get("content", "")).strip()
            if not content:
                continue

            title = str(item.get("title", "")).strip() or f"{path.stem} [{idx}]"
            source_path = f"{path.as_posix()}#item={idx}"

            doc = Document.create(
                title=title,
                content=content,
                source_type="json",
                source_path=source_path,
            )
            results.append(LoadedDocument(document=doc))

        return results