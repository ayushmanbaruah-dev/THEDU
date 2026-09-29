from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

from .base import DocumentLoader
from .csv_loader import CsvLoader
from .html_loader import HtmlLoader
from .json_loader import JsonLoader
from .txt_loader import TxtLoader

SUPPORTED_SUFFIXES = {".txt", ".html", ".htm", ".json", ".csv"}


def iter_files(target: Path) -> Iterator[Path]:
    """Yield files from a file or directory, deterministically."""
    if target.is_file():
        yield target
        return

    for path in sorted(target.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_file():
            yield path


class LoaderRegistry:
    def __init__(self, loaders: Iterable[DocumentLoader]) -> None:
        self._loaders = list(loaders)

    @classmethod
    def default(cls) -> LoaderRegistry:
        return cls([TxtLoader(), HtmlLoader(), JsonLoader(), CsvLoader()])

    def get_loader(self, path: Path) -> DocumentLoader | None:
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            return None
        for loader in self._loaders:
            if loader.supports(path):
                return loader
        return None