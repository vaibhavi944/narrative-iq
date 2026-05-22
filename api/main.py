from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

from src.agents.writer_critique_agent import WriterCritiqueAgent

app = FastAPI()

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_agent: Optional[WriterCritiqueAgent] = None


def get_agent() -> WriterCritiqueAgent:
    """
    Lazily initialize the heavy agent so the API can boot cleanly on a VM
    before the first analysis request arrives.
    """
    global _agent
    if _agent is None:
        _agent = WriterCritiqueAgent()
        print("--- NARRATIVE IQ BACKEND ---")
        print(f"Data Loaded: {len(_agent.analysis_data)} narrative chunks")
        print("Status: Operational")
    return _agent

class AnalysisRequest(BaseModel):
    text: str
    language: str

class RewriteRequest(BaseModel):
    text: str
    language: str
    benchmark_text: str
    benchmark_id: str

@app.get("/")
def read_root():
    return {"status": "NarrativeIQ API is active"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        agent = get_agent()
        result = agent.analyze_and_critique(request.text, language=request.language)
        # Ensure we return a successful flat structure for the frontend
        return {
            "success": True,
            "score": result["analysis"]["writing_strength"],
            "label": result["analysis"]["label"],
            "summary": result["feedback"]["summary"],
            "tips": result["feedback"]["tips"],
            "critique": result["agent_critique"],
            "benchmark": {
                "text": result["benchmark_example"]["text"],
                "genre": result["benchmark_example"]["genre"],
                "chunk_id": result["benchmark_example"]["chunk_id"]
            } if result.get("benchmark_example") else None,
            "pacing_score": result["analysis"]["pacing"],
            "repetition_score": result["analysis"]["repetition"],
            "emotion_score": result["analysis"]["emotion"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/rewrite")
async def rewrite(request: RewriteRequest):
    try:
        agent = get_agent()
        benchmark = {"text": request.benchmark_text, "chunk_id": request.benchmark_id}
        result = agent.generate_rewrite(
            request.text,
            benchmark,
            language=request.language
        )
        return {"success": True, "rewrite": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
