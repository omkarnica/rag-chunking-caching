"""
Caching layer.

Three types of caching:
1. Exact match cache
2. Semantic similarity cache
3. Retrieval cache
"""

import numpy as np
from sentence_transformers import SentenceTransformer


class CacheManager:

    def __init__(self, config):

        # Exact query cache
        self.exact_cache = {}

        # Semantic cache stores embeddings
        self.semantic_cache = {}

        # Retrieval cache stores retrieved docs
        self.retrieval_cache = {}

        self.similarity_threshold = config["cache"]["semantic_threshold"]

        model_name = config["models"]["embedding_model"]
        self.embedding_model = SentenceTransformer(model_name)

    def get_exact(self, query):
        """
        Check if exact query already exists.
        """

        return self.exact_cache.get(query)

    def store_exact(self, query, answer):
        """
        Store exact query result.
        """

        self.exact_cache[query] = answer

    def get_semantic(self, query):
        """
        Check if a semantically similar query exists.
        """

        query_embedding = self.embedding_model.encode(query)

        for cached_query, (embedding, answer) in self.semantic_cache.items():

            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )

            if similarity > self.similarity_threshold:
                return answer

        return None

    def store_semantic(self, query, answer):
        """
        Store query embedding for semantic lookup.
        """

        embedding = self.embedding_model.encode(query)

        self.semantic_cache[query] = (embedding, answer)

    def get_retrieval(self, query):
        """
        Check if we already retrieved documents for this query.
        """

        return self.retrieval_cache.get(query)

    def store_retrieval(self, query, docs):
        """
        Store retrieved documents.
        """

        self.retrieval_cache[query] = docs