# Error Analysis

## What Can Go Wrong

### Failure Case 1: Retrieval miss

The user asks a good question, but the correct document chunk is not in the top results. This creates downstream answer risk even if the LLM is strong.

Example:

- Question: "Can I roll over unused vacation?"
- Risk: the system may retrieve benefits content instead of PTO policy if retrieval weighting is weak

### Failure Case 2: Partial answer

The answer includes one correct rule but misses a crucial qualifier.

Example:

- Question: "Can I book international travel directly?"
- Good answer: requires manager and finance approval regardless of cost
- Failure: answer mentions only manager approval

### Failure Case 3: Overconfident synthesis

The assistant blends multiple chunks into a neat answer that sounds complete even when evidence is incomplete.

Example:

- Question: "What are the steps after a Sev-1 incident?"
- Risk: answer may mention the review but omit required timeline or incident documentation details

### Failure Case 4: Citation mismatch

The answer text is reasonable, but the cited source is weak or unrelated. This harms trust even if the answer happens to be correct.

## Root Causes

- Sparse keyword retrieval can miss semantically similar wording
- Chunk boundaries can split qualifiers from the main rule
- Generative models may smooth over uncertainty
- Small benchmark sets can hide edge cases

## Recommended Next Improvements

- Move from TF-IDF to embedding retrieval
- Add answer abstention when retrieval scores are low
- Add human-rated evaluation for usefulness and trust
- Expand benchmark coverage with ambiguous and adversarial questions
- Track citation precision separately from answer correctness
