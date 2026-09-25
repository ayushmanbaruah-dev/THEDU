# THEDU
**Search without the noise.**

THEDU is a lightweight, relevance-first local search engine prototype.
Phase 1 focuses on a transparent lexical search pipeline using:
- deterministic tokenization (stopwords optional; OFF by default)
- SQLite storage for documents (coming next)
- inverted index + BM25 ranking (coming next)
- API + CLI + Docker + CI (coming next)

## Dev setup (Windows PowerShell)
```powershell
cd A:\THEDU
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"