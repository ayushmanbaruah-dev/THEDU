import json
from pathlib import Path

from thedu.ingestion.json_loader import JsonLoader


def test_json_loader_supports_list_of_docs(tmp_path: Path) -> None:
    payload = [
        {"title": "Doc A", "content": "machine learning"},
        {"title": "Doc B", "content": "cats and dogs"},
    ]
    path = tmp_path / "docs.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    loader = JsonLoader()
    loaded = loader.load(path)

    assert len(loaded) == 2
    assert loaded[0].document.title == "Doc A"
    assert "machine" in loaded[0].document.content