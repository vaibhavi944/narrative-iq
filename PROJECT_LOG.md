# Project Log - Narrative IQ

This file tracks the engineering decisions, architectural changes, and implementation steps for the Narrative IQ project. It serves as the single source of truth for the project's development history.

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

# Final System Capabilities

NarrativeIQ now supports:
- **Multilingual semantic narrative retrieval:** Search across English, Hindi, and Marathi simultaneously.
- **Cross-language story search:** Retrieve relevant content even if the query language differs from the story language.
- **Semantic vector search:** Powered by FAISS and E5 embeddings for high-accuracy thematic matching.
- **Metadata-aware narrative indexing:** High-quality tags for genre, scene type, and dialogue density.
- **Semantic clustering:** Automatically groups emotional and thematic scenes across the dataset.
- **Scalable architecture:** Robust pipelines for large-scale multilingual RAG.

---

# Engineering History & Approach Changes

## Phase 1 — Heuristic Foundation (2026-05-18)
The goal was to establish a robust linguistic foundation using heuristic analysis and large language models (Groq) for deeper emotional understanding.

### Core Analysis Files:
1. **`src/utils/text_splitter.py`**: Breaks down raw text into paragraphs using double newlines.
2. **`src/features/pacing.py`**: Measures sentence length variance to analyze narrative rhythm.
3. **`src/features/repetition.py`**: Detects repetitive starters, words, and bigrams with multilingual noise filtering.
4. **`src/features/emotion.py`**: Initially lexicon-based, then upgraded to Groq API for literary nuance.
5. **`src/scoring/weakness_scorer.py`**: Aggregates features into qualitative labels (Weak/Moderate/Strong).
6. **`src/scoring/feedback_generator.py`**: Converts raw scores into actionable writing tips.

### Phase 1 Approach Changes:
- **Sentence Splitting**: Moved from simple punctuation splits to `nltk` (English) and regex `[à¥¤?!.]` (Hindi/Marathi) to handle abbreviations and modern punctuation correctly.
- **Emotion Scoring**: Switched from TextBlob/Lexicons to **Groq (Llama 3.3 70B)** because standard tools failed to capture literary subtext and imagery.
- **Scoring Weights**: Implemented language-aware weights (Emotion reduced for Hindi/Marathi) to account for naturally expressive Indic prose style.
- **Repetition Filtering**: Added `len(word) > 1` filter to remove noise from single-character tokens in Hindi and Marathi.

## Phase 2 — Ingestion and RAG Setup (2026-05-20)
Shifted focus to building a high-quality multilingual corpus and the foundation for semantic retrieval.

### 1. Dataset Ingestion & Synthetic Shift
- **Approach**: Ingested 500 English `TinyStories`. For Hindi and Marathi, moved from difficult-to-parse legacy datasets to **Synthetic Generation** using Groq.
- **Why**: Provided full control over story length, tone, and multi-paragraph formatting required for the chunking pipeline.

### 2. RAG Chunking & Initial Tagging
- **Approach**: Implemented paragraph-based chunking with unique IDs and word counts.
- **Metadata Tagging**: Built the first batch-processing pipeline using Groq for Genre and Scene Type.

## Phase 3 — Production Scale & Retrieval (2026-05-21)
Optimized infrastructure to handle the full 2,654 chunk dataset and enabled semantic search.

### 1. Robust Metadata Pipeline
- **Change**: Implemented **API Key Rotation** (across 5 keys) and 65s rate-limit recovery.
- **Why**: To process thousands of chunks with high-quality 70B models without failing.

### 2. Embedding & Vector Store
- **Model**: Integrated `multilingual-e5-base` with mandatory `passage: ` and `query: ` prefixes.
- **FAISS**: Built an `IndexFlatL2` store, separating large vector artifacts from lightweight metadata.

### 3. Semantic Retriever
- **Completion**: Finalized the retrieval interface, enabling sub-second cross-lingual discovery.
- **Validation**: Confirmed that English queries correctly retrieve relevant emotional or thematic content in Hindi and Marathi.

---

## Phase 4 — Narrative Intelligence (2026-05-21)
Implemented the batch analysis engine to generate structured intelligence for all narrative chunks.

### 1. Local Multilingual Emotion Scorer (`src/features/emotion.py`)
- **What:** Replaced Groq-based emotion analysis with a fully local transformer model (`cardiffnlp/twitter-xlm-roberta-base-sentiment`).
- **Why:** To eliminate API dependencies, costs, and rate limits. Local inference is significantly faster (~60-250ms per chunk) and allows for 100% offline batch processing.
- **Approach:** 
    - Integrated XLM-RoBERTa via the `transformers` library for native English, Hindi, and Marathi support.
    - Mapped model labels (Positive/Negative/Neutral) to the NarrativeIQ polarity/intensity schema.
    - Used model confidence as a proxy for emotional intensity.
- **Result:** Successfully validated with multilingual test cases; zero API latency.

### 2. Full Analysis Pipeline (`src/pipelines/full_analysis_pipeline.py`)
- **What:** The "Main Brain" script that runs the entire analysis stack (Pacing, Repetition, Emotion, Scoring, Feedback).
- **Why:** To create the final intelligence dataset (`full_narrative_analysis.json`) required for the UI and AI critiquing agents.
- **Approach:**
    - Processes all 2,654 story chunks with progress tracking every 25 units.
    - Supports resuming from progress files if interrupted.
    - Captures comprehensive stats (label distribution, average scores).
- **Status:** Verified with a 20-chunk test run (Results: 15 Strong, 5 Moderate; Avg Score: 0.65).

### 3. Full Dataset Analysis Completion
- **What:** Executed the complete analysis pipeline on all 2,654 story chunks using local XLM-RoBERTa and calibrated scoring.
- **Why:** To finalize the intelligence dataset for the future FastAPI/Next.js production system.
- **Results (Final Calibration Audit):**
    - **Strong**: 731 (27.5%) — Properly selective for high-quality narrative.
    - **Moderate**: 1,767 (66.6%) — Correctly captures the majority of average/good writing.
    - **Weak**: 156 (5.9%) — Effectively identifies sections with significant structural or repetitive flaws.
- **Status:** Completed. Final intelligence saved to `data/processed/full_narrative_analysis.json`.

---

# Core Technologies
- **Sentence Transformers**: `multilingual-e5-base`
- **FAISS**: `IndexFlatL2`
- **Groq**: `llama-3.3-70b-versatile` & `llama-3.1-8b-instant`
- **Python Stack**: NumPy, Pickle, NLTK, Scikit-learn
- **Dataset**: TinyStories (English) + Synthetic Indic (Hindi/Marathi)

---

*Current Project State: The multilingual semantic retrieval backbone is fully operational and validated.*
