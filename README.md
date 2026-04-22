
# Internal Knowledge Assistant

A lightweight internal knowledge assistant for teams that need fast, source-grounded answers from company documents, with a simple prototype app and a small built-in evaluation workflow.

## Key Features

- Simple web interface for asking questions against an internal document set
- Local document ingestion from `.md` and `.txt` files
- Chunking and TF-IDF retrieval over a demo company knowledge base
- Grounded answer generation with visible citations and retrieval debug output
- Support for OpenAI, Gemini, and offline extractive fallback modes
- Guardrail for low-relevance or out-of-scope questions
- Evaluation script with 10 benchmark questions, expected sources, and structured logs

## Benchmark Snapshot

Current prototype benchmark results from [`logs/latest_eval.json`](./logs/latest_eval.json):

| Metric | Result |
| --- | ---: |
| Question count | 10 |
| Average usefulness | 0.91 |
| Average faithfulness | 1.00 |
| Hallucination rate | 0.00 |
| Average latency (extractive benchmark run) | 0 ms |

These are small-sample prototype results from the local evaluation script, not production performance claims.

## Why This Use Case Matters

Internal teams repeatedly answer the same questions about policies, onboarding, benefits, travel, and incident response. A grounded internal assistant can reduce repetitive support work, improve answer consistency, and make it easier to inspect what source material informed a response.

## Example Questions

- What is the remote work policy for new hires?
- How many PTO days can employees carry over into the next year?
- What approvals are required for international travel?
- What is the reimbursement limit for meals during U.S. business travel?
- When does health coverage start for new employees?
- What is the annual learning and development stipend?
- What is required before a medium-risk product launch?
- What should managers do during a security incident?

## MVP Scope

- Local knowledge base stored in `data/docs/`
- Document normalization and chunking
- TF-IDF retrieval over chunked internal documents
- LLM-backed answer generation when a provider key is configured
- Offline extractive fallback when no provider is configured or generation is unavailable
- Source citations and retrieval debug data in the UI
- Benchmark evaluation with structured output logs

## System Architecture

1. Documents are stored locally in `data/docs/`.
2. The ingestion layer loads and normalizes Markdown files, then splits them into chunks.
3. The retriever indexes those chunks with TF-IDF and returns the top matches for a question.
4. The answer layer uses the retrieved context to generate a grounded response through Gemini or OpenAI, or falls back to extractive mode.
5. The UI displays the answer, citations, latency, and retrieval debug information.
6. The evaluation script runs benchmark questions from `data/eval/questions.json` and writes results to `logs/latest_eval.json`.

## Product Tradeoffs

- Accuracy vs. speed: TF-IDF retrieval is fast and easy to explain, but semantic retrieval would likely improve recall on paraphrased questions.
- Cost vs. quality: model-backed generation improves fluency and synthesis, while extractive fallback keeps the prototype runnable without API spend.
- Retrieval breadth vs. precision: returning more chunks can improve recall, but can also add distractors and weaker citations.

## Evaluation Approach

The repository includes a small benchmark set in `data/eval/questions.json` with:

- 10 test questions
- reference answers
- expected source documents

The evaluation script reports:

- `usefulness_score`: token overlap between generated and reference answers
- `faithfulness_score`: whether expected source documents were retrieved
- `hallucination_flag`: whether no expected source was retrieved
- `latency_ms`: end-to-end response latency for each question

This evaluation is intentionally lightweight. It is useful for iteration and discussion, but it is not a substitute for larger-scale human review or production monitoring.

## Project Documents

- [PRD](./docs/prd.md)
- [User Personas](./docs/user_personas.md)
- [User Stories](./docs/user_stories.md)
- [Feature Prioritization](./docs/feature_prioritization.md)
- [Success Metrics](./docs/success_metrics.md)
- [Error Analysis](./docs/error_analysis.md)

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

To run the benchmark:

```bash
python scripts/evaluate.py
```

## Configuration

By default, the project is configured for extractive fallback mode. That means the app still runs even if no LLM API key is set.

Example default:

```env
LLM_PROVIDER=extractive
```

### Gemini

The project uses Google's current `google-genai` SDK for Gemini.

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-1.5-flash
```

If the primary Gemini model is temporarily unavailable, the app retries with the fallback Gemini model and then degrades to offline extractive mode instead of crashing.

### OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

### Other useful settings

```env
TOP_K=4
MIN_RETRIEVAL_SCORE=0.08
CHUNK_SIZE=550
CHUNK_OVERLAP=100
```

## Repo Structure

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
│   ├── app_events.jsonl
│   ├── eval_runs.jsonl
│   └── latest_eval.json
├── scripts
│   └── evaluate.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Limitations

- The demo knowledge base is small and local; it does not connect to live internal systems.
- Retrieval uses TF-IDF rather than embeddings or reranking.
- The benchmark set is small and heuristic-based.
- There is no authentication, permissions model, or document access control.
- The current app is a single-turn assistant, not a multi-step workflow tool.

## Next Steps

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

=======
