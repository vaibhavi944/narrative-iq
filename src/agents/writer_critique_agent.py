import os
import json
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
# =========================================================

class WriterCritiqueAgent:
    """
    Agent that analyzes user prose and provides feedback based on
    semantically similar high-quality examples.
    """
    
    def __init__(self):
        # Initialize Groq for reasoning
        # We reuse the first key for reasoning tasks
        api_key = os.getenv("GROQ_API_KEY_1") or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Groq API key not found in environment.")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Cache for analysis dataset to allow for fast lookup of labels
        self.analysis_db_path = "data/processed/full_narrative_analysis.json"
        self._analysis_data = None

    @property
    def analysis_data(self):
        """Lazy load the analysis dataset."""
        if self._analysis_data is None:
            if os.path.exists(self.analysis_db_path):
                with open(self.analysis_db_path, "r", encoding="utf-8") as f:
                    # Convert to dict for O(1) ID lookup
                    raw_data = json.load(f)
                    self._analysis_data = {item["chunk_id"]: item for item in raw_data}
            else:
                self._analysis_data = {}
        return self._analysis_data

    def _get_strong_example(self, query_text, language, top_k=10):
        """
        Retrieves the most semantically similar 'Strong' example
        from the reference dataset.
        """
        # 1. Get raw similar chunks
        results = retrieve_similar_chunks(query_text, top_k=top_k)
        
        # 2. Filter for 'Strong' label using the analysis database
        for res in results:
            chunk_id = res["chunk_id"]
            if chunk_id in self.analysis_data:
                if self.analysis_data[chunk_id]["label"] == "Strong":
                    return self.analysis_data[chunk_id]
        
        # Fallback: if no Strong found in top-k, return the first result
        return results[0] if results else None

    def analyze_and_critique(self, text, language="english"):
        """
        Full orchestration flow: Analysis -> Retrieval -> Critique.
        """
        # 1. Analyze User Input
        score_result = score_paragraph(text, language=language)
        feedback = generate_feedback(score_result)
        
        # 2. Retrieve a "Strong" Benchmark
        # We search specifically for something that matches the user's theme
        benchmark = self._get_strong_example(text, language)
        
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
        Uses Llama-3 to compare the user's text with a benchmark and
        explain the qualitative difference.
        """
        if not benchmark:
            return "Unable to find a comparative benchmark for this specific theme."

        prompt = f"""You are a master literary editor. 
Compare the USER'S PARAGRAPH with the BENCHMARK PARAGRAPH (which is rated as 'Strong' in our quality index).

USER'S PARAGRAPH:
"{user_text}"
- Pacing Score: {user_score['pacing']['pacing_score']}
- Repetition Score: {user_score['repetition']['repetition_score']}
- Key Issues: {', '.join(user_score['reasons'])}

BENCHMARK PARAGRAPH (Quality Reference):
"{benchmark['text']}"
- Why it is Strong: {', '.join(benchmark['reasons'])}

YOUR TASK:
1. Explain specifically what the BENCHMARK does better in terms of rhythm, word choice, or emotional impact.
2. Provide 2-3 specific, actionable steps for the user to transform their paragraph to match this quality level.
3. Be encouraging but critically precise.

Return your response as a clean, structured critique. No preamble. No JSON."""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Critique generation failed: {e}"

# ---------------------------------------------------------
# Testing Block
# ---------------------------------------------------------

if __name__ == "__main__":
    agent = WriterCritiqueAgent()
    
    # Test with a known "Weak" style input
    test_input = "He went to the forest. He saw a bear. The bear was big. He was scared of the bear. He ran away from the forest."
    
    print("\n" + "="*70)
    print("NARRATIVE IQ - WRITER CRITIQUE AGENT TEST")
    print("="*70)
    print(f"INPUT: {test_input}")
    
    result = agent.analyze_and_critique(test_input)
    
    print("\n--- 1. ANALYSIS ---")
    print(f"Label: {result['analysis']['label']} | Score: {result['analysis']['combined_score']}")
    print(f"Issues: {result['analysis']['reasons']}")
    
    print("\n--- 2. BENCHMARK FOUND ---")
    if result['benchmark_example']:
        print(f"ID: {result['benchmark_example']['chunk_id']}")
        print(f"Text: {result['benchmark_example']['text'][:150]}...")
    
    print("\n--- 3. AGENT CRITIQUE ---")
    print(result['agent_critique'])
    print("\n" + "="*70)
