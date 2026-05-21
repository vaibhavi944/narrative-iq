import os
import json
import time
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv
from src.scoring.weakness_scorer import score_paragraph
from src.scoring.feedback_generator import generate_feedback
from src.rag.retriever import retrieve_similar_chunks

# Load environment variables
load_dotenv(override=True)

# =========================================================
# NarrativeIQ - Writer Critique Agent
# =========================================================
# Purpose:
# Orchestrates analysis, retrieval, and comparative reasoning.
# Supports multi-provider fallback (Groq + Google Gemini).
# =========================================================

class WriterCritiqueAgent:
    """
    Agent that analyzes user prose and provides feedback based on
    semantically similar high-quality examples.
    """
    
    def __init__(self):
        # 1. Groq Keys
        self.groq_keys = []
        for i in range(1, 6):
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key: self.groq_keys.append(key)
        if not self.groq_keys and os.getenv("GROQ_API_KEY"):
            self.groq_keys.append(os.getenv("GROQ_API_KEY"))
            
        self.current_groq_index = 0
        self.groq_model = "llama-3.3-70b-versatile"
        
        # 2. Gemini Key
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                print("Gemini model configured successfully.")
            except Exception as e:
                print(f"Error configuring Gemini: {e}")
                self.gemini_model = None
        else:
            self.gemini_model = None

        if not self.groq_keys and not self.gemini_model:
            raise ValueError("No reasoning API keys (Groq or Gemini) found in .env")

        # 3. Reference Data Cache
        self.analysis_db_path = "data/processed/full_narrative_analysis.json"
        self._analysis_data = None

    @property
    def analysis_data(self):
        if self._analysis_data is None:
            if os.path.exists(self.analysis_db_path):
                try:
                    with open(self.analysis_db_path, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)
                        self._analysis_data = {item["chunk_id"]: item for item in raw_data}
                except Exception as e:
                    print(f"Error loading analysis database: {e}")
                    self._analysis_data = {}
            else:
                self._analysis_data = {}
        return self._analysis_data

    def _normalize_chunk(self, chunk):
        """
        Guarantees a safe and consistent dictionary structure for narrative chunks.
        Prevents KeyErrors during reasoning and retrieval.
        """
        return {
            "chunk_id": chunk.get("chunk_id", "unknown"),
            "text": chunk.get("text", ""),
            "label": chunk.get("label", "Unknown"),
            "reasons": chunk.get("reasons", []),
            "feedback": chunk.get("feedback", {}),
            "combined_score": chunk.get("combined_score", 0.0),
            "language": chunk.get("language", "unknown"),
            "genre": chunk.get("genre", "unknown"),
            "scene_type": chunk.get("scene_type", "unknown")
        }

    def _call_groq(self, prompt):
        """Internal helper for Groq with rotation."""
        if not self.groq_keys: return None
        
        attempts = 0
        # Try each key once
        while attempts < len(self.groq_keys):
            try:
                client = Groq(api_key=self.groq_keys[self.current_groq_index])
                completion = client.chat.completions.create(
                    model=self.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                if "429" in str(e):
                    print(f"Groq Key {self.current_groq_index + 1} limited. Rotating...")
                    self.current_groq_index = (self.current_groq_index + 1) % len(self.groq_keys)
                else:
                    print(f"Groq non-rate-limit error: {e}")
                    break
            attempts += 1
        return None

    def _call_gemini(self, prompt):
        """Internal helper for Gemini."""
        if not self.gemini_model: return None
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini reasoning error: {e}")
            return None

    def _get_strong_example(self, query_text, top_k=10):
        try:
            results = retrieve_similar_chunks(query_text, top_k=top_k)
            if not results: return None
            
            for res in results:
                cid = res.get("chunk_id")
                if cid in self.analysis_data and self.analysis_data[cid].get("label") == "Strong":
                    return self._normalize_chunk(self.analysis_data[cid])
            
            # Fallback: normalize the first raw result
            return self._normalize_chunk(results[0])
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None

    def analyze_and_critique(self, text, language="english"):
        if not text or not text.strip():
            return {"error": "No text provided", "agent_critique": "Please provide text."}

        # 1. Analysis
        score_result = score_paragraph(text, language=language)
        feedback = generate_feedback(score_result)
        
        # 2. Retrieval
        benchmark = self._get_strong_example(text)
        
        # 3. Reasoning (Try Groq first, then Gemini)
        prompt = self._build_critique_prompt(text, score_result, benchmark)
        
        critique = self._call_groq(prompt)
        if not critique:
            print("Groq exhausted or failed. Attempting Gemini fallback...")
            critique = self._call_gemini(prompt)
            
        if not critique:
            critique = "Critique generation currently unavailable due to provider limits. Local analysis suggests your prose is: " + score_result.get('label', 'Moderate')

        return {
            "analysis": score_result,
            "feedback": feedback,
            "benchmark_example": benchmark,
            "agent_critique": critique
        }

    def _build_critique_prompt(self, user_text, user_score, benchmark):
        bench_text = benchmark.get('text', '') if benchmark else "N/A"
        bench_reasons = ', '.join(benchmark.get('reasons', [])) if benchmark and benchmark.get('reasons') else "Strong narrative rhythm"
        user_reasons = ', '.join(user_score.get('reasons', [])) if user_score.get('reasons') else 'No major issues'
        
        return f"""You are a master literary editor. 
Compare the USER'S PARAGRAPH with the BENCHMARK PARAGRAPH.

USER'S PARAGRAPH:
"{user_text}"
- Detected Issues: {user_reasons}

BENCHMARK PARAGRAPH:
"{bench_text}"
- Why it is Strong: {bench_reasons}

TASK:
1. Explain specifically what the BENCHMARK does better in terms of craft.
2. Provide 2-3 specific, actionable steps for the user to improve.
Return clean, structured text only. No preamble."""

if __name__ == "__main__":
    agent = WriterCritiqueAgent()
    test_input = "He went to the forest. He saw a bear. The bear was big. He was scared."
    print(f"\nTesting Critique Agent with input: {test_input}")
    res = agent.analyze_and_critique(test_input)
    print(f"\nCritique Output:\n{res['agent_critique']}")
