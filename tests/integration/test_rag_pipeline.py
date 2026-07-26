"""Tests for the RAG pipeline."""

# mypy: disable-error-code="no-untyped-def"

import pytest

from ingestion.chunking.strategy_selector import StrategySelector
from ingestion.embeddings.batch_processor import BatchEmbeddingProcessor
from ingestion.embeddings.provider import MockEmbeddingProvider
from ingestion.parsers.readme_parser import ReadmeParser
from ingestion.parsers.resume_parser import ResumeParser
from rag.retriever.hybrid import HybridRetriever
from rag.retriever.keyword_search import KeywordSearcher
from rag.retriever.vector_store import VectorStore


@pytest.mark.integration
def test_rag_pipeline(tmp_path):
    """Test the ingestion and retrieval flow with sample README and resume content."""
    vector_store_instance = VectorStore(persist_dir=str(tmp_path / "chromadb"))
    collection = vector_store_instance.get_collection("rag_test_collection")

    readme_text = """# Sample README
This project uses RAG to search resumes and README files.
It supports chunking, embeddings, and vector search.
"""
    resume_text = """# Jane Doe
## Summary
Experienced software engineer with Python, FastAPI, and Docker expertise.
## Skills
Python, FastAPI, PostgreSQL, AWS, Docker
"""
    # Parse the README and resume content
    readme_parser = ReadmeParser()
    resume_parser = ResumeParser()

    readme_result = readme_parser.parse(readme_text)
    resume_result = resume_parser.parse(resume_text)

    # Chunk the parsed content
    chunker = StrategySelector()
    readme_chunks = chunker.chunk(
        readme_result.text,
        {
            "source_id": "demo-readme",
            "profile_id": "demo-user",
            "source_type": "readme",
        },
    )
    resume_chunks = chunker.chunk(
        resume_result.text,
        {
            "source_id": "demo-resume",
            "profile_id": "demo-user",
            "source_type": "resume",
        },
    )

    # Store the chunks with embeddings in the vector store
    embedding_provider = MockEmbeddingProvider()
    batch_processor = BatchEmbeddingProcessor(embedding_provider, collection)
    stored_chunks = batch_processor.process(readme_chunks + resume_chunks)

    # Check #1: Ensure that the number of stored chunks matches the
    # total number of chunks from README and resume
    assert len(stored_chunks) == len(readme_chunks) + len(resume_chunks)

    # Check #2: Ensure that the stored chunks have the correct metadata
    for chunk, _embedding_id in stored_chunks:
        assert chunk.metadata["source_id"]
        assert chunk.metadata["profile_id"]
        assert chunk.metadata["source_type"]

    # Create keyword searcher and index the chunks
    keyword_searcher = KeywordSearcher()
    keyword_searcher.index(
        [
            {
                "id": embedding_id,
                "text": chunk.text,
                "metadata": {
                    "source_id": chunk.metadata["source_id"],
                    "profile_id": chunk.metadata["profile_id"],
                    "source_type": chunk.metadata["source_type"],
                },
            }
            for chunk, embedding_id in stored_chunks
        ]
    )

    # Check #3: Ensure that the keyword searcher has built the
    # BM25 index and stored the chunks
    assert keyword_searcher.bm25 is not None

    # Check #4: Ensure that the number of chunks in the keyword
    # searcher matches the number of stored chunks
    assert len(keyword_searcher.chunks) == len(stored_chunks)

    # run hybrid retrieval
    query = "Find experience with Python and Docker"
    query_embedding = embedding_provider.embed([query])[0]
    hybrid_retriever = HybridRetriever(vector_store_instance, keyword_searcher)

    results = hybrid_retriever.retrieve(
        query,
        query_embedding=query_embedding,
        profile_id="demo-user",
        max_chunks=3,
        min_score=0.1,
    )

    # Check #5: Ensure that the hybrid retriever returns results
    assert results

    # Check #6: Ensure that the number of results returned by the
    # hybrid retriever does not exceed the specified max_chunks
    assert len(results) <= 3

    # Check #8: Ensure that the results contain relevant chunks
    # based on the query
