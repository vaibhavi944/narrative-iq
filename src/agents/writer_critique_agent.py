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

    def _get_strong_example(self, query_text, user_metadata=None, top_k=15):
        """
        Retrieves the most semantically AND stylistically similar 'Strong' example.
        """
        # 1. Get reranked similar chunks (now passes user metadata for better alignment)
        try:
            results = retrieve_similar_chunks(query_text, top_k=top_k, user_metadata=user_metadata)
            if not results: return None
            
            # 2. Prefer the highest-ranked 'Strong' result
            for res in results:
                if res.get("quality_label") == "Strong":
                    return self._normalize_chunk(res)
            
            # Fallback: return the best stylistic match even if not 'Strong'
            return self._normalize_chunk(results[0])
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None

    def analyze_and_critique(self, text, language="english"):
        if not text or not text.strip():
            return {"error": "No text provided", "agent_critique": "Please provide text."}

        # 1. Analysis (Heuristics)
        score_result = score_paragraph(text, language=language)
        feedback = generate_feedback(score_result)
        
        # 2. Qualitative Style Detection (Enhanced for better alignment)
        lower_text = text.lower()
        user_style = {
            "genre": "fantasy" if any(k in lower_text for k in ["queen", "castle", "magic", "sword", "king", "dragon"]) else "slice_of_life",
            "scene_type": "dialogue" if "\"" in text or "“" in text else "description",
            "language": language
        }
        
        # 3. Retrieval with Stylistic & Language Alignment
        benchmark = self._get_strong_example(text, user_metadata=user_style)
        
        # 4. Reasoning & Suggestion (Language-Locked)
        critique_prompt = self._build_critique_prompt(text, score_result, benchmark, language)
        
        critique = self._call_groq(critique_prompt)
        if not critique:
            print(f"Groq limited. Falling back to Gemini for {language} critique...")
            critique = self._call_gemini(critique_prompt)
            
        # 5. Context-Preserving Rewrite (Strictly Language-Locked)
        rewrite_prompt = self._build_rewrite_prompt(text, score_result, language)
        suggested_rewrite = self._call_groq(rewrite_prompt)
        if not suggested_rewrite:
            print(f"Groq limited. Falling back to Gemini for {language} rewrite...")
            suggested_rewrite = self._call_gemini(rewrite_prompt)

        if not critique:
            critique = f"Critique generation currently unavailable. Local analysis suggests: {score_result.get('label', 'Moderate')}"
        
        if not suggested_rewrite:
            suggested_rewrite = "Rewrite suggestion unavailable due to provider limits."

        return {
            "analysis": score_result,
            "feedback": feedback,
            "benchmark_example": benchmark,
            "agent_critique": critique,
            "suggested_rewrite": suggested_rewrite
        }

    def _build_critique_prompt(self, user_text, user_score, benchmark, language):
        bench_text = benchmark.get('text', '') if benchmark else "N/A"
        user_reasons = ', '.join(user_score.get('reasons', [])) if user_score.get('reasons') else 'No major issues'
        
        return f"""You are a gentle, expert writing mentor. 
Review the USER'S PARAGRAPH and compare it to a high-quality BENCHMARK.

STRICT RULE: YOU MUST RESPOND ENTIRELY IN {language.upper()}.

USER'S PARAGRAPH:
"{user_text}"
- Mentor Observation: {user_reasons}

BENCHMARK PARAGRAPH (for inspiration):
"{bench_text}"

TASK:
1. Explain specifically what the benchmark does better in terms of storytelling craft (rhythm, sensory details, or emotional subtext).
2. Provide 2-3 encouraging, actionable steps the writer can take right now to elevate their work.
Be specific to the user's context. Return clean, structured text only. No preamble. No English if the input is Hindi or Marathi."""

    def _build_rewrite_prompt(self, user_text, user_score, language):
        user_reasons = ', '.join(user_score.get('reasons', [])) if user_score.get('reasons') else 'No major issues'
        
        return f"""You are a master developmental editor. 
Your goal is to REWRITE the user's paragraph to improve its quality while STICKING TO THEIR STORY.

STRICT RULES:
1. YOU MUST RESPOND ENTIRELY IN {language.upper()}.
2. PRESERVE all characters (entities), settings, and plot points. 
3. DO NOT introduce random new characters, weather, or objects (No random boys, no random mist).
4. MAINTAIN the original tone and intent.
5. IMPROVE structural weaknesses like: {user_reasons}.
6. VARY sentence lengths to create a better rhythmic flow.
7. INJECT sensory details or show character emotions through actions (Show, Don't Tell).

ORIGINAL PARAGRAPH:
"{user_text}"

Return ONLY the refined paragraph in {language.upper()}. No explanation. No markdown."""

if __name__ == "__main__":
    agent = WriterCritiqueAgent()
    test_input = "He went to the forest. He saw a bear. The bear was big. He was scared."
    print(f"\nTesting Critique Agent with input: {test_input}")
    res = agent.analyze_and_critique(test_input)
    print(f"\nCritique Output:\n{res['agent_critique']}")
