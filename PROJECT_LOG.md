# Project Log - Narrative IQ

This file tracks the engineering decisions, architectural changes, and implementation steps for the Narrative IQ project.

---

# NarrativeIQ Progress Summary

## Completed Infrastructure

### 1. Dataset Ingestion
- Multilingual dataset preparation (English, Hindi, Marathi).
- Successfully ingested/generated 2,654 story chunks across three languages.

### 2. Chunking Pipeline
- Semantic paragraph-based chunk generation.
- Metadata enrichment with unique IDs, word counts, and language tags.
- Total chunks: 2,654.

### 3. Metadata Pipeline
- Overhauled with Groq `llama-3.3-70b-versatile` for high-quality semantic tagging.
- Multilingual support for Genre, Scene Type, and Dialogue Density.
- Robust API key rotation (5 keys) and 65s rate-limit recovery.
- Strict validation for categorical tags.
- 100% dataset coverage (2,654/2,654).
- Resume/recovery system implemented.
- Fallback handling and validation pipeline.

### 4. Embeddings Pipeline
- Integrated `intfloat/multilingual-e5-base` for dense vector representation.
- 768-dimensional semantic vectors generated for the full dataset.
- Resilient batch processing with embedding status tracking.
- Full dataset embedding success (2654/2654).

### 5. Embedding Validation
- Semantic similarity testing confirmed healthy clustering.
- Multilingual semantic alignment verification (e.g., English queries retrieving relevant Hindi/Marathi chunks).
- Cross-language retrieval validation.
- Healthy semantic clustering confirmed.

### 6. FAISS Vector Store
- Implemented `IndexFlatL2` for exact nearest-neighbor search.
- Efficient vector/metadata separation.
- Persistent FAISS storage.
- Metadata mapping.
- Successful indexing of all 2,654 vectors with float32 optimization.

### 7. Semantic Retriever
- End-to-end query embedding and FAISS search pipeline.
- Multilingual semantic narrative search.
- Successful retrieval validation for complex themes:
    - *Emotional family conflict*
    - *Thriller scenes*
    - *Fantasy scenes*
    - *Family/dinner scenes*

## Current Architecture
**Raw Stories** → **Chunking** → **Metadata Tagging** → **Embeddings** → **FAISS Vector Store** → **Semantic Retriever**

## Current Status
NarrativeIQ now supports:
- Multilingual semantic retrieval.
- Cross-language narrative search.
- Metadata-aware narrative storage.
- Retrieval-ready RAG backbone.

## Next Planned Steps
- Metadata-aware filtered retrieval (Genre/Scene filtering).
- Reranking layer for improved precision.
- Narrative analysis agent (Emotion/Pacing/Repetition).
- Writer feedback generation UI.

---

## Engineering History

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
    - **Optimization:** Global model loading and manual batch processing (batch_size=32).
    - **Resilience:** Implemented isolated batch-level exception handling to prevent entire pipeline failure on single-batch errors.
    - **Tracking:** Added `embedding_status` metadata and detailed success/failure statistics.
    - **Persistence:** Results stored as a pickle file (`.pkl`) to preserve numpy arrays and metadata.
- **Status:** Completed. Refactored for production safety and verified with a 20-chunk resilient test run.

### 7. Vector Storage with FAISS (`src/rag/vector_store.py`)
- **What:** Implemented a vector storage and management system using FAISS.
- **Why:** To enable efficient, low-latency semantic retrieval of story chunks.
- **Approach:** 
    - **Index Type:** Used `IndexFlatL2` for exact distance calculations (brute-force L2 search).
    - **Precision:** Enforced `float32` for all embeddings as required by FAISS optimizations.
    - **Optimization:** Separated vector storage (`.faiss`) from metadata storage (`.pkl`) to keep the retrieval process lightweight.
    - **Utility:** Provided helper functions for creating, saving, and loading indices.
- **Status:** Completed. Verified indexing and loading with a 50-chunk sample.


### 8. Multi-Paragraph Story Format
- **Why:** To test the chunking pipeline, stories needed multiple paragraphs. 
- **Change:** Updated generation prompts to enforce exactly 3 paragraphs per story with blank line separators and dialogue.
- Status: 30/30 stories successfully regenerated using a hybrid approach (`llama-3.1-8b-instant` used for the final 28 stories to bypass 70b rate limits).
    - Logic: Added file-skip logic to the ingestion script to support incremental generation.

