from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


@dataclass
class Document:
    doc_id: str
    title: str
    source_path: str
    text: str


def _normalize_text(raw: str) -> str:
    return "\n".join(line.strip() for line in raw.splitlines() if line.strip())


def load_documents(docs_dir: Path | None = None) -> list[Document]:
    docs_path = docs_dir or settings.docs_dir
    documents: list[Document] = []
    for path in sorted(docs_path.glob("*.md")):
        text = _normalize_text(path.read_text(encoding="utf-8"))
        title = path.stem.replace("_", " ").title()
        documents.append(
            Document(
                doc_id=path.stem,
                title=title,
                source_path=str(path),
                text=text,
            )
        )
    return documents


def chunk_documents(chunk_size: int | None = None, overlap: int | None = None) -> list[dict]:
    size = chunk_size or settings.chunk_size
    stride = size - (overlap or settings.chunk_overlap)
    chunks: list[dict] = []
    for doc in load_documents():
        start = 0
        index = 0
        while start < len(doc.text):
            end = min(len(doc.text), start + size)
            chunk_text = doc.text[start:end]
            chunks.append(
                {
                    "chunk_id": f"{doc.doc_id}-chunk-{index}",
                    "doc_id": doc.doc_id,
                    "title": doc.title,
                    "source_path": doc.source_path,
                    "text": chunk_text,
                    "token_estimate": max(1, len(chunk_text) // 4),
                }
            )
            if end >= len(doc.text):
                break
            start += max(1, stride)
            index += 1
    return chunks
