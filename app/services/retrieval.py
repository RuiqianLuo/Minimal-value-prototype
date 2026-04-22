from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.services.ingestion import chunk_documents


@dataclass
class RetrievalResult:
    chunk_id: str
    doc_id: str
    title: str
    source_path: str
    text: str
    score: float


class Retriever:
    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._chunks: list[dict] = []
        self._matrix = None
        self.reindex()

    def reindex(self) -> None:
        self._chunks = chunk_documents()
        corpus = [chunk["text"] for chunk in self._chunks] or [""]
        self._matrix = self._vectorizer.fit_transform(corpus)

    def search(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:
        k = top_k or settings.top_k
        query_vector = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self._matrix).flatten()
        ranked_indices = scores.argsort()[::-1][:k]
        results: list[RetrievalResult] = []
        for idx in ranked_indices:
            chunk = self._chunks[int(idx)]
            results.append(
                RetrievalResult(
                    chunk_id=chunk["chunk_id"],
                    doc_id=chunk["doc_id"],
                    title=chunk["title"],
                    source_path=chunk["source_path"],
                    text=chunk["text"],
                    score=float(scores[int(idx)]),
                )
            )
        return results
