# src/retriever.py

"""
Retriever module.

Steps:
1. Embed query
2. Perform vector search
3. Rank parent chunks based on best child similarity
4. Return ordered parent contexts
"""

from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self, config, vector_db):

        self.vector_db = vector_db

        model_name = config["models"]["embedding_model"]
        self.embedding_model = SentenceTransformer(model_name)

        self.top_k = config.get("retrieval", {}).get("top_k", 5)

    def retrieve(self, query):

        # Convert query to embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search vector DB
        results = self.vector_db.search(query_embedding, self.top_k)

        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        parent_scores = {}

        for meta, distance in zip(metadatas, distances):

            parent_id = meta["parent_id"]
            parent_text = meta["parent_text"]

            # Convert distance to similarity score
            score = 1 - distance

            if parent_id not in parent_scores:
                parent_scores[parent_id] = (parent_text, score)

            else:
                # Keep best score for that parent
                existing_score = parent_scores[parent_id][1]

                if score > existing_score:
                    parent_scores[parent_id] = (parent_text, score)

        # Sort parents by score
        sorted_parents = sorted(
            parent_scores.values(),
            key=lambda x: x[1],
            reverse=True
        )

        # Return only text
        contexts = [item[0] for item in sorted_parents]

        return contexts