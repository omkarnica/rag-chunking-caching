from pypdf import PdfReader
from utils import load_config

# ---------------------------------------------------------
# Load configuration values from config.yaml
# ---------------------------------------------------------
config = load_config()

pdf_path = config['paths']['data_dir']

# Chunking parameters
parent_size = config['chunking']['parent_size']
parent_overlap = config['chunking']['parent_overlap']
child_size = config['chunking']['child_size']
child_overlap = config['chunking']['child_overlap']

print(load_config())
print(f"Loading PDFs from: {pdf_path}")


# ---------------------------------------------------------
# Function: load_pdf
# Purpose: Read the PDF document and extract text
# ---------------------------------------------------------
def load_pdf():

    # PdfReader returns a reader object containing pages
    reader = PdfReader(pdf_path)

    text = ""

    # Extract text from each page and concatenate
    for page in reader.pages:
        text += page.extract_text()

    print(f"First 100 characters : {text[:100]}")

    return text


# ---------------------------------------------------------
# Function: create_parent_chunks
# Purpose:
# Split the full document into larger parent chunks.
# These provide broader context to the LLM during generation.
# ---------------------------------------------------------
def create_parent_chunks(text):

    start = 0
    parent_chunks = []

    # Sliding window chunking with overlap
    while start < len(text):

        end = start + parent_size

        parent_chunks.append(text[start:end])

        start = end - parent_overlap

    print(f"Number of parent chunks is {len(parent_chunks)}")

    return parent_chunks


# ---------------------------------------------------------
# Function: create_child_chunks
# Purpose:
# Split each parent chunk into smaller child chunks.
# Child chunks are embedded and used for retrieval.
#
# Each child chunk stores the ID of its parent so
# the full parent context can later be retrieved.
# ---------------------------------------------------------
def create_child_chunks(parent_chunks):

    child_chunks = []
    child_id=0

    # enumerate gives both parent_id and parent_text
    for parent_id, parent in enumerate(parent_chunks):

        start = 0

        while start < len(parent):

            end = start + child_size

            child_text = parent[start:end]

            child_chunks.append({
                    "child_id": child_id,
                    "child_text": child_text,
                    "parent_id": parent_id,
                    "parent_text": parent
                    })
            
            child_id += 1

            start = end - child_overlap

    print(child_chunks[0])

    print(f"Number of child chunks is {len(child_chunks)}")

    return child_chunks


import re


# ---------------------------------------------------------
# Function: question_based_chunking
# Purpose:
# Document-aware chunking based on the structure of the PDF.
# The document contains interview questions labeled as Q1., Q2., etc.
# Each question-answer section is treated as a semantic chunk.
# ---------------------------------------------------------
def question_based_chunking(text):

    pattern = r"Q\d+\."

    raw_chunks = re.split(pattern, text)

    # clean chunks
    question_chunks = [chunk.strip() for chunk in raw_chunks if len(chunk) > 10]

    overlapped_chunks = []

    for i, chunk in enumerate(question_chunks):

        # add overlap with previous chunk
        if i > 0:
            overlap_text = question_chunks[i-1][-child_overlap:]
            chunk = overlap_text + " " + chunk

        overlapped_chunks.append({
            "chunk_id": i,
            "text": chunk
        })

    print(f"Number of question-based chunks: {len(overlapped_chunks)}")

    return overlapped_chunks

# ---------------------------------------------------------
# Pipeline Execution
# ---------------------------------------------------------

pdf = load_pdf()

# Strategy 1: Parent-Child Chunking
parent_chunks = create_parent_chunks(pdf)
child_chunks = create_child_chunks(parent_chunks)

# Strategy 2: Document-aware Question Chunking
question_chunks = question_based_chunking(pdf)

