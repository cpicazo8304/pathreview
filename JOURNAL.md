## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/38 

**Issue title:** Add an integration test that runs the full RAG pipeline against a mock LLM

**Tier:** [ ] Tier 1  [X] Tier 2  [ ] Tier 3

**Problem summary:**

The issue is that there doesn't exist a test that doesn't test the full RAG pipeline (querying, reranking, generation, etc). Need to create a test that has a checkpoint at each checkpoint, making sure the process is going well. 

**Why I chose this issue:** I chose this issue because it seemed something that could be meaningful but at the same time not as complex as other tier-2 issues. I have done simple issues, so wanted a step up.

**Branch name:** test/38-add-rag-integration-test

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger


## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/cpicazo8304/pathreview/commit/857423dbc7b397b01e09cf62afe3ebcaa81f1501 

**Reproduction summary:**
Ran

'make test-integration' 

But, this lead to no tests being ran, pointing to the fact that a test for the entire RAG pipeline is needed.

Additionally, the only tests are unit tests (as said in issue #38), that test individual sections of the RAG pipeline:

- test_faithfulness_checker.py
- test_keyword_search.py
- test_output_parser.py
- test_prompt_templates.py
- test_relevance_scorer.py

**PLAN.md link:** [\[link to PLAN.md in your fork\]](https://github.com/cpicazo8304/pathreview/blob/test/38-add-rag-integration-test/PLAN.md)

**Blockers or open questions:**

Would a test of the RAG pipeline be a combination of the unit tests? Like having certain checkpoints to check how the RAG pipeline is doing? If the certain parts of the pipeline are doing what they are supposed to be doing?


## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
[What have you implemented so far? Which sub-tasks from PLAN.md are done?]

- Add ingestion to RAG pipeline to check this section of the RAG pipeline. 

**Next steps:**
[What are you working on for the rest of the week?]

- Add in the retrieval step and generation step to test. 

**Blockers:**
[Anything slowing you down? Or leave blank.]

- There is a lot of formatting errors in the other files that I had not touched. This is from the original repository and some may be issues that students could be fixing up, but it is affecting my test in turn. 

---

### Check-in 2 (end of week)

**PR link:** https://github.com/cpicazo8304/pathreview/blob/test/38-add-rag-integration-test/PR.md 

**Branch:** test/38-add-rag-integration-test

**What you built:**
My fix adds in a test for the integration of the RAG pipeline. It goes through ingestion (testing parsing, chunking, and embedding) of documents that will be added to an example vector store, retrieval of chunks in relation to a query, and generation of an answer according to context + query. The intregation test is able to fully check each stage.

**Tests added or updated:**
[Which test files did you touch? What do they cover?]
Added integration test: tests/integration/test_rag_pipeline.py

**Self-review confirmation:** [X] make check passes  [X] make test-unit passes

**Draft PR feedback received from:** none