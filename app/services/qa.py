from __future__ import annotations

import time

from app.core.schemas import AskResponse, Citation
from app.core.config import settings
from app.services.llm import generate_answer
from app.services.logging_utils import append_jsonl
from app.services.retrieval import Retriever


class QAService:
    def __init__(self) -> None:
        self.retriever = Retriever()

    def refresh_index(self) -> None:
        self.retriever.reindex()

    def answer(self, question: str) -> AskResponse:
        start = time.perf_counter()
        results = self.retriever.search(question)
        top_score = results[0].score if results else 0.0

        if not results or top_score < settings.min_retrieval_score:
            answer = (
                "I couldn't find enough relevant evidence in the internal knowledge base to answer this confidently.\n\n"
                "This assistant is designed to answer questions from company documents only. "
                "Try asking about PTO, benefits, travel policy, onboarding, product launches, or security incidents."
            )
            mode = "guardrail:no-grounded-answer"
        else:
            answer, mode = generate_answer(question, results)

        latency_ms = int((time.perf_counter() - start) * 1000)
        citations = [
            Citation(
                doc_id=result.doc_id,
                title=result.title,
                chunk_id=result.chunk_id,
                snippet=result.text[:220],
                score=round(result.score, 4),
            )
            for result in results
        ]
        payload = AskResponse(
            answer=answer,
            citations=citations,
            retrieval_debug=[
                {
                    "title": result.title,
                    "chunk_id": result.chunk_id,
                    "score": round(result.score, 4),
                    "source_path": result.source_path,
                }
                for result in results
            ],
            mode=mode,
            latency_ms=latency_ms,
        )
        append_jsonl(
            "app_events.jsonl",
            {
                "type": "qa_response",
                "question": question,
                "mode": mode,
                "latency_ms": latency_ms,
                "top_retrieval_score": round(top_score, 4),
                "citations": [citation.model_dump() for citation in citations],
            },
        )
        return payload
