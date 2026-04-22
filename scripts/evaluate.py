from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings
from app.services.logging_utils import append_jsonl
from app.services.qa import QAService


def token_set(text: str) -> set[str]:
    return {token.strip(".,:;!?()[]").lower() for token in text.split() if token.strip()}


def overlap_score(candidate: str, reference: str) -> float:
    candidate_tokens = token_set(candidate)
    reference_tokens = token_set(reference)
    if not reference_tokens:
        return 0.0
    return len(candidate_tokens & reference_tokens) / len(reference_tokens)


def citation_hit_rate(retrieved_sources: list[str], expected_sources: list[str]) -> float:
    if not expected_sources:
        return 0.0
    matches = sum(1 for source in expected_sources if source in retrieved_sources)
    return matches / len(expected_sources)


def main() -> None:
    qa = QAService()
    rows = json.loads(Path(settings.eval_file).read_text(encoding="utf-8"))
    results = []
    for row in rows:
        response = qa.answer(row["question"])
        retrieved_sources = [citation.doc_id for citation in response.citations]
        usefulness = overlap_score(response.answer, row["reference_answer"])
        faithfulness = citation_hit_rate(retrieved_sources, row["expected_sources"])
        hallucination_flag = 1 if faithfulness == 0 else 0
        result = {
            "id": row["id"],
            "question": row["question"],
            "mode": response.mode,
            "latency_ms": response.latency_ms,
            "usefulness_score": round(usefulness, 3),
            "faithfulness_score": round(faithfulness, 3),
            "hallucination_flag": hallucination_flag,
            "retrieved_sources": retrieved_sources,
            "expected_sources": row["expected_sources"],
            "answer_preview": response.answer[:240],
        }
        results.append(result)

    summary = {
        "question_count": len(results),
        "avg_usefulness": round(mean(row["usefulness_score"] for row in results), 3),
        "avg_faithfulness": round(mean(row["faithfulness_score"] for row in results), 3),
        "hallucination_rate": round(mean(row["hallucination_flag"] for row in results), 3),
        "avg_latency_ms": round(mean(row["latency_ms"] for row in results), 1),
    }
    output = {"summary": summary, "results": results}

    output_path = Path(settings.logs_dir) / "latest_eval.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    append_jsonl("eval_runs.jsonl", output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
