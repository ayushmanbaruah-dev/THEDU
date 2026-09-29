from pathlib import Path

from thedu.ingestion.html_loader import HtmlLoader


def test_html_loader_extracts_title_and_text(tmp_path: Path) -> None:
    html = """
    <html>
      <head><title>Test Page</title><style>body{}</style></head>
      <body>
        <script>evil()</script>
        <h1>Main Heading</h1>
        <p>Hello <b>world</b></p>
      </body>
    </html>
    """
    path = tmp_path / "page.html"
    path.write_text(html, encoding="utf-8")

    loader = HtmlLoader()
    loaded = loader.load(path)

    assert len(loaded) == 1
    doc = loaded[0].document
    assert doc.title == "Test Page"
    assert "evil" not in doc.content.lower()
    assert "hello world" in doc.content.lower()