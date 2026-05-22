# Project Log - Narrative IQ

This file tracks the engineering decisions, architectural changes, and implementation steps for the Narrative IQ project. It serves as the single source of truth for the project's development history.

## Phase 1 — Data Ingestion & Metadata Pipeline (2026-05-18)
Established the foundation for a multilingual developmental editor.
- **Datasets**: Downloaded **TinyStories** (English) for high-quality baseline prose and generated **Synthetic Indic Stories** (Hindi/Marathi) using Llama 3.3.
- **Processing**: Built a metadata extraction pipeline (`src/ingestion/metadata_pipeline.py`) that extracts word counts, scene types (Action, Dialogue, etc.), and emotional markers.

## Phase 2 — Feature Engineering & Semantic Scorer (2026-05-19)
Developed the "eyes" of the editor.
- **Pacing**: Algorithmic detection of sentence length variance to identify "staccato" vs "monotonous" flow.
- **Repetition**: Vocabulary richness analysis using Type-Token Ratio (TTR).
- **Emotion**: Local pipeline using `distilbert-base-uncased-emotion` to detect emotional depth and variety.
- **Unified Scorer**: Combined these signals into a 0.0-1.0 "Writing Strength" score.

## Phase 3 — Multilingual RAG & Vector Store (2026-05-20)
Created the semantic memory to enable comparative reasoning.
- **Embeddings**: Used `multilingual-e5-base` to project English, Hindi, and Marathi into the same vector space.
- **Vector Store**: Implemented **FAISS** (`IndexFlatL2`) for ultra-fast semantic retrieval of "Strong" literary benchmarks.
- **Chunking**: Developed a language-aware `text_splitter.py` to preserve narrative units across different scripts.

## Phase 4 — AI Editorial Agent (2026-05-21)
Shifted from preprocessing to building the core reasoning layer of NarrativeIQ.
- **Master Agent**: Built `WriterCritiqueAgent` using **Groq (Llama 3.3 70B)** and **Gemini 1.5 Pro** as a fallback.
- **Editorial Logic**: 
    - **Contextual Retrieval:** Pulls the top literary benchmark for the user's specific scene type.
    - **Comparative Reasoning:** Uses **Llama 3.3 70B** to compare the user text with the benchmark, explaining technical differences and providing actionable transformation steps.
- **Result:** Successfully validated across 8 diverse test cases (Repetitive, Action, Dialogue, Multilingual). Demonstrated high-quality reasoning and semantic bridge-building between languages.

## Phase 5 — Quality-Aware Retrieval & Reranking (2026-05-21)
- **What:** Upgraded the retrieval engine from simple semantic similarity to a two-stage "Quality-Aware" process.
- **Why:** To ensure the critique agent always compares user prose against the highest-quality literary benchmarks, rather than just semantically similar but average writing.
- **Approach:** 
    - **Stage 1:** Retrieve top 50 semantically similar candidates.
    - **Stage 2:** Apply a custom scoring function: `Score = (0.7 * similarity) + (0.3 * writing_strength)`.
        - **Style Alignment (Bonus):** Extra points for matching Genre or Scene Type.
- **Result:** Successfully validated; basic retrieval's "Moderate" benchmarks were replaced by verified "Strong" benchmarks in 100% of test cases while maintaining thematic relevance.

## Phase 6 — Quality Stabilization & Localization (2026-05-22)
Focused on refining the user experience, ensuring 100% multilingual integrity, and hardening the RAG-driven feedback loop.

### 1. UI Persistence & Session State
- **Failure:** The "Suggested Rewrite" button and results would disappear immediately after clicking. This occurred because Streamlit reruns the script on every interaction, losing temporary local variables.
- **Fix:** Refactored `app.py` to use `st.session_state`. 
    - All analysis results, input parameters, and rewrite outputs are now stored in the session.
    - Results are displayed outside the "Analyze" button block, ensuring they remain visible even when secondary buttons (like Rewrite) are clicked.
    - Implemented `st.session_state.rewrite_result = ""` at the start of new analyses to prevent stale results from persisting across different texts.

### 2. Eliminating Language Mixing
- **Failure:** Even when Hindi or Marathi was selected, the AI would return headers (e.g., "Actionable Steps") or benchmark critiques in English. The "Delta" labels (Strong/Moderate/Weak) were also stuck in English.
- **Fix (Prompt Engineering):** Upgraded `WriterCritiqueAgent` with an aggressive "Zero-Tolerance" prompt.
    - Explicit instructions: "YOUR ENTIRE RESPONSE MUST BE IN [LANGUAGE]. DO NOT USE ANY ENGLISH. FAILURE TO COMPLY WILL RESULT IN SYSTEM ERROR."
    - Dynamic language instructions: Added specific requirements for "Hindi Devanagari script" and "Marathi Devanagari script" to prevent the model from using Romanized text.
- **Fix (UI/Logic Localization):** 
    - Created `src/utils/language_utils.py` to hardcode all UI strings (headers, metrics, button labels).
    - Updated `feedback_generator.py` to localize the qualitative labels (e.g., "Strong" -> "मजबूत" / "मजबूत").
    - Ensured the `language` parameter is passed through every layer (Agent -> Scorer -> Feedback Gen).

