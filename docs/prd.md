# PRD: Internal Knowledge Assistant

## Product Summary

The Internal Knowledge Assistant helps employees quickly find trustworthy answers from company documents such as policies, playbooks, and process docs. The product combines document retrieval, grounded answer generation, and source citations so employees can self-serve without creating extra work for HR, IT, or operations teams.

## Problem

Employees regularly ask repeat questions in Slack or email:

- "What is the PTO carryover policy?"
- "Who needs to approve international travel?"
- "What do I do during a security incident?"

Today, answers are slow, inconsistent, and hard to audit. Teams waste time answering the same questions, and employees may act on outdated or incomplete information.

## Why It Matters

- Reduces time spent answering repetitive internal questions
- Improves trust because answers are grounded in company sources
- Creates a measurable path to scaling internal knowledge support
- Demonstrates how AI can support internal productivity with lower risk than customer-facing deployments

## Target Users

- Employees who need quick policy or process answers
- Managers who need operational guidance
- Internal enablement teams who want fewer repetitive requests

## Jobs To Be Done

- When I have a policy question, I want a fast answer with a source so I can act confidently.
- When I manage a team, I want reliable internal guidance without searching across multiple docs.
- When I evaluate AI tooling, I want measurable answer quality and failure analysis.

## Goals

- Deliver useful answers in under 5 seconds for a demo knowledge base
- Show source grounding for every answer
- Provide a lightweight evaluation framework for usefulness, faithfulness, hallucination rate, and retrieval quality

## Non-Goals

- Full enterprise permissions model
- Real-time syncing from Google Drive, Confluence, or SharePoint
- Advanced admin analytics dashboards
- Complex agentic workflows

## MVP Scope

- Local document ingestion from Markdown files
- Chunking and TF-IDF retrieval
- LLM-backed answer generation with fallback mode
- Answer citations and retrieval debug output
- Evaluation script with benchmark questions and structured logs

## User Flow

1. User asks a question in the web app.
2. System retrieves top matching document chunks.
3. Answer generation uses only retrieved context.
4. UI returns answer, citations, and retrieval metadata.
5. Evaluation pipeline scores response quality against reference examples.

## Key Risks

- Wrong document chunk retrieved for ambiguous questions
- Answer sounds confident even when evidence is weak
- Small demo knowledge base can overstate real-world performance

## Tradeoffs

### Accuracy vs Speed

Using lightweight TF-IDF retrieval keeps setup and latency simple, but semantic retrieval would likely improve recall for more nuanced phrasing.

### Cost vs Quality

An OpenAI-backed generation layer improves answer quality, but the fallback extractive mode keeps the demo runnable with zero API cost.

### Retrieval Breadth vs Precision

Higher `top_k` improves recall but can introduce distractor chunks; lower `top_k` is faster and cleaner but may miss supporting context.

## Open Questions For Future Iteration

- Should the assistant ask clarifying questions when retrieved evidence conflicts?
- What trust threshold should trigger "I’m not confident enough to answer"?
- Which internal document types create the highest ROI for ingestion first?
