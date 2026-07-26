Added a new regression test for the RAG pipeline integration flow in `tests/unit/test_rag_pipeline.py`.

## Summary

This change adds coverage for the end-to-end RAG workflow by introducing a dedicated integration-style test for the pipeline. The goal is to ensure that retrieval and generation continue to work together correctly as part of the broader system behavior.

## Root cause

The RAG pipeline lacked a targeted regression test for the full integration path. Because of that, issues in the combined retrieval and generation flow could slip through without being caught early.

## How to test

1. Run the relevant unit tests:
   `make test-unit`
2. Or run the specific test file directly:
   `pytest tests/unit/test_rag_pipeline.py`
3. Confirm that the new RAG pipeline integration test passes successfully.

## Files changed

| File | Change |
|------|--------|
| `tests/unit/test_rag_pipeline.py` | Added a new integration-focused regression test for the RAG pipeline |

## Tests

- New: `test_rag_pipeline` — validates the end-to-end RAG integration flow and helps catch regressions in pipeline behavior
- Existing tests: continue to pass without changes to the core implementation

## Pre-existing issues

No new issues were introduced by this change.