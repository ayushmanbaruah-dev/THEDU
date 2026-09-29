from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """THEDU runtime configuration (Phase 1 local prototype)."""

    model_config = SettingsConfigDict(env_prefix="THEDU_", env_file=".env")

    # Runtime persistence location (not committed to git)
    data_dir: Path = Path("data")
    sqlite_path: Path = Path("data/documents.sqlite3")

    index_dir: Path = Path("data/index")
    index_meta_path: Path = Path("data/index/meta.json")
    index_data_path: Path = Path("data/index/index.pkl")

    # Tokenization (OFF by default per your spec)
    stopwords_enabled: bool = False

    # Logging
    log_queries: bool = False


def ensure_runtime_dirs(settings: Settings) -> None:
    """Create required runtime directories."""
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    settings.index_dir.mkdir(parents=True, exist_ok=True)