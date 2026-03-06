import chromadb
from sentence_transformers import SentenceTransformer
from utils import load_config


config = load_config()

embedding_model_name = config["models"]["embedding_model"]


class VectorDatabase:

    def __init__(self):

        # initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # initialize chroma client
        self.client = chromadb.Client()

        self.collection = self.client.create_collection(name="rag_chunks")


    def store_chunks(self, child_chunks):

        for chunk in child_chunks:

            embedding = self.embedding_model.encode(chunk["child_text"]).tolist()

            self.collection.add(
                ids=[str(chunk["child_id"])],
                embeddings=[embedding],
                documents=[chunk["child_text"]],
                metadatas=[{"parent_id": chunk["parent_id"]}]
            )


    def query(self, query, k=5):

        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        return results