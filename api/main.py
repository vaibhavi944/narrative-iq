from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

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

agent = WriterCritiqueAgent()

# Health check to ensure data is loaded on startup
print(f"--- NARRATIVE IQ BACKEND ---")
print(f"Data Loaded: {len(agent.analysis_data)} narrative chunks")
print(f"Status: Operational")

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

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        result = agent.analyze_and_critique(request.text, language=request.language)
        # Ensure we return a successful flat structure for the frontend
        return {
            "success": True,
            "score": result["analysis"]["combined_score"],
            "label": result["analysis"]["label"],
            "summary": result["feedback"]["summary"],
            "tips": result["feedback"]["tips"],
            "critique": result["agent_critique"],
            "benchmark": {
                "text": result["benchmark_example"]["text"],
                "genre": result["benchmark_example"]["genre"],
                "chunk_id": result["benchmark_example"]["chunk_id"]
            } if result.get("benchmark_example") else None,
            "pacing_score": result["analysis"]["pacing"]["pacing_score"],
            "repetition_score": result["analysis"]["repetition"]["repetition_score"],
            "emotion_score": result["analysis"]["emotion"]["emotion_score"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/rewrite")
async def rewrite(request: RewriteRequest):
    try:
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
