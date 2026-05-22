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
        
        # Blocklist for known corrupted chunks
        self.BLOCKED_CHUNK_IDS = {"mar_021_02", "mar_021_01", "mar_021_03"}
        
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

    def _is_valid_chunk(self, chunk):
        import re
        
        chunk_id = chunk.get("chunk_id", "")
        
        # Block known corrupted chunks directly
        if chunk_id in self.BLOCKED_CHUNK_IDS:
            return False
        
        text = chunk.get("text", "")
        
        # Must have minimum length
        if len(text) < 80:
            return False
        
        # No Cyrillic characters
        if re.search(r'[\u0400-\u04FF]', text):
            return False
        
        # No Chinese/Japanese/Korean characters
        if re.search(r'[\u4E00-\u9FFF]', text):
            return False
        
        # Must have at least 2 sentences
        sentences = [s.strip() for s in 
                    re.split(r'[.।?!]', text) if s.strip()]
        if len(sentences) < 2:
            return False
        
        # Must have minimum word count
        words = text.split()
        if len(words) < 15:
            return False
        
        return True

    def _get_strong_example(self, query_text, language="english", top_k=50):
        """
        Retrieves the most semantically similar 'Strong' example
        in the TARGET LANGUAGE from the reference dataset.
        """
        # 1. Get raw similar chunks
        try:
            results = retrieve_similar_chunks(query_text, top_k=50)
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None
        
        if not results:
            return None

        # 2. Filter for 'Strong' label AND matching language AND valid quality
        for res in results:
            chunk_id = res.get("chunk_id")
            if chunk_id in self.analysis_data:
                bench = self.analysis_data[chunk_id]
                is_strong = bench.get("label") == "Strong"
                is_lang_match = bench.get("language", "").lower() == language.lower()
                is_valid = self._is_valid_chunk(bench)
                
                if is_strong and is_lang_match and is_valid:
                    return self._normalize_chunk(bench)
        
        # 3. Fallback: If no Strong match in target language, find ANY valid match in target language
        for res in results:
            if res.get("language", "").lower() == language.lower() and self._is_valid_chunk(res):
                return self._normalize_chunk(res)
        
        # 4. Final fallback: pick best valid Strong chunk in target language by score
        lang_strong_chunks = [
            v for v in self.analysis_data.values()
            if v.get("language", "").lower() == language.lower()
            and v.get("label") == "Strong"
            and self._is_valid_chunk(v)
        ]
        if lang_strong_chunks:
            best = max(lang_strong_chunks, key=lambda x: x.get("combined_score", 0))
            return self._normalize_chunk(best)

        # 5. Absolute last fallback: return the highest scoring valid Hindi chunk
        # (as an emergency fallback for Marathi/English if nothing else is found)
        all_strong = [
            v for v in self.analysis_data.values()
            if v.get("label") == "Strong"
            and self._is_valid_chunk(v)
        ]
        if all_strong:
            best = max(all_strong, key=lambda x: x.get("combined_score", 0))
            return self._normalize_chunk(best)

        return None

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
            feedback = generate_feedback(score_result, language=language)
        except Exception as e:
            print(f"Internal Analysis Error: {e}")
            return {
                "error": f"Internal analysis failed: {e}",
                "agent_critique": "Unable to perform narrative analysis at this time."
            }
        
        # 2. Retrieve a "Strong" Benchmark in the SAME language
        benchmark = self._get_strong_example(text, language=language)
        
        # 3. Generate Comparative Critique using LLM
        critique = self._generate_comparative_reasoning(
            user_text=text,
            user_score=score_result,
            benchmark=benchmark,
            language=language
        )
        
        return {
            "analysis": score_result,
            "feedback": feedback,
            "benchmark_example": benchmark,
            "agent_critique": critique
        }

    def _generate_comparative_reasoning(self, user_text, user_score, benchmark, language="english"):
        """
        Uses LLM to compare the user's text with a benchmark.
        CRITICAL: This method has a ZERO-TOLERANCE policy for English when another language is selected.
        """
        if not benchmark:
            return "Unable to retrieve benchmark."

        lang_map = {
            "english": "ENGLISH",
            "hindi": "HINDI",
            "marathi": "MARATHI"
        }
        target_lang = lang_map.get(language, "ENGLISH")

        # The prompt is now a direct order with high penalty for English
        prompt = f"""You are a master literary editor. 
You must analyze the USER'S PARAGRAPH against the BENCHMARK.

USER'S PARAGRAPH: "{user_text}"
BENCHMARK PARAGRAPH: "{benchmark.get('text', '')}"

INSTRUCTIONS:
1. Explain what the BENCHMARK does better regarding rhythm and word choice.
2. Give 3 actionable steps to improve the USER'S PARAGRAPH.

!!! ABSOLUTE REQUIREMENT !!!
YOUR ENTIRE RESPONSE MUST BE WRITTEN IN {target_lang}. 
- IF LANGUAGE IS HINDI, EVERY SINGLE WORD MUST BE HINDI.
- IF LANGUAGE IS MARATHI, EVERY SINGLE WORD MUST BE MARATHI.
- DO NOT USE ENGLISH TERMS LIKE 'Rhythm', 'Pacing', or 'Actionable Steps'. TRANSLATE THEM.
- DO NOT USE ENGLISH HEADERS.
- FAILURE TO COMPLY WILL RESULT IN SYSTEM ERROR.

FORMAT (use {target_lang} for all text including headers):
Write a short paragraph analyzing what the benchmark does better.
Then write exactly 3 numbered improvement steps.
No markdown. No mixed languages. Everything in {target_lang} only."""

        return self._call_groq_with_rotation(prompt)

    def generate_rewrite(self, user_text, benchmark, language="english"):
        lang_map = {
            "english": "ENGLISH",
            "hindi": "HINDI",
            "marathi": "MARATHI"
        }
        target_lang = lang_map.get(language, "ENGLISH")
        
        # Build language instruction dynamically
        if language == "hindi":
            lang_instruction = "Write ONLY in Hindi Devanagari script. Every single word must be Hindi. No English words at all."
        elif language == "marathi":
            lang_instruction = "Write ONLY in Marathi Devanagari script. Every single word must be Marathi. No English words at all."
        else:
            lang_instruction = f"Write ONLY in {target_lang}."

        benchmark_text = benchmark.get("text", "") if benchmark else ""
        
        prompt = f"""You are a master literary editor who rewrites weak prose.

USER'S ORIGINAL TEXT:
"{user_text}"

STYLE REFERENCE (how good writing looks):
"{benchmark_text}"

YOUR TASK:
Rewrite the user's original text to make it stronger.
Fix these issues: repetitive sentence starts, flat emotion, monotonous pacing.
Keep the same meaning and story. Just make it better written.
Make it feel natural and human, not robotic.
Use simple vocabulary that any reader can understand.

CRITICAL RULES - MUST FOLLOW:
- {lang_instruction}
- Do not mix languages under any circumstance.
- Do not add any explanation or headers.
- Just the rewritten paragraph directly.
- Nothing else."""

        return self._call_groq_with_rotation(prompt)

# ---------------------------------------------------------
# Local CLI Testing
# ---------------------------------------------------------

if __name__ == "__main__":
    agent = WriterCritiqueAgent()
    test_input = "He went to the forest. He saw a bear. The bear was big."
    print(f"\nTesting Agent Robustness with input: {test_input}")
    res = agent.analyze_and_critique(test_input)
    print(f"\nCritique Output:\n{res['agent_critique']}")
