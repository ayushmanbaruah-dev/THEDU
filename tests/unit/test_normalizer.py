from thedu.core.normalizer import normalize_text


def test_normalizer_lowercases_text() -> None:
    assert normalize_text("PyThOn SEARCH") == "python search"


def test_normalizer_applies_unicode_nfkc() -> None:
    assert normalize_text("Ｆｕｌｌ　Ｗｉｄｔｈ") == "full width"