# Success Metrics

## Core Product Metrics

- Answer usefulness: overlap between generated answer and reference answer, plus human review for clarity
- Answer faithfulness: whether cited sources match the expected grounding documents
- Hallucination rate: share of responses with no expected source retrieved
- Latency: median end-to-end response time in milliseconds
- Retrieval hit quality: whether the correct source appears in top-k retrieval results
- User satisfaction proxy: percent of answers that would likely avoid a follow-up support question

## MVP Targets

- Average usefulness score above 0.65 on the local benchmark
- Average faithfulness score above 0.80 on the local benchmark
- Hallucination rate below 0.15 on the local benchmark
- Median latency below 5000 ms with OpenAI mode and below 1000 ms in extractive mode
- Correct source in top-4 retrieval results for at least 85 percent of benchmark questions

## Leading Indicators

- Number of repeat questions covered by the knowledge base
- Reduction in manual responses from HR, finance, and security teams
- Number of questions that return "insufficient evidence" instead of a risky answer
