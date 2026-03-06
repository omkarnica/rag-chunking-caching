# Production-Style RAG System with Intelligent Chunking and Caching

## Overview

This project implements a modular Retrieval-Augmented Generation (RAG) system designed to mimic a production-style architecture.

The system focuses on three key improvements over naive RAG systems:

- Intelligent document chunking
- Multi-layer caching
- Modular and scalable architecture

The goal is to improve retrieval quality, reduce latency, and demonstrate best practices used in modern RAG pipelines.

---

# System Architecture

The system follows the pipeline below:

User Query
↓
Exact Cache
↓
Semantic Cache
↓
Retrieval Cache
↓
Vector Database Search
↓
Parent Context Assembly
↓
LLM Generation
↓
Cache Update
↓
Answer Returned

---

# Project Structure
rag_chunking_caching/

src/
ingestion.py
database.py
retriever.py
generation.py
caching.py
main.py
utils.py

docs/
architecture.md

data/
RAG_Interview_Questions_Guide.pdf

config.yaml
.env
requirements.txt


---

# Document Ingestion

The system uses two chunking strategies.

## Parent–Child Chunking

Parent chunks provide larger context while child chunks are used for retrieval.

Configuration:

parent_size = 1000  
parent_overlap = 100  
child_size = 200  
child_overlap = 20  

Pipeline:

PDF  
↓  
Extract Text  
↓  
Parent Chunks  
↓  
Child Chunks  

Each child chunk contains metadata linking it to its parent.

Example structure:
{
"child_id": 0,
"child_text": "...",
"parent_id": 3,
"parent_text": "..."
}

---

## Document-Aware Chunking

The dataset contains interview questions structured as:

Q1.  
Q2.  
Q3.  

Regex splitting is used:


This produces semantically meaningful chunks aligned with the document structure.

---

# Vector Database

The system uses **ChromaDB** as the vector store.

Each child chunk is embedded using:

sentence-transformers/all-MiniLM-L6-v2

Stored information:

Embedding → child_text  
Metadata → parent_id, parent_text  

During retrieval, child chunks are matched and their parent context is reconstructed.

---

# Retrieval Pipeline

Retrieval follows these steps:

1. Query embedding generation
2. Vector search in ChromaDB
3. Top-K child chunk retrieval
4. Parent chunk reconstruction
5. Parent ranking based on similarity score

Returning parent chunks improves context quality for generation.

---

# Multi-Layer Caching

Three cache layers reduce redundant computation.

## Exact Cache

Maps:

query → answer

Used for identical repeated queries.

---

## Semantic Cache

Stores embeddings of previous queries.

If a new query is semantically similar to a cached query (similarity > threshold), the cached answer is returned.

---

## Retrieval Cache

Maps:

query → retrieved documents

This avoids repeated vector database searches.

---

# Generation Layer

The final answer is generated using a Groq-hosted LLM.

Model used:

llama3-8b-8192

Prompt structure:

Context  
Question  
Instructions for grounded answering

The model generates answers strictly based on retrieved context.

---

# Configuration System

All parameters are controlled via `config.yaml`.

This includes:

- chunk sizes
- embedding model
- LLM model
- cache settings

This makes the system easy to modify without changing code.

---

# Key Features

- Parent–Child chunking strategy
- Document-aware chunking
- ChromaDB vector storage
- Multi-layer caching
- Modular architecture
- Groq LLM integration

---

# Future Improvements

Potential extensions include:

- Reranking using cross-encoder models
- Query expansion
- Hybrid retrieval (BM25 + vector)
- Persistent vector database
- Streaming LLM responses

---

# Conclusion

This project demonstrates how a production-style RAG system can be built using modular components and efficient retrieval strategies.

The architecture focuses on improving retrieval quality, minimizing latency through caching, and maintaining flexibility through configuration-driven design.