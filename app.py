import streamlit as st
import os
from dotenv import load_dotenv

# Import our core logic
from src.agents.writer_critique_agent import WriterCritiqueAgent
from src.utils.text_splitter import split_into_paragraphs
from src.utils.language_utils import get_localized_ui

# Load environment variables (GROQ_API_KEY)
load_dotenv()

def main():
    st.set_page_config(page_title="NarrativeIQ", layout="wide")

    # Sidebar settings
    st.sidebar.header("Settings")
    language = st.sidebar.selectbox("Select Language", ["english", "hindi", "marathi"])
    
    # Get Localized Strings
    ut = get_localized_ui(language)

    st.title(ut["title"])
    st.markdown(ut["subtitle"])

    # Input Area
    user_text = st.text_area("Input:", height=200, placeholder=ut["placeholder"], label_visibility="collapsed")

    if st.button(ut["button"], key="analyze_btn"):
        if not user_text.strip():
            st.warning("Empty text!")
        else:
            # FIX 5 - Check for vector database
            if not os.path.exists("data/processed/narrative_index.faiss"):
                st.error("Vector database not found. Please run the ingestion pipeline first.")
                st.stop()

            with st.spinner("Processing..."):
                try:
                    agent = WriterCritiqueAgent()
                    paragraphs = split_into_paragraphs(user_text)
                    
                    # FIX 1 - Update target_para logic
                    target_para = paragraphs[0] if paragraphs else user_text.strip()

                    result = agent.analyze_and_critique(target_para, language=language)
                    
                    st.session_state.analysis_result = result
                    st.session_state.target_para = target_para
                    st.session_state.language = language
                    st.session_state.rewrite_result = ""
                except Exception as e:
                    st.error(f"Error: {e}")

    # Display Section (Outside the Analyze button block)
    if "analysis_result" in st.session_state and st.session_state.analysis_result:
        result = st.session_state.analysis_result
        language = st.session_state.get("language", "english")
        target_para = st.session_state.get("target_para", "")
        
        agent = WriterCritiqueAgent() # Initialize for rewrite or display
        
        analysis = result["analysis"]
        feedback = result["feedback"] 
        benchmark = result["benchmark_example"]
        critique = result["agent_critique"]

        # --- DISPLAY ---
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader(ut["metrics_header"])
            # Label from localized feedback
            st.metric(label=ut["quality_label"], value=f"{analysis['combined_score']:.2f}", delta=feedback["label"])
            st.progress(analysis["combined_score"])

            st.markdown(f"**{feedback['summary']}**")
            
            if feedback["tips"]:
                st.error(ut["issues_header"])
                for tip in feedback["tips"]:
                    st.write(f"• {tip}")

        with col2:
            st.subheader(ut["critique_header"])
            st.markdown(critique)

        st.divider()
        st.subheader(ut["rag_header"])
        if benchmark:
            st.info(f"{ut['benchmark_id']} {benchmark.get('chunk_id')} | {ut['genre']} {benchmark.get('genre')}")
            st.write(benchmark.get("text"))

            # --- REWRITE SECTION ---
            st.divider()
            st.subheader(ut["rewrite_header"])
            
            if st.button(ut["rewrite_button"], key="rewrite_btn"):
                with st.spinner("Generating rewrite..."):
                    rewrite = agent.generate_rewrite(
                        st.session_state.target_para,
                        benchmark,
                        st.session_state.language
                    )
                    st.session_state.rewrite_result = rewrite or "Could not generate rewrite."

            if st.session_state.get("rewrite_result"):
                st.markdown(f"**{ut['rewrite_label']}**")
                st.text_area("", 
                    value=st.session_state.rewrite_result, 
                    height=200, 
                    label_visibility="collapsed",
                    key="rewrite_display"
                )

if __name__ == "__main__":
    main()
