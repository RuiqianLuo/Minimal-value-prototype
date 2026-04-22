# Internal Knowledge Assistant MVP

A portfolio-ready AI product case study and working prototype for an internal knowledge assistant. The project demonstrates how to turn a realistic company pain point into a grounded RAG demo, a measurable evaluation loop, and a clear MVP story for AI Product Manager, AI Product Analyst, and junior PM roles.

## Why this project works for an AI Product portfolio

This project is intentionally framed as a product case study, not a research experiment. It demonstrates:

- A concrete business problem: repetitive internal policy and process questions
- A believable AI workflow: retrieval-augmented generation with citations
- Product thinking: target users, tradeoffs, MVP scope, and measurable outcomes
- Evaluation discipline: benchmark questions, structured logs, and explicit failure modes
- A working demo: lightweight web app with source-grounded answers

## Product Summary

Employees often waste time searching internal docs or asking repeat questions in Slack. This prototype answers those questions using a local knowledge base of sample company documents, cites the evidence it used, and supports evaluation against a small benchmark set.

## Target Users

- Employees looking for fast policy answers
- Managers who need reliable operational guidance
- AI product stakeholders evaluating whether an internal assistant is trustworthy enough to scale

## MVP Scope

- Markdown document ingestion
- Chunking and retrieval
- Grounded answer generation
- Answer citations in the UI
- Guardrail for low-relevance or out-of-scope questions
- Local benchmark evaluation pipeline
- Structured JSON logs for app and evaluation runs

## Architecture

1. Documents are stored locally in `data/docs/`
2. The ingestion layer normalizes and chunks documents
3. The retriever indexes chunks with TF-IDF
4. The answer layer uses OpenAI if a key is present, otherwise extractive fallback mode
5. The app returns answers plus source snippets and retrieval metadata
6. The evaluation script runs benchmark questions and scores response quality

## Product Tradeoffs

- Accuracy vs speed: TF-IDF is fast and simple, but embedding retrieval would likely improve semantic recall.
- Cost vs quality: OpenAI generation improves fluency and synthesis, while offline extractive fallback keeps the demo runnable without API spend.
- Retrieval breadth vs precision: increasing `top_k` can improve recall but may introduce noisier context and weaker citations.

## Evaluation Framework

The project includes 10 benchmark questions in `data/eval/questions.json` with:

- reference answers
- expected grounding documents
- structured output scoring

Current heuristic metrics:

- `usefulness_score`: reference-answer token overlap
- `faithfulness_score`: expected-source hit rate
- `hallucination_flag`: 1 when no expected source is retrieved
- `latency_ms`: end-to-end answer latency

This is intentionally lightweight so the framework is easy to explain in interviews. A strong next step would be adding LLM-as-judge or human review labels.

## Repo Tree

```text
.
├── app
│   ├── core
│   │   ├── config.py
│   │   └── schemas.py
│   ├── services
│   │   ├── ingestion.py
│   │   ├── llm.py
│   │   ├── logging_utils.py
│   │   ├── qa.py
│   │   └── retrieval.py
│   ├── main.py
│   └── templates
│       └── index.html
├── data
│   ├── docs
│   │   ├── benefits_faq.md
│   │   ├── employee_handbook.md
│   │   ├── product_launch_process.md
│   │   ├── security_incident_playbook.md
│   │   └── travel_and_expense_policy.md
│   └── eval
│       └── questions.json
├── docs
│   ├── error_analysis.md
│   ├── feature_prioritization.md
│   ├── prd.md
│   ├── resume_bullets.md
│   ├── success_metrics.md
│   ├── user_personas.md
│   └── user_stories.md
├── logs
├── scripts
│   └── evaluate.py
├── .env.example
├── README.md
└── requirements.txt
```

## How to run locally

### 1. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
```

Add your `OPENAI_API_KEY` to `.env` if you want LLM generation. If you leave it blank, the app still runs in extractive fallback mode.

To use Gemini instead, set:

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-1.5-flash
```

This project uses Google's current `google-genai` Python SDK for Gemini.
If Gemini returns a temporary `503 UNAVAILABLE` due to demand, the app will now retry with the fallback Gemini model and then degrade to offline extractive mode instead of crashing.

To use OpenAI, set:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

### 3. Start the app

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 4. Run evaluation

```bash
python scripts/evaluate.py
```

Results are saved to `logs/latest_eval.json` and appended to `logs/eval_runs.jsonl`.

## Demo talking points

- The UI shows both the answer and the retrieved evidence, which makes trust easier to discuss.
- The code is intentionally modular so each RAG stage is easy to explain.
- The evaluation layer makes this feel like a product iteration loop, not just a one-off demo.

## What makes this a good resume project

- It connects user pain points to a believable AI solution
- It includes both product artifacts and working software
- It demonstrates grounded AI design rather than generic chatbot wrapping
- It shows evaluation maturity, which is highly relevant for AI Product roles
- It is simple enough to explain clearly in interviews, but deep enough to discuss tradeoffs and next steps
