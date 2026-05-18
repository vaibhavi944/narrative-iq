# Narrative-IQ

Narrative-IQ is a multilingual AI narrative analysis system designed for fiction writers. It provides deep insights into story structure, pacing, emotional resonance, and stylistic patterns across English, Hindi, and Marathi.

## Overview

Writing compelling fiction requires balancing multiple elements like pacing, dialogue, and emotional arc. Narrative-IQ leverages advanced NLP and RAG (Retrieval-Augmented Generation) to help writers analyze their work and receive actionable feedback.

## Planned Features

- **Multilingual Support:** Native analysis for English, Hindi, and Marathi.
- **Narrative Analysis:** Pacing detection, repetition analysis, and emotional arc mapping.
- **AI-Powered Suggestions:** Rewrite suggestions and stylistic improvements using LangChain & LangGraph.
- **Interactive UI:** Heatmaps and feedback cards for visual story analysis.
- **RAG Integration:** Context-aware retrieval for consistent story world-building.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vaibhavi944/narrative-iq.git
   cd narrative-iq
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Future Roadmap

- [ ] Core ingestion pipeline setup
- [ ] Multilingual feature extraction (Pacing, Emotion)
- [ ] RAG implementation for story context
- [ ] LangGraph orchestration for complex workflows
- [ ] Streamlit Dashboard development
