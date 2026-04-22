from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "Acme Knowledge Assistant"
    data_dir: Path = BASE_DIR / "data"
    docs_dir: Path = BASE_DIR / "data" / "docs"
    eval_file: Path = BASE_DIR / "data" / "eval" / "questions.json"
    logs_dir: Path = BASE_DIR / "logs"
    llm_provider: str = os.getenv("LLM_PROVIDER", "extractive").lower()
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    gemini_fallback_model: str = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-1.5-flash")
    top_k: int = int(os.getenv("TOP_K", "4"))
    min_retrieval_score: float = float(os.getenv("MIN_RETRIEVAL_SCORE", "0.08"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "550"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))


settings = Settings()
