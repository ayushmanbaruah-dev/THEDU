from thedu.core.tokenizer import Tokenizer, tokenize


def test_tokenizer_handles_punctuation_and_case() -> None:
    result = tokenize("Python, Python! Search-engine.")
    assert result == ["python", "python", "search", "engine"]


def test_tokenizer_returns_empty_list_for_empty_input() -> None:
    assert tokenize("") == []


def test_tokenizer_keeps_numbers_and_unicode_words() -> None:
    tokens = tokenize("Café search 123")
    assert tokens == ["café", "search", "123"]


def test_stopwords_are_off_by_default() -> None:
    assert tokenize("the cat and the dog") == ["the", "cat", "and", "the", "dog"]


def test_stopwords_can_be_enabled_explicitly() -> None:
    tokenizer = Tokenizer(stopwords_enabled=True)
    assert tokenizer.tokenize("the cat and the dog") == ["cat", "dog"]