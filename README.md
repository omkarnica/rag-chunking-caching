# RAG System with Intelligent Chunking and Multi-Layer Caching

## Overview

This project implements a modular Retrieval-Augmented Generation (RAG) pipeline designed to resemble a production-style architecture.

The system focuses on improving three core areas of a typical RAG pipeline:

* **Document chunking quality**
* **Retrieval efficiency**
* **Query latency through caching**

Instead of relying on high-level frameworks, the system builds each stage of the pipeline explicitly to make the architecture transparent and easy to extend.

The pipeline processes a document containing interview questions and answers and allows users to query the content through a retrieval-augmented language model.

---

## Key Features

**1. Intelligent Chunking**

Two chunking strategies are implemented:

* **Parent–Child Chunking**

  * Large parent chunks preserve context
  * Smaller child chunks improve retrieval precision

* **Document-Aware Chunking**

  * Uses document structure (e.g., `Q1.`, `Q2.` patterns)
  * Produces semantically meaningful chunks

---

**2. Vector Retrieval**

* Embeddings generated using:

  `sentence-transformers/all-MiniLM-L6-v2`

* Vector database:

  **ChromaDB**

* Retrieval process:

  * Query embedding
  * Vector similarity search
  * Child chunk retrieval
  * Parent context reconstruction
  * Ranking by similarity score

---

**3. Multi-Layer Caching**

To reduce redundant computation and improve response time, three cache layers are implemented.

| Cache Layer     | Purpose                                      |
| --------------- | -------------------------------------------- |
| Exact Cache     | Returns stored answers for identical queries |
| Semantic Cache  | Detects semantically similar queries         |
| Retrieval Cache | Avoids repeated vector database searches     |

---

**4. Modular Architecture**

Each component of the system is isolated into its own module.

This makes the system easier to maintain, test, and extend.

---

## Project Structure

```
rag_chunking_caching/

src/
│
├── ingestion.py
├── database.py
├── retriever.py
├── generation.py
├── caching.py
├── utils.py
└── main.py

docs/
└── architecture.md

data/
└── RAG_Interview_Questions_Guide.pdf

config.yaml
requirements.txt
.env
README.md
```

---

## System Architecture

The full query pipeline is shown below.

```
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
```

This layered approach improves both **retrieval efficiency** and **response latency**.

---

## Document Processing Pipeline

The ingestion stage processes the PDF document and produces structured chunks.

```
PDF
 ↓
Text Extraction
 ↓
Parent Chunking
 ↓
Child Chunking
 ↓
Embedding Generation
 ↓
Vector Database Storage
```

Each child chunk stores metadata linking it to its parent chunk.
This enables the system to retrieve precise matches while still providing full contextual information to the language model.

---

## Language Model

The system uses a Groq-hosted language model for generation.

Example configuration:

```
llama3-8b-8192
```

The model receives:

* retrieved parent context
* user query
* instructions for grounded answering

The prompt encourages answers that rely only on retrieved context.

---

## Configuration

All configurable parameters are stored in `config.yaml`.

Example settings:

```
chunking:
  parent_size: 1000
  parent_overlap: 100
  child_size: 200
  child_overlap: 20

models:
  embedding_model: sentence-transformers/all-MiniLM-L6-v2
  llm_model: llama3-8b-8192

cache:
  semantic_threshold: 0.85
  ttl_seconds: 3600
```

This makes the pipeline easier to modify without editing code.

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/rag-chunking-caching.git
cd rag-chunking-caching
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## Running the System

Start the RAG pipeline:

```
python src/main.py
```

Then enter queries in the terminal.

Example:

```
Ask a question: What are common RAG interview questions?
```

---

## Possible Extensions

This system can be extended in several directions:

* Cross-encoder reranking
* Hybrid search (BM25 + vector search)
* Persistent vector databases
* Query expansion
* Evaluation pipelines
* Streaming responses

---

## Purpose of the Project

The goal of this project is to demonstrate how a RAG pipeline can be built from modular components while following architectural patterns commonly used in production systems.

It emphasises transparency of the retrieval pipeline and practical improvements such as chunking strategies and caching layers.
