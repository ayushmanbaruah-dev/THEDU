from thedu.core.inverted_index import InvertedIndex
from thedu.core.tokenizer import Tokenizer


def test_inverted_index_builds_postings_and_lengths() -> None:
    docs = [
        ("d1", "python python search"),
        ("d2", "search engines"),
    ]
    idx = InvertedIndex()
    idx.build(docs, tokenizer=Tokenizer())

    postings = idx.get_postings("python")
    assert len(postings) == 1
    assert postings[0].document_id == "d1"
    assert postings[0].term_frequency == 2

    assert idx.document_lengths["d1"] == 3
    assert idx.document_lengths["d2"] == 2

    stats = idx.stats()
    assert stats.document_count == 2
    assert stats.total_tokens == 5