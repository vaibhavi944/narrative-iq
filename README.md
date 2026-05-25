# NarrativeIQ

NarrativeIQ is a creative writing analysis tool that provides comparative critique and rewrites for stories in English, Hindi, and Marathi.

Writing narrative prose is challenging because it requires balancing pacing, emotional depth, and vocabulary variety. NarrativeIQ solves this by providing literary-focused analysis rather than just basic grammar and spelling corrections. It identifies weaknesses in specific paragraphs and retrieves high-quality "Strong" benchmarks from its vector database to show how professional writers handle similar scenes. The output includes numerical scores for pacing, repetition, and emotion, along with human-readable tips and a language-matched rewrite of the user's text.

## Architecture

The system combines rule-based NLP heuristics with RAG-powered retrieval and LLM reasoning. Each layer has a specific job and can be understood and defended independently.

```
User Input (English / Hindi / Marathi)
         |
         v
Paragraph Splitter (text_splitter.py)
         |
         v
Feature Extraction
+------------------+------------------+------------------+
| Pacing Analyzer  | Repetition Detector| Emotion Scorer  |
| sentence length  | starters, words,  | Groq API for    |
| + variance       | bigrams           | all 3 languages  |
+------------------+------------------+------------------+
         |
         v
Weakness Scorer (language-aware weighted combination)
Strong >= 0.60 | Moderate >= 0.40 | Weak < 0.40
         |
         v
RAG Retrieval (FAISS top-50 -> Strong filter -> quality check)
         |
         v
LLM Agent (Groq llama-3.3-70b-versatile)
Comparative critique + Language-matched rewrite
         |
         v
FastAPI Response / Next.js UI
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| NLP Heuristics | Custom Python, nltk, regex | Explainable signals, consistent across runs |
| Emotion Scoring | Groq API (llama-3.3-70b) | Understands literary subtext, not keyword matching |
| Embeddings | intfloat/multilingual-e5-base | Single model for all 3 languages |
| Vector Store | FAISS IndexFlatL2 | Exact search, no cloud dependency |
| API Layer | FastAPI | Async, lightweight, easy to extend |
| UI | Next.js (React) | Modern, responsive, and production-ready |

## Key Design Decisions

### Why custom heuristics instead of asking an LLM to score everything

Heuristics give measurable explainable numbers. Pacing score comes from avg sentence length and variance. Repetition score from counter-based detection. These are defensible in an interview. LLM-only scoring is a black box with inconsistent outputs across runs.

### Why Groq for emotion scoring instead of TextBlob

TextBlob assigns polarity based on word lists. It does not understand literary language. Example: "She felt something loosen in her chest" scores near zero on TextBlob because none of those words are in its sentiment lexicon. Groq understands the literary meaning and scores it correctly.

### Why language-aware weights in the scorer

Hindi and Marathi literary prose uses more emotionally expressive language by default. Without adjusted weights, nearly all Hindi and Marathi paragraphs scored Strong on emotion even when pacing and repetition were weak. Separate weights: English pacing 0.40, Hindi/Marathi pacing 0.45.

### Why two-stage benchmark retrieval

Semantic similarity alone finds similar scenes but not necessarily strong writing. System retrieves top 50 semantically similar chunks then filters for Strong label, correct language, and passes a quality validation check. This ensures the benchmark is always better than the user input.

### Why FAISS over a managed vector database

The dataset is 2651 chunks. FAISS IndexFlatL2 gives exact search results with zero cloud dependency, no API costs, and fast local inference. A managed vector DB adds infrastructure complexity for no benefit at this scale.

## Data Pipeline

Run once to build the system. After the pipeline completes, the app loads the pre-built index and analysis database at startup.

1. Download and generate raw stories
```bash
python -m src.ingestion.download_datasets
```
Downloads 500 English stories from HuggingFace TinyStories. Generates 50 Hindi and 40 Marathi stories via Groq API. Saves as .txt files in data/raw_stories/

2. Chunk stories into paragraphs
```bash
python -m src.rag.chunking
```
Splits each story on double newlines. Creates 2654 chunks with chunk_id, text, language, word_count.

3. Tag chunks with metadata
```bash
python -m src.ingestion.metadata_pipeline
```
Rule-based tagging for genre, scene_type, dialogue_density. No API calls. Keyword rules only. Runs in seconds.

4. Generate embeddings
```bash
python -m src.rag.embeddings
```
Uses intfloat/multilingual-e5-base. Prepends "passage: " to each chunk (E5 model requirement). Saves to data/processed/embedded_chunks.pkl

5. Build FAISS index
```bash
python -m src.rag.vector_store
```
Creates IndexFlatL2 from embeddings. Saves narrative_index.faiss and chunk_metadata.pkl

6. Score all chunks
```bash
python -m src.pipelines.full_analysis_pipeline
```
Runs all chunks through pacing, repetition, emotion scoring. Labels each chunk Strong, Moderate, or Weak. Saves full_narrative_analysis.json. Agent uses this file to filter for Strong benchmark chunks.

## Dataset Statistics

| Language | Total Chunks | Strong | Moderate | Weak |
|---|---|---|---|---|
| English | 2408 | 672 | 1608 | 128 |
| Hindi | 150 | 31 | 105 | 14 |
| Marathi | 93 | 28 | 54 | 11 |
| Total | 2651 | 731 | 1767 | 153 |

## Setup and Running

```bash
# Create environment
conda create -n narrativeiq_env python=3.11
conda activate narrativeiq_env
pip install -r requirements.txt
python -m nltk.downloader punkt

