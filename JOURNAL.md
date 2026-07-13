## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/29

**Issue title:** Add a max_chunks parameter to the retriever to limit context window usage

**Tier:** [X] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**

The issue is that there doesn't exist a max_chunks variable in the hybrid retrieval step. When there is a large portfolio, there may be a lot of chunks that are returned, so it can lead to the retrieval returning a lot of results, that can overflow the context window of the LLm leading to weak answers due to truncation. This is located in rag/retriever/hybrid.py and rag/retriever/vector_store.py. Adding the max_chunks should lead to the LLM focusing on the top k chunks, that should give meaninful context without overflowing the context window. This should be able to be tweaked as a config so that it can be properly tuned.

**Branch name:** feat/29-add-max-chunks

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger