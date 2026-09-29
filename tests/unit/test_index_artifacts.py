from pathlib import Path

from thedu.core.index_artifacts import IndexArtifacts, IndexMetadata
from thedu.core.inverted_index import InvertedIndex
from thedu.core.tokenizer import Tokenizer


def test_index_artifacts_roundtrip(tmp_path: Path) -> None:
    idx = InvertedIndex()
    idx.build([("d1", "hello world")], tokenizer=Tokenizer())
    meta = IndexMetadata.from_stats(idx.stats(), stopwords_enabled=False)

    artifacts = IndexArtifacts(tmp_path / "meta.json", tmp_path / "index.pkl")
    artifacts.save(idx, meta)

    loaded_idx, loaded_meta = artifacts.load()
    assert loaded_meta.document_count == 1
    assert "hello" in loaded_idx.postings