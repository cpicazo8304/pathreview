# Notes

## Important Files

### hybrid.py

Uses vector_store.py and keyword_search.py to find the best chunks to attach to the prompt.

- vector_store looks at relevant chunks that semantically match with the query.

- keyword search finds relevant chunks through keywords in the query.

- Together, they find the max_chunks amount of chunks to attach to the prompt.

### review_generator.py

Uses prompt_templates.py and output_parser.py

- prompt templates contains the templates that will be fed into the LLM (includes ways to add the context from chunks, and other info like profiles, etc.)

- output_parser organizes the LLM's output to something more structured.


### eval_suite.py

Uses relevance_scorer.py and faithfulness_checker.py to get a final overall score of the RAG pipeline.

- Relevance scorer gets the chunk's texts and scores it based on matching words with the query.

- Faithfulness checker checks if the feedback matches well with the context. Checks how many of its claims is supported by the context of the chunks (through word matching).
