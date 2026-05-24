# Narrative-IQ: Multilingual RAG-Driven Editorial Engine

**Narrative-IQ** is a specialized narrative analysis and editorial system designed to provide deep, context-aware critiques for fiction writing. The core of the project is a sophisticated **Retrieval-Augmented Generation (RAG)** engine that understands narrative structure across **English, Hindi, and Marathi**.

The system moves beyond simple grammar checking, employing semantic benchmarking to evaluate prose quality against verified high-quality literary datasets.

---

## ⚙️ Core Architecture: The Editorial Engine

### 1. Narrative Intelligence & Scoring
The engine processes raw text through a series of specialized feature extraction pipelines:
*   **Pacing & Rhythm Logic:** Algorithmic analysis of sentence length variance to identify stylistic patterns (staccato, monotonous, or fluid).
*   **Vocabulary & Density:** Measures Type-Token Ratio (TTR) and word variety to detect narrative friction and repetition.
*   **Multilingual Emotion Pipeline:** A localized NLP system that maps emotional arcs and sentiment depth, calibrated specifically for each target language.

### 2. Semantic RAG & Benchmarking
The system's reasoning is grounded in a curated database of over 2,600 narrative chunks.
*   **Vectorization:** Uses `multilingual-e5-base` to project multi-language prose into a unified semantic space.
*   **Quality-Aware Retrieval:** A two-stage retrieval process that identifies the most semantically similar "Strong" benchmark for any given user scene.
*   **Comparative Reasoning:** Powered by **Llama 3.3 70B**, the engine performs a side-by-side analysis, identifying the "density gap" between the user's prose and professional benchmarks.

---

## 🛠️ Technical Engineering Lifecycle

The development of the engine followed a rigorous 8-phase implementation cycle:

*   **Data Ingestion & Synthesis:** Curated the TinyStories dataset for English and generated high-quality synthetic benchmarks for Hindi and Marathi using Groq, ensuring a balanced multilingual foundation.
*   **Semantic Memory Construction:** Built the vector store using **FAISS** (`IndexFlatL2`) and implemented a custom chunking strategy to maintain narrative integrity across different scripts.
*   **Intelligence Layer:** Developed the `WriterCritiqueAgent` with a zero-tolerance language-locking prompt architecture to ensure 100% native output for Indic languages.
*   **Optimization:** Implemented a re-ranking layer that prioritizes "Strong" benchmarks even when "Moderate" results are semantically closer, ensuring a high-quality feedback loop.

---

## 📂 Project Structure (Core Engine)

```bash
narrative-iq/
├── api/
│   └── main.py                 # FastAPI endpoints & Request Orchestration
├── data/
│   └── processed/              # FAISS Index, Metadata, & Analysis Database
├── src/
│   ├── agents/
│   │   └── writer_critique_agent.py # Master AI reasoning & RAG coordination
│   ├── rag/
│   │   ├── embeddings.py       # E5 Vector generation pipeline
│   │   ├── retriever.py        # Quality-aware search logic
│   │   └── vector_store.py     # FAISS management
│   ├── scoring/
│   │   ├── weakness_scorer.py  # Multi-feature aggregation logic
│   │   └── feedback_generator.py # Localized qualitative analysis
│   ├── features/
│   │   ├── pacing.py           # Rhythm & Variance analysis
│   │   ├── repetition.py       # TTR & Vocabulary richness
│   │   └── emotion.py          # Multilingual sentiment pipeline
│   ├── pipelines/
│   │   └── full_analysis_pipeline.py # Batch processing for intelligence DB
│   └── utils/
│       └── text_splitter.py    # Script-aware narrative chunking
└── PROJECT_LOG.md              # Detailed engineering history
```

---

## 🚀 System Setup

### Backend & Engine
1.  **Environment Preparation:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Model Loading & Indexing:**
    The system requires the FAISS index and analysis database to be present in `data/processed/`.
3.  **API Execution:**
    ```bash
    uvicorn api.main:app --host 127.0.0.1 --port 8000
    ```

### Tech Stack Highlights
*   **Inference:** Groq (Llama 3.3 70B) for high-speed narrative reasoning.
*   **Embeddings:** `multilingual-e5-base` for cross-language semantic bridge-building.
*   **Vector DB:** FAISS (Facebook AI Similarity Search).
*   **Language Support:** English (Standard), Hindi (Devanagari), Marathi (Devanagari).

---

**Narrative-IQ** — *Advanced Multilingual Narrative Analysis*
