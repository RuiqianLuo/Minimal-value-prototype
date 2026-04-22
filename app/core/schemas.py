from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Citation(BaseModel):
    doc_id: str
    title: str
    chunk_id: str
    snippet: str
    score: float


class AskRequest(BaseModel):
    question: str = Field(min_length=3)


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieval_debug: list[dict[str, Any]]
    mode: str
    latency_ms: int


class ChunkRecord(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    source_path: str
    text: str
    token_estimate: int
