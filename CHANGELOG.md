# Project Log - Narrative IQ

This file tracks the engineering decisions, architectural changes, and implementation steps for the Narrative IQ project.

## [2026-05-20] - Initial Ingestion and RAG Setup

### 1. Dataset Ingestion Script (`src/ingestion/download_datasets.py`)
- **What:** Created a script to collect story datasets for English, Hindi, and Marathi.
- **Why:** To build a multilingual corpus for story analysis and RAG.
- **Approach:** 
    - **English:** Downloads 500 stories from HuggingFace's `TinyStories`.
    - **Hindi/Marathi:** Initially planned as dataset downloads, but shifted to synthetic generation.
- **Status:** Completed.

### 2. Infrastructure Updates
- **Why:** Addressed HuggingFace's security policy changes and model deprecations.
- **Changes:**
    - Enabled `trust_remote_code=True` for Hindi dataset loading (before migration to synthetic).
    - Upgraded Groq model from `llama3-8b-8192` to `llama-3.3-70b-versatile` for better generation quality and future-proofing.
- **Status:** Completed.

### 3. Shift to Synthetic Indic Data
- **Why:** Legacy Indic datasets (like `hindi_discourse`) were inconsistent and difficult to chunk effectively. Synthetic generation provides control over length, tone, and formatting.
- **Approach:** Used Groq's `llama-3.3-70b-versatile` to generate stories with specific topics (village life, festivals, etc.) and expressive narrative styles.
- **Status:** Hindi (50 stories) regenerated. Marathi (30 stories) pending rate limit reset.

### 4. RAG Chunking Pipeline (`src/rag/chunking.py`)
- **What:** Implemented a paragraph-based chunking system.
- **Why:** Foundation for retrieval-augmented generation. Paragraphs provide better semantic context than fixed-size chunks for stories.
- **Approach:** Recursive file reading, double-newline splitting, and metadata enrichment (unique IDs, word counts, language tags).
- **Status:** Completed.

### 5. Metadata Tagging Pipeline (`src/ingestion/metadata_pipeline.py`)
- **What:** Automated semantic tagging for genre, scene type, and dialogue density.
- **Why:** To enable deep filtering and thematic analysis within the RAG system.
- **Approach:** Refactored for scalability using Groq `llama-3.3-70b-versatile`.
    - **Batching:** Processes 10 chunks per API call to reduce latency and overhead.
    - **Safety:** Implemented 1s rate-limit delay and incremental progress saving to `data/processed/`.
    - **Robustness:** Added safe markdown cleanup, robust JSON array parsing (handling dict-to-list conversion), and fallback metadata defaults.
    - **Fix:** Resolved a `NameError` in the test block caused by incorrect indentation of samples display logic.
- **Status:** Verified with a 15-chunk multilingual batch test (Genres: 10 slice_of_life, 2 fantasy, 3 drama).

### 6. Semantic Embedding Pipeline (`src/rag/embeddings.py`)
- **What:** Implemented a multilingual embedding generation system.
- **Why:** To enable vector-based semantic search across English, Hindi, and Marathi stories.
- **Approach:** 
    - **Model:** Used `intfloat/multilingual-e5-base` from `sentence-transformers`.
    - **Formatting:** Applied "passage: " prefix required for E5 asymmetric retrieval.
    - **Optimization:** Global model loading and batch processing (batch_size=32).
    - **Persistence:** Results stored as a pickle file (`.pkl`) to preserve numpy arrays and metadata.
- **Status:** Completed. Verified with 20-chunk test run (768-dimensional embeddings).


### 7. Multi-Paragraph Story Format
- **Why:** To test the chunking pipeline, stories needed multiple paragraphs. 
- **Change:** Updated generation prompts to enforce exactly 3 paragraphs per story with blank line separators and dialogue.
- **Status:** 
    - Hindi: 50/50 stories successfully regenerated using `llama-3.3-70b-versatile`.
    - Marathi: 30/30 stories successfully regenerated using a hybrid approach (`llama-3.1-8b-instant` used for the final 28 stories to bypass 70b rate limits).
    - Logic: Added file-skip logic to the ingestion script to support incremental generation.

