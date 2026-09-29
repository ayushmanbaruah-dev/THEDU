from pathlib import Path

from thedu.ingestion.csv_loader import CsvLoader


def test_csv_loader_reads_content_column(tmp_path: Path) -> None:
    csv_text = "title,content\nDoc1,hello world\nDoc2,machine learning\n"
    path = tmp_path / "docs.csv"
    path.write_text(csv_text, encoding="utf-8")

    loader = CsvLoader()
    loaded = loader.load(path)

    assert len(loaded) == 2
    assert loaded[1].document.title == "Doc2"
    assert "machine learning" in loaded[1].document.content


def test_csv_loader_skips_rows_without_content(tmp_path: Path) -> None:
    csv_text = "title,content\nDoc1,\nDoc2,ok\n"
    path = tmp_path / "docs.csv"
    path.write_text(csv_text, encoding="utf-8")

    loader = CsvLoader()
    loaded = loader.load(path)

    assert len(loaded) == 1
    assert loaded[0].document.title == "Doc2"