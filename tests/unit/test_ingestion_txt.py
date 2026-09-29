from pathlib import Path

from thedu.ingestion.txt_loader import TxtLoader


def test_txt_loader_loads_document(tmp_path: Path) -> None:
    path = tmp_path / "doc1.txt"
    path.write_text("Hello world", encoding="utf-8")

    loader = TxtLoader()
    loaded = loader.load(path)

    assert len(loaded) == 1
    doc = loaded[0].document
    assert doc.title == "doc1"
    assert "hello world" in doc.content.lower()
    assert doc.source_type == "txt"