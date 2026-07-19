## Solution plan

**Issue link:** https://github.com/ascherj/pathreview/issues/38 

**Issue title:** Add an integration test that runs the full RAG pipeline against a mock LLM

### Understand
What is the root cause of this issue? What behavior is expected vs. actual?

- A test that checks if the FULL RAG pipeline works or not is not included. This integration scenario is not tested, which could check for multiple things that cannot be caught when just testing individual components of the RAG pipeline.

- Expected behavior: When running integration tests, there should at least be an integration test that tests the RAG pipeline.

- Actual behavior: When running integration tests, there are none. 

### Map
Which files, functions, or modules are involved?
List the specific files you expect to touch.

- The only file that should be touched is one that should be added:
'tests/integration/test_rag_pipeline.py'

### Plan
What are the steps to fix this issue?
Break it into 3–5 concrete sub-tasks.

Three main files: hybrid.py, review_generator.py

Steps to develop integration test of rag pipeline:

- Create file: 'tests/integration/test_rag_pipeline.py'
- Create a small in-memory test fixture with a few fake chunks and a fake profile payload.
- Use a simple fake vector store and keyword searcher so the retriever can return realistic results.
- Run the hybrid retrieval flow.
- Pass the retrieved chunks into the generator with a stubbed LLM response that returns structured JSON. 
- Assert that the output is parsed into feedback sections and that the final result is non-empty and correctly shaped.

### Inputs & outputs
What does your fix take as input? What should it produce or change?

Inputs:

- A sample query such as “review this candidate’s Python and backend experience.”
- A profile identifier and a dummy query embedding.
- A small set of fake retrieved chunks, including text and metadata.
- A stubbed LLM response that returns structured JSON with sections such as skills_feedback and projects_feedback.


Outputs:

- A list of retrieved chunks ordered by relevance from the hybrid retrieval step.
- A list of generated feedback sections from the generator.
- Parsed section objects with non-empty content, expected section names, and a reasonable confidence value.

The test should verify that the full pipeline completes without crashing and produces the expected structure.

### Risks & unknowns
What could go wrong? What are you still unsure about?

Certain parts of the pipeline could be called wrongly or there could be checks missing that should be tested.

### Edge cases
What inputs or states should your fix handle gracefully?

- No retrieved chunks:

The pipeline should still complete gracefully and produce a fallback result or empty output without crashing.
Low-confidence or low-scoring retrieval:

The retriever should still return a valid list, even if the results are weak.

- Malformed LLM output:

The parser should fall back safely rather than breaking the integration test.

- Missing metadata in chunks:

The generator should still format context safely and not fail because a source_id or similar field is absent.
Missing profile fields:

The generator should use defaults such as empty strings or zero values rather than crashing.