### 3. RAG Benchmark Integrity
- **Failure:** Hindi/Marathi queries often returned English benchmarks. This happened because English stories (2,400+) vastly outnumbered Indic stories (96), dominating the semantic vector space. Some benchmarks also returned "corrupted" text containing Russian or Chinese characters.
- **Fix (Filtering):** 
    - Increased retrieval `top_k` from 20 to 50 to cast a wider net for minority languages.
    - Implemented a **Hard Language Filter** in `WriterCritiqueAgent`: any benchmark not matching the user's selected language is rejected.
- **Fix (Quality Validation):** 
    - Added `_is_valid_chunk()` to the agent.
    - **Length Check:** Minimum 50 characters to avoid useless fragments.
    - **Script Check:** Regex filter to reject Cyrillic (Russian) or CJK (Chinese/Japanese/Korean) characters which indicated corrupted synthetic data.
- **Fix (Emergency Fallback):** If no valid benchmark is found in the target language within the search results, the system now scans the entire `analysis_data` for the **highest-scoring valid Strong chunk** in that language as a safety measure.

### 4. Data Cleanup
- **Issue:** `story_050.txt` in the Hindi dataset was identified as corrupted during manual testing.
- **Fix:** Deleted the corrupted file and regenerated a fresh 3-paragraph Hindi story using a specialized Groq prompt to ensure pure Devanagari script.

## Phase 7 — Permanent Data Purge (2026-05-22)
Applied a permanent fix for corrupted Marathi chunks that were bypassing semantic filters.

### 1. Hardcoded Blocklist & Strict Validation
- **Failure:** Specific corrupted chunks (e.g., `mar_021_02`) continued to appear as benchmarks despite previous regex filters.
- **Fix (Agent Logic):** 
    - Added `BLOCKED_CHUNK_IDS` set to `WriterCritiqueAgent` to explicitly reject known bad IDs.
    - Enhanced `_is_valid_chunk()` with stricter criteria:
        - Minimum length increased to 80 characters.
        - Mandatory check for at least 2 sentences (using `re.split(r'[.।?!]')`).
        - Minimum word count of 15.
- **Fix (Data Purge):** Physically deleted entries `mar_021_01`, `mar_021_02`, and `mar_021_03` from both `full_narrative_analysis.json` and `tagged_chunks_final.json`. This ensures they can never be loaded into memory or retrieved.

## Phase 8 — Production Readiness & UI Overhaul (2026-05-22)
Transformed NarrativeIQ from an experimental tool into a professional, stable, and visually sophisticated "Multilingual Developmental Editor."

### 1. "Quiet Luxury" Aesthetic Overhaul
- **Objective:** Move beyond generic UI to a premium, editorial-grade design.
- **Visuals:** Implemented a minimalist off-white palette (`#fafaf8`) with high-contrast charcoal (`#1a1a18`) and unified Indigo (`#4338ca`) accents.
- **Typography:** 
    - **English:** Switched to `Newsreader` (Serif) for a classic literary feel and `Geist` (Sans) for crisp UI elements.
    - **Indic (Hindi/Marathi):** Switched to `Mukta` for UI and ensured naturally joined ligatures by disabling Latin-style letter-spacing.

### 2. Hardened AI Grounding & Reliability
- **Hallucination Ban:** Re-engineered `WriterCritiqueAgent` prompts with "Strict Grounding Rules" to prevent the AI from inventing new plot points or characters.
- **Structured Feedback:** Redesigned the "Editor's Note" to present critiques as a professional, 3-point rubric (Density, Flow, Emotion), automatically formatted into a clear list.
- **Zero-Tolerance Language Locking:** Reinforced script-consistency across all three languages, ensuring 100% native rendering in all critiques and rewrites.

### 3. Workspace UX Refinements
- **Resizable Side Panel:** Implemented a custom interactive resizer, allowing writers to adjust the editorial panel width for better focus.
- **Clean Editor:** Fixed a jarring "black box" focus ring issue in the textarea, providing a distraction-free writing environment.
- **High-Impact Dashboard:** Overhauled the `ScoreCard` component with a high-contrast luxury dashboard feel, featuring massive scores and professional metrics.

### 4. Deployment Stability & Data Integrity
- **Production Structure:** Standardized backend logging and ensured all frontend components pass full production builds (`npm run build`).
- **Data Pruning:** Updated `.gitignore` to exclude large raw/processed story data, keeping the repository lean and focused on code.
- **Mobile Safety:** Optimized padding and responsive layouts to ensure a professional experience on all device sizes.

---

# Core Technologies

- **UI Framework**: Next.js 15+ (React 19)
- **Backend API**: FastAPI
- **Sentence Transformers**: `multilingual-e5-base`
- **FAISS**: `IndexFlatL2`
- **Groq**: `llama-3.3-70b-versatile` (Master Editor / Rewriter)
- **Google AI**: `gemini-1.5-pro` (Reasoning Fallback)
- **Python Stack**: NumPy, Pickle, NLTK, Regex
- **Primary Fonts**: Newsreader (English Serif), Geist (English Sans), Mukta (Devanagari)

---

*Current Project State: The system is now UI-stable, language-consistent, and data-validated across all three supported languages. Ready for deployment testing.*
