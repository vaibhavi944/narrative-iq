import os
import json
from src.agents.writer_critique_agent import WriterCritiqueAgent

# =========================================================
# NarrativeIQ - Writer Critique Agent Validation Suite
# =========================================================
# Purpose:
# Validates the quality of AI reasoning, retrieval relevance,
# and multilingual support of the Writer Critique Agent.
# =========================================================

def run_agent_validation():
    agent = WriterCritiqueAgent()
    
    test_cases = [
        {
            "name": "REPETITIVE WEAK PROSE",
            "lang": "english",
            "text": "The cat sat on the mat. The cat was happy on the mat. The mat was soft for the cat. The cat liked the soft mat."
        },
        {
            "name": "EMOTIONALLY FLAT PROSE",
            "lang": "english",
            "text": "The man walked to the store. He bought bread and milk. He paid with cash. He walked home and put the groceries away."
        },
        {
            "name": "STRONG EMOTIONAL PROSE",
            "lang": "english",
            "text": "He stood at the edge of the cliff, the wind howling like a wounded beast. Every breath was a struggle against the weight of his regret, a heavy anchor pulling him toward the jagged rocks below."
        },
        {
            "name": "HIGH-ACTION PROSE",
            "lang": "english",
            "text": "He lunged forward, blade flashing in the dim light. The guard barely parried, the metal clashing with a bone-jarring vibration. He spun, kicked the guard's knee, and slammed him against the stone wall."
        },
        {
            "name": "DIALOGUE-HEAVY PROSE",
            "lang": "english",
            "text": "\"Where are you going?\" she asked. \"Nowhere,\" he replied. \"You always say that,\" she snapped. \"Because it's always true,\" he muttered without looking back."
        },
        {
            "name": "EXTREMELY SHORT",
            "lang": "english",
            "text": "He cried."
        },
        {
            "name": "HINDI TEST",
            "lang": "hindi",
            "text": "वह बहुत उदास था। उसके पास कोई नहीं था। वह बस बैठा रहा और रोता रहा।"
        },
        {
            "name": "MARATHI TEST",
            "lang": "marathi",
            "text": "तो खूप आनंदी होता. आज त्याचा वाढदिवस होता. सर्व मित्र आले होते."
        }
    ]

    print("\n" + "="*80)
    print("NARRATIVE IQ - AGENT INTELLIGENCE AUDIT")
    print("="*80)

    for tc in test_cases:
        print(f"\n>>> TEST CASE: {tc['name']}")
        print(f"Language: {tc['lang']}")
        print(f"Input: {tc['text']}")
        print("-" * 40)

        try:
            result = agent.analyze_and_critique(tc['text'], language=tc['lang'])
            
            # 1. Narrative Analysis Verification
            analysis = result["analysis"]
            print(f"[ANALYSIS] Label: {analysis['label']} | Score: {analysis['combined_score']}")
            print(f"[ISSUES]   {analysis['reasons']}")
            
            # 2. Retrieval Verification
            benchmark = result["benchmark_example"]
            if benchmark:
                print(f"[RAG] Found Benchmark: {benchmark['chunk_id']} ({benchmark['genre']}/{benchmark['scene_type']})")
                print(f"[RAG PREVIEW] {benchmark['text'][:150]}...")
            else:
                print("[RAG WARNING] No benchmark found.")

            # 3. Critique Verification
            critique = result["agent_critique"]
            print(f"\n[CRITIQUE]\n{critique}")

            # 4. Intelligence Quality Checks (Warnings)
            if len(critique) < 100:
                print("\n[QUALITY WARNING] Critique seems unusually short/generic.")
            
            if benchmark and tc['lang'] == "english":
                # Basic relevance check (keyword-based for this test)
                text_lower = tc['text'].lower()
                bench_lower = benchmark['text'].lower()
                # Simple check for thematic overlap
                thematic_keywords = ["cat", "man", "forest", "bear", "cliff", "guard", "she", "happy", "sad"]
                found_keyword = any(k in text_lower and k in bench_lower for k in thematic_keywords)
                if not found_keyword:
                    print("[QUALITY WARNING] Low thematic overlap detected between input and benchmark.")

        except Exception as e:
            print(f"[ERROR] Test failed: {e}")

        print("\n" + "="*80)

if __name__ == "__main__":
    run_agent_validation()
