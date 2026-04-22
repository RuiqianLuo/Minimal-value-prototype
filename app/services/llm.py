from __future__ import annotations

import re
from textwrap import dedent

from openai import OpenAI

from app.core.config import settings
from app.services.retrieval import RetrievalResult


def _build_context(results: list[RetrievalResult]) -> str:
    context_parts = []
    for idx, result in enumerate(results, start=1):
        context_parts.append(
            f"[{idx}] {result.title} | {result.chunk_id}\n{result.text}"
        )
    return "\n\n".join(context_parts)


def _keyword_set(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9-]+", text)}


def _top_sentences(question: str, results: list[RetrievalResult], limit: int = 3) -> list[tuple[str, int]]:
    question_terms = _keyword_set(question)
    scored_sentences: list[tuple[float, str, int]] = []
    for idx, result in enumerate(results, start=1):
        sentences = re.split(r"(?<=[.!?])\s+", result.text.replace("\n", " "))
        for sentence in sentences:
            clean = sentence.strip()
            if len(clean) < 30:
                continue
            overlap = len(_keyword_set(clean) & question_terms)
            if overlap == 0:
                continue
            score = overlap + result.score
            scored_sentences.append((score, clean, idx))
    ranked = sorted(scored_sentences, key=lambda item: item[0], reverse=True)
    selected: list[tuple[str, int]] = []
    seen = set()
    for _, sentence, citation_idx in ranked:
        if sentence in seen:
            continue
        selected.append((sentence, citation_idx))
        seen.add(sentence)
        if len(selected) >= limit:
            break
    return selected


def extractive_fallback(question: str, results: list[RetrievalResult]) -> str:
    if not results:
        return "I could not find a grounded answer in the demo knowledge base."
    best_sentences = _top_sentences(question, results)
    if not best_sentences:
        return "I found related documents, but not enough clear evidence to answer confidently."

    answer_lines = [f"Grounded answer for: {question}"]
    for sentence, citation_idx in best_sentences:
        answer_lines.append(f"- {sentence} [{citation_idx}]")
    answer_lines.append("")
    answer_lines.append("This response was generated in offline extractive mode from retrieved document sentences.")
    return "\n".join(answer_lines)


def generate_answer(question: str, results: list[RetrievalResult]) -> tuple[str, str]:
    client = OpenAI(api_key=settings.openai_api_key)
    prompt = dedent(
        f"""
        You are an internal company knowledge assistant.
        Answer only from the provided context.
        If the context is insufficient, say so clearly.
        Use short, direct language suitable for employees.
        End each claim with citation markers like [1] or [2] based on the provided sources.

        Question:
        {question}

        Context:
        {_build_context(results)}
        """
    ).strip()

    if settings.llm_provider == "gemini" and settings.gemini_api_key:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)
        gemini_models = [settings.gemini_model]
        if settings.gemini_fallback_model and settings.gemini_fallback_model not in gemini_models:
            gemini_models.append(settings.gemini_fallback_model)

        last_error: Exception | None = None
        for model_name in gemini_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                    ),
                )
                text = (response.text or "").strip()
                if text:
                    return text, f"gemini:{model_name}"
            except Exception as exc:
                last_error = exc

        fallback_answer = extractive_fallback(question, results)
        if last_error:
            fallback_answer += (
                "\n\nNote: Gemini was temporarily unavailable, so this answer was served from offline grounded fallback mode."
            )
        return fallback_answer, "extractive"

    if settings.llm_provider == "openai" and settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0.1,
        )
        return response.output_text.strip(), "openai"

    return extractive_fallback(question, results), "extractive"
