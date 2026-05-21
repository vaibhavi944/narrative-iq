import os
import json
import time
from groq import Groq
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
# Orchestrates analysis, retrieval, and comparative reasoning
# to provide writers with context-aware critiques.
# Robust version with safe dictionary access and normalization.
# =========================================================

class WriterCritiqueAgent:
    """
    Agent that analyzes user prose and provides feedback based on
    semantically similar high-quality examples.
    """
    
    def __init__(self):
        # API Key Rotation Management
        self.keys = []
        for i in range(1, 6):
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key:
                self.keys.append(key)
        if not self.keys:
            single = os.getenv("GROQ_API_KEY")
            if single:
                self.keys.append(single)
        
        if not self.keys:
            raise ValueError("No Groq API keys found in .env file")
            
        self.current_key_index = 0
        self.model = "llama-3.3-70b-versatile"
        
        # Cache for analysis dataset to allow for fast lookup of labels
        self.analysis_db_path = "data/processed/full_narrative_analysis.json"
        self._analysis_data = None

    @property
    def analysis_data(self):
        """Lazy load the analysis dataset."""
        if self._analysis_data is None:
            if os.path.exists(self.analysis_db_path):
                try:
                    with open(self.analysis_db_path, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)
                        # Convert to dict for O(1) ID lookup
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

    def _get_client(self):
        """Returns a Groq client using the current rotated key."""
        return Groq(api_key=self.keys[self.current_key_index])

    def _call_groq_with_rotation(self, prompt):
        """Executes LLM call with API key rotation logic."""
        attempts = 0
        max_attempts = len(self.keys) * 2
        
        while attempts < max_attempts:
            try:
                client = self._get_client()
                completion = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return completion.choices[0].message.content.strip()
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "rate_limit" in error_str.lower():
                    print(f"Critique Agent: Key {self.current_key_index + 1} hit rate limit.")
                    self.current_key_index = (self.current_key_index + 1) % len(self.keys)
                    if self.current_key_index == 0:
                        print("All keys exhausted. Waiting 65 seconds for reset...")
                        time.sleep(65)
                    print(f"Switching to key {self.current_key_index + 1}...")
                else:
                    print(f"Non-rate-limit error in critique generation: {e}")
                    return None
            attempts += 1
        return None

    def _get_strong_example(self, query_text, top_k=10):
        """
        Retrieves the most semantically similar 'Strong' example
        from the reference dataset.
        """
        # 1. Get raw similar chunks
        try:
            results = retrieve_similar_chunks(query_text, top_k=top_k)
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None
        
        if not results:
            return None

        # 2. Filter for 'Strong' label using the analysis database
        for res in results:
            chunk_id = res.get("chunk_id")
            if chunk_id in self.analysis_data:
                bench = self.analysis_data[chunk_id]
                if bench.get("label") == "Strong":
                    return self._normalize_chunk(bench)
        
        # Fallback: if no Strong found in top-k, return the first result normalized
        return self._normalize_chunk(results[0])

    def analyze_and_critique(self, text, language="english"):
        """
        Full orchestration flow: Analysis -> Retrieval -> Critique.
        """
        if not text or not text.strip():
            return {
                "error": "Empty input text provided.",
                "agent_critique": "Please provide narrative text for analysis."
            }

        # 1. Analyze User Input
        try:
            score_result = score_paragraph(text, language=language)
            feedback = generate_feedback(score_result)
        except Exception as e:
            print(f"Internal Analysis Error: {e}")
            return {
                "error": f"Internal analysis failed: {e}",
                "agent_critique": "Unable to perform narrative analysis at this time."
            }
        
        # 2. Retrieve a "Strong" Benchmark
        benchmark = self._get_strong_example(text)
        
        # 3. Generate Comparative Critique using LLM
        critique = self._generate_comparative_reasoning(
            user_text=text,
            user_score=score_result,
            benchmark=benchmark
        )
        
        return {
            "analysis": score_result,
            "feedback": feedback,
            "benchmark_example": benchmark,
            "agent_critique": critique
        }

    def _generate_comparative_reasoning(self, user_text, user_score, benchmark):
        """
        Uses LLM to compare the user's text with a benchmark and
        explain the qualitative difference.
        """
        if not benchmark:
            return "Unable to retrieve benchmark examples, but local narrative analysis completed successfully."

        # Double check benchmark text
        if not benchmark.get("text"):
            return "Retrieved benchmark was malformed. Unable to perform comparative analysis."

        prompt = f"""You are a master literary editor. 
Compare the USER'S PARAGRAPH with the BENCHMARK PARAGRAPH (which is rated as 'Strong' in our quality index).

USER'S PARAGRAPH:
"{user_text}"
- Pacing Score: {user_score.get('pacing', {}).get('pacing_score', 0.0)}
- Repetition Score: {user_score.get('repetition', {}).get('repetition_score', 0.0)}
- Key Issues: {', '.join(user_score.get('reasons', [])) if user_score.get('reasons') else 'No major issues'}

BENCHMARK PARAGRAPH (Quality Reference):
"{benchmark.get('text', '')}"
- Why it is Strong: {', '.join(benchmark.get('reasons', [])) if benchmark.get('reasons') else 'Well-balanced rhythm and clarity'}

YOUR TASK:
1. Explain specifically what the BENCHMARK does better in terms of rhythm, word choice, or emotional impact.
2. Provide 2-3 specific, actionable steps for the user to transform their paragraph to match this quality level.
3. Be encouraging but critically precise.

Return your response as a clean, structured critique. No preamble. No JSON."""

        critique = self._call_groq_with_rotation(prompt)
        
        if not critique:
            return "Critique generation was interrupted by API constraints. Local analysis suggests: " + user_score.get('label', 'Moderate')
            
        return critique

# ---------------------------------------------------------
# Local CLI Testing
# ---------------------------------------------------------

if __name__ == "__main__":
    agent = WriterCritiqueAgent()
    test_input = "He went to the forest. He saw a bear. The bear was big."
    print(f"\nTesting Agent Robustness with input: {test_input}")
    res = agent.analyze_and_critique(test_input)
    print(f"\nCritique Output:\n{res['agent_critique']}")
