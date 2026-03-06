"""
Main pipeline that connects all modules together.
"""

import yaml

from ingestion import run_ingestion
from database import VectorDatabase
from retriever import Retriever
from generation import Generator
from caching import CacheManager

from dotenv import load_dotenv
load_dotenv()


def main():

    # Load configuration
    config = yaml.safe_load(open("config.yaml"))

    # Run ingestion pipeline
    parent_chunks, child_chunks = run_ingestion(config)

    # Initialize vector database
    vector_db = VectorDatabase(config)
    vector_db.add_documents(child_chunks)

    # Initialize system components
    retriever = Retriever(config, vector_db)
    generator = Generator(config)
    cache = CacheManager(config)

    print("RAG system ready.\n")

    while True:

        query = input("Ask a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        # ---------- Exact Cache ----------
        cached_answer = cache.get_exact(query)

        if cached_answer:
            print("\n[Exact cache hit]\n")
            print(cached_answer)
            continue

        # ---------- Semantic Cache ----------
        cached_answer = cache.get_semantic(query)

        if cached_answer:
            print("\n[Semantic cache hit]\n")
            print(cached_answer)
            continue

        # ---------- Retrieval Cache ----------
        docs = cache.get_retrieval(query)

        if docs is None:
            docs = retriever.retrieve(query)
            cache.store_retrieval(query, docs)

        # ---------- Generation ----------
        answer = generator.generate(query, docs)

        # Store in caches
        cache.store_exact(query, answer)
        cache.store_semantic(query, answer)

        print("\nAnswer:\n")
        print(answer)


if __name__ == "__main__":
    main()