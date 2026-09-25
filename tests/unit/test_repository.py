from pathlib import Path

from thedu.storage.database import connect, initialize_database
from thedu.storage.models import Document
from thedu.storage.repositories import DocumentRepository


def test_document_repository_crud(tmp_path: Path) -> None:
    connection = connect(tmp_path / "documents.sqlite3")
    initialize_database(connection)
    repository = DocumentRepository(connection)

    document = Document.create(
        title="Introduction to Search",
        content="Search engines retrieve documents.",
        source_type="txt",
        source_path="sample_data/search.txt",
    )

    stored = repository.upsert(document)

    fetched = repository.get(stored.id)
    assert fetched is not None
    assert fetched.id == stored.id
    assert fetched.title == "Introduction to Search"
    assert fetched.content_hash == stored.content_hash

    assert repository.count() == 1
    assert len(repository.list_documents()) == 1

    assert repository.delete(stored.id) is True
    assert repository.get(stored.id) is None
    assert repository.count() == 0

    connection.close()


def test_document_ids_are_deterministic() -> None:
    first = Document.create(
        title="Document",
        content="same content",
        source_type="txt",
        source_path="docs/example.txt",
    )
    second = Document.create(
        title="Document",
        content="same content",
        source_type="txt",
        source_path="docs/example.txt",
    )

    assert first.id == second.id
    assert first.content_hash == second.content_hash