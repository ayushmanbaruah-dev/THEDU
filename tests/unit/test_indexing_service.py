from pathlib import Path

from thedu.config import Settings
from thedu.services.indexing_service import IndexingService
from thedu.storage.database import connect, initialize_database
from thedu.storage.models import Document
from thedu.storage.repositories import DocumentRepository


def test_indexing_service_rebuild_creates_artifacts(tmp_path: Path) -> None:
    settings = Settings(
        data_dir=tmp_path / "data",
        sqlite_path=tmp_path / "data" / "documents.sqlite3",
        index_dir=tmp_path / "data" / "index",
        index_meta_path=tmp_path / "data" / "index" / "meta.json",
        index_data_path=tmp_path / "data" / "index" / "index.pkl",
        stopwords_enabled=False,
        log_queries=False,
    )

    conn = connect(settings.sqlite_path)
    initialize_database(conn)
    repo = DocumentRepository(conn)

    repo.upsert(
        Document.create(
            title="A",
            content="machine learning",
            source_type="txt",
            source_path="a.txt",
        )
    )
    repo.upsert(
        Document.create(
            title="B",
            content="cats are animals",
            source_type="txt",
            source_path="b.txt",
        )
    )

    service = IndexingService(settings, repo)
    meta = service.rebuild()

    assert meta.document_count == 2
    assert settings.index_meta_path.is_file()
    assert settings.index_data_path.is_file()

    conn.close()