## [2026-05-21] - Full Metadata Tagging & API Resilience

### 1. Robust Metadata Pipeline (`src/ingestion/metadata_pipeline.py`)
- **What:** Overhauled the tagging pipeline to support large-scale processing.
- **Why:** To process the entire 2,654 chunk dataset with high-quality `llama-3.3-70b-versatile` tags without failing due to rate limits.
- **Approach:**
    - **API Key Rotation:** Implemented rotation across 5 Groq API keys with automatic failover.
    - **Resilience:** Added a 65-second sleep when all keys hit rate limits to allow for quota resets.
    - **Quality Control:** Refined prompts with clear definitions and added strict validation for genre, scene type, and dialogue density.
- **Results:** 100% of the dataset (2,654 chunks) successfully tagged.
- Distribution:
    - **Genres:** slice_of_life: 1647, fantasy: 793, drama: 125, thriller: 67, romance: 22.
    - **Scenes:** action: 779, dialogue: 654, description: 629, emotional: 488, conflict: 104.
    - **Dialogue Density:** none: 1286, low: 553, high: 524, medium: 291.
- **Status:** Completed. Data saved to `data/processed/tagged_chunks_final.json`.

### 2. Metadata Validation (`check_metadata.py`)
- **What:** Automated validation script to verify tagging quality.
- **Why:** To detect "fallback pollution" where the API might have returned default values during rate-limit failures.
- **Approach:**
    - Randomly sampled 15 chunks (5 per language) with `random.seed(42)`.
    - Calculated "Fallback Pattern" rate (slice_of_life + description).
- **Results:**
    - **Pollution Rate:** 15.3% (Well below the 60% danger threshold).
    - **Verification:** Manually inspected samples confirmed high semantic accuracy across English, Hindi, and Marathi.
- **Status:** Data verified and ready for RAG/Scoring.

### 3. Embedding Pipeline Refactor (`src/rag/embeddings.py`)
- **What:** Added CLI argument support and validation for the embedding process.
- **Why:** To allow easy switching between small-scale tests and full-dataset processing.
- **Approach:**
    - Integrated `argparse` for `--test` mode (20 chunks).
    - Verified 768-dimension vector generation using `multilingual-e5-base`.
- **Status:** Verified with a 20-chunk test run. Ready for full dataset encoding.

### 4. Vector Store Implementation (`src/rag/vector_store.py`)
- **What:** Completed the FAISS vector database for sub-second semantic retrieval.
- **Why:** To provide an efficient and scalable search infrastructure for multilingual narratives.
- **Approach:**
    - Used `faiss.IndexFlatL2` for exact nearest-neighbor search.
    - Separated high-dimensional vectors (`.faiss`) from metadata (`.pkl`) for memory efficiency.
    - Verified the complete dataset of 2,654 chunks was indexed with 768-dimension alignment.
- **Status:** Completed and verified with 100% data coverage.

### 5. Semantic Retriever Implementation (`src/rag/retriever.py`)
- **What:** Built the semantic search interface for multilingual narrative retrieval.
- **Why:** To enable sub-second, cross-lingual discovery of story chunks based on semantic meaning rather than keywords.
- **Approach:**
    - Integrated `multilingual-e5-base` with the mandatory `query: ` prefix for high-accuracy retrieval.
    - Implemented a lazy-loading resource manager to optimize memory usage.
    - Verified retrieval with complex cross-lingual queries (e.g., "emotional family conflict").
- **Status:** Completed and verified.

## Final System Capabilities

NarrativeIQ now supports:

- multilingual semantic narrative retrieval
- cross-language story search
- semantic vector search using FAISS
- metadata-aware narrative indexing
- semantic clustering of emotional and thematic scenes
- retrieval-augmented narrative infrastructure
- scalable multilingual RAG architecture

Example capabilities:
- English queries retrieving Hindi emotional scenes
- fantasy/adventure semantic retrieval
- thriller atmosphere detection
- family/emotional scene discovery

Current retrieval stack:

User Query
→ Query Embedding
→ FAISS Semantic Search
→ Metadata Mapping
→ Narrative Retrieval

Core Technologies:
- Sentence Transformers (`multilingual-e5-base`)
- FAISS (`IndexFlatL2`)
- Groq (`llama-3.3-70b-versatile`)
- Python
- NumPy
- Pickle-based metadata persistence

Current Project State:
The multilingual semantic retrieval backbone is now fully operational and validated across English, Hindi, and Marathi datasets.
