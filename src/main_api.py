import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from src.agents.writer_critique_agent import WriterCritiqueAgent
from src.scoring.weakness_scorer import score_paragraph

# =========================================================
# NarrativeIQ - API Backend
# =========================================================
# Purpose:
# Serves the intelligence layer (Analysis, Retrieval, Critique)
# via high-performance FastAPI endpoints.
# =========================================================

app = FastAPI(
    title="NarrativeIQ API",
    description="Intelligent AI Writing Mentor Backend",
    version="1.0.0"
)

# ---------------------------------------------------------
# Step 1: Middleware Configuration (CORS)
# ---------------------------------------------------------
# Required for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Step 2: Global Resource Management
# ---------------------------------------------------------
# Initialize the agent once to avoid reloading models/FAISS on every request
print("Initializing NarrativeIQ Intelligence Backend...")
agent = WriterCritiqueAgent()

# ---------------------------------------------------------
# Step 3: Request/Response Schemas
# ---------------------------------------------------------
class AnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = "english"

# ---------------------------------------------------------
# Step 4: Endpoints
# ---------------------------------------------------------

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """
    Performs raw narrative analysis (pacing, repetition, emotion).
    """
    try:
        result = score_paragraph(request.text, language=request.language)
        return result
    except Exception as e:
        print(f"API Analyze Error: {e}")
        raise HTTPException(status_code=500, detail="Internal analysis failure.")

@app.post("/critique")
async def get_full_critique(request: AnalysisRequest):
    """
    Performs full orchestration: Analysis -> Retrieval -> Critique -> Rewrite.
    """
    try:
        result = agent.analyze_and_critique(request.text, language=request.language)
        return result
    except Exception as e:
        print(f"API Critique Error: {e}")
        raise HTTPException(status_code=500, detail="Internal critique generation failure.")

@app.get("/health")
async def health_check():
    """
    Basic service health check.
    """
    return {
        "status": "active",
        "service": "NarrativeIQ Backend",
        "models": ["multilingual-e5-base", "xlm-roberta-sentiment"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
