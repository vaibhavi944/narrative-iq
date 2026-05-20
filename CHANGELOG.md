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

### 5. Multi-Paragraph Story Format
- **Why:** To test the chunking pipeline, stories needed multiple paragraphs. 
- **Change:** Updated generation prompts to enforce exactly 3 paragraphs per story with blank line separators and dialogue.
- **Status:** 
    - Hindi: 50/50 stories successfully regenerated using `llama-3.3-70b-versatile`.
    - Marathi: 30/30 stories successfully regenerated using a hybrid approach (`llama-3.1-8b-instant` used for the final 28 stories to bypass 70b rate limits).
    - Logic: Added file-skip logic to the ingestion script to support incremental generation.

