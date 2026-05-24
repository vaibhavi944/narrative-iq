# Narrative-IQ: The Multilingual Developmental Editor

**Narrative-IQ** is a sophisticated AI-powered developmental editor designed specifically for fiction writers. Unlike generic AI writing assistants, Narrative-IQ uses **Retrieval-Augmented Generation (RAG)** and **Comparative Reasoning** to help writers elevate their prose across **English, Hindi, and Marathi**.

It doesn't just "fix" your writing; it acts as a mentor by comparing your work against thousands of high-quality literary benchmarks and providing specific, actionable editorial insights.

---

## 🌟 The Vision: "Show, Don't Just Tell"
Narrative-IQ was born from the need for an editor that understands the rhythm of storytelling. It focuses on three core pillars:
1.  **Multilingual Depth:** Native understanding of English, Hindi, and Marathi scripts and styles.
2.  **RAG-Driven Mentorship:** Comparative feedback based on a curated database of 2,600+ story chunks.
3.  **Quiet Luxury UX:** A minimalist, distraction-free environment that puts the focus back on the manuscript.

---

## 🚀 Key Features

### 1. Deep Narrative Analysis
The system evaluates your prose through three distinct technical lenses:
*   **Pacing & Rhythm:** Analyzes sentence length variance to detect staccato or monotonous flow.
*   **Vocabulary Richness:** Uses Type-Token Ratio (TTR) to identify repetitive wording.
*   **Emotional Resonance:** Employs a local NLP pipeline to map the emotional depth and variety of the scene.

### 2. The "Mentor" (Comparative RAG)
This is the heart of Narrative-IQ. When you analyze a text:
1.  **Semantic Search:** It uses the `multilingual-e5-base` model to find the most semantically similar "Strong" benchmark in our database.
2.  **Benchmark Comparison:** It displays a high-quality reference scene side-by-side with your writing.
3.  **Editor's Note:** Using **Llama 3.3 70B**, it generates a professional 3-point critique (Density, Flow, Emotion) explaining exactly why the benchmark is stronger.

### 3. High-Fidelity Rewrites
The "Show Better Version" feature doesn't just "clean up" text. It uses the benchmark's style to **elevate** your prose—adding sensory nuance, transforming "telling" into "showing," and improving rhythmic flow while strictly preserving your original plot and characters.

---

## 🛠️ The Technical Journey (How She Built It)

This project was developed through an intensive 8-phase engineering cycle:

*   **Phase 1-2 (The Foundation):** Ingested TinyStories (English) and generated synthetic Indic stories (Hindi/Marathi) using Groq. Built the core feature extraction algorithms.
*   **Phase 3-4 (The Brain):** Implemented a **FAISS Vector Store** for ultra-fast retrieval and developed the `WriterCritiqueAgent` to orchestrate analysis and comparative reasoning.
*   **Phase 5 (The Quality Filter):** Upgraded to a "Quality-Aware" retrieval system, ensuring users are always compared against **verified Strong** benchmarks.
*   **Phase 6-7 (The Polish):** Solved complex "Language Mixing" issues, ensuring 100% native Devanagari script for Hindi/Marathi critiques. Purged corrupted data to ensure 100% benchmark integrity.
*   **Phase 8 (The Overhaul):** Transformed the UI into a "Quiet Luxury" aesthetic using a minimalist palette and premium typography (Newsreader, Geist, and Mukta).

---

## 💻 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python 3.10+ |
| **AI Models** | Groq (Llama 3.3 70B), Sentence Transformers (`multilingual-e5-base`) |
| **Vector DB** | FAISS (IndexFlatL2) |
| **Data Processing** | NumPy, Pickle, NLTK, Regex |
| **UI Design** | "Quiet Luxury" palette, Serif-first typography |

---

## ⚙️ Setup & Installation

### Backend Setup
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/vaibhavi944/narrative-iq.git
    cd narrative-iq
    ```
2.  **Environment:** Create a virtual environment and install requirements.
    ```bash
    python -m venv venv
    ./venv/Scripts/activate
    pip install -r requirements.txt
    ```
3.  **Secrets:** Add your `GROQ_API_KEY` to a `.env` file.
4.  **Run API:**
    ```bash
    uvicorn api.main:app --host 127.0.0.1 --port 8000
    ```

### Frontend Setup
1.  **Navigate to directory:** `cd frontend`
2.  **Install:** `npm install`
3.  **Run:** `npm run dev`
4.  **Access:** Open [http://localhost:3000](http://localhost:3000)

---

## 🎨 Design Philosophy: "Quiet Luxury"
Narrative-IQ uses a carefully curated visual language:
*   **Palette:** Off-white surfaces (`#fafaf8`) with Charcoal text (`#1a1a18`) and Indigo accents (`#4338ca`).
*   **Typography:** **Newsreader** for a classic book-like feel, **Geist** for crisp metadata, and **Mukta** for natural Devanagari ligatures.
*   **Focus:** A "Zen" editor mode that hides complexity until you ask for an editorial review.

---

**Narrative-IQ** — *Elevating the world's stories, one language at a time.*