# Add API keys
cp .env.example .env
# Edit .env and add your Groq API keys

# Build data pipeline (first time only, takes 20-30 minutes)
python -m src.ingestion.download_datasets
python -m src.rag.chunking
python -m src.ingestion.metadata_pipeline
python -m src.rag.embeddings
python -m src.rag.vector_store
python -m src.pipelines.full_analysis_pipeline

# Run FastAPI backend
uvicorn api.main:app --reload --port 8000

# Run Next.js UI (in frontend directory)
cd frontend
npm install
npm run dev
```

## Project Structure

```
narrativeiq/
├── api/
│   └── main.py                         # FastAPI endpoints
├── frontend/                           # Next.js React application
│   ├── app/                            # Pages and routing
│   ├── components/                     # Reusable UI components
│   └── package.json
├── src/
│   ├── agents/
│   │   └── writer_critique_agent.py    # RAG + LLM orchestration
│   ├── features/
│   │   ├── pacing.py                   # Sentence length and variance
│   │   ├── repetition.py               # Repeated words and bigrams
│   │   └── emotion.py                  # Groq-based emotion scoring
│   ├── ingestion/
│   │   ├── download_datasets.py        # Data download and generation
│   │   └── metadata_pipeline.py        # Rule-based chunk tagging
│   ├── pipelines/
│   │   └── full_analysis_pipeline.py   # Batch chunk scoring
│   ├── rag/
│   │   ├── chunking.py                 # Story to paragraph chunks
│   │   ├── embeddings.py               # E5 embedding generation
│   │   ├── retriever.py                # FAISS semantic search
│   │   └── vector_store.py             # FAISS index management
│   ├── scoring/
│   │   ├── weakness_scorer.py          # Weighted score combination
│   │   └── feedback_generator.py       # Scores to plain language tips
│   └── utils/
│       ├── text_splitter.py            # Chapter to paragraphs
│       └── language_utils.py           # UI translation strings
├── tests/
│   └── test_pipeline.py                # End to end pipeline test
├── docs/
│   └── PROJECT_LOG.md                  # Full development log
├── requirements.txt
└── .env.example
```

## Requirements

See requirements.txt for full list.

- groq
- faiss-cpu
- sentence-transformers
- nltk
- fastapi
- uvicorn
- datasets
- python-dotenv
