from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from thedu.storage.models import Document

from .base import LoadedDocument


class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._text_parts: list[str] = []
        self._in_ignored_tag = 0
        self._capture_title = False
        self._capture_h1 = False
        self.title: str | None = None
        self.h1: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        _ = attrs
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self._in_ignored_tag += 1
            return
        if tag == "title":
            self._capture_title = True
        if tag == "h1":
            self._capture_h1 = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"} and self._in_ignored_tag > 0:
            self._in_ignored_tag -= 1
            return
        if tag == "title":
            self._capture_title = False
        if tag == "h1":
            self._capture_h1 = False

    def handle_data(self, data: str) -> None:
        if self._in_ignored_tag:
            return
        text = data.strip()
        if not text:
            return

        if self._capture_title and self.title is None:
            self.title = text
        if self._capture_h1 and self.h1 is None:
            self.h1 = text

        self._text_parts.append(text)

    def get_text(self) -> str:
        merged = " ".join(self._text_parts)
        return re.sub(r"\s+", " ", merged).strip()


class HtmlLoader:
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in {".html", ".htm"}

    def load(self, path: Path) -> list[LoadedDocument]:
        raw = path.read_text(encoding="utf-8", errors="replace")

        extractor = _HtmlTextExtractor()
        extractor.feed(raw)
        content = extractor.get_text()

        title = extractor.title or extractor.h1 or path.stem
        doc = Document.create(
            title=title,
            content=content,
            source_type="html",
            source_path=path.as_posix(),
        )
        return [LoadedDocument(document=doc)]