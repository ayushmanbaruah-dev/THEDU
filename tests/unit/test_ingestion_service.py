from pathlib import Path

from thedu.ingestion.loader import LoaderRegistry
from thedu.services.ingestion_service import IngestionService
from thedu.storage.database import connect, initialize_database
from thedu.storage.repositories import DocumentRepository


def test_ingestion_service_ingests_directory(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("machine learning with python", encoding="utf-8")
    (tmp_path / "b.html").write_text(
        "<html><title>T</title><body>cats</body></html>",
        encoding="utf-8",
    )
    (tmp_path / "c.json").write_text(
        '[{"title":"J","content":"dogs"}]',
        encoding="utf-8",
    )
    (tmp_path / "d.csv").write_text("content\nhello\n", encoding="utf-8")
    (tmp_path / "ignore.bin").write_bytes(b"\x00\x01\x02")

    db_path = tmp_path / "documents.sqlite3"
    conn = connect(db_path)
    initialize_database(conn)
    repo = DocumentRepository(conn)

    service = IngestionService(repo, registry=LoaderRegistry.default())
    report = service.ingest(tmp_path)

    assert report.discovered_files >= 5
    assert repo.count() == 4
    conn.close()