import os
import streamlit as st
from datetime import datetime
# Removed: import requests # Not needed as external API calls are gone.

from core.preamble_data import PREAMBLE_TEXT, PREAMBLE_TERMS

# Consolidating the LLM client imports for clarity
from core.llm_client import (
    explain_term_with_llm, 
    fetch_country_preamble, 
    explain_preamble_global
)
from core.ui_components import (
    render_header,
    render_preamble_card,
    render_term_buttons,
    render_explanation_card,
    render_history_panel,
    render_footer,
    render_global_preamble_card,
    render_global_explanation_card,
)


# ====================================================================
# SESSION STATE MANAGEMENT
# ====================================================================

def init_session_state():
    if "history" not in st.session_state:
        # History stores both Indian term explanations and Global Preamble lookups
        st.session_state["history"] = []
    if "selected_term" not in st.session_state:
        st.session_state["selected_term"] = None
    if "global_preamble_data" not in st.session_state: # Stores the fetched preamble, if any
        st.session_state["global_preamble_data"] = None
    if "country_input" not in st.session_state:
        st.session_state["country_input"] = ""


def handle_global_fetch(country_name):
    """Handles the full lifecycle of fetching and analyzing a global preamble."""
    
    st.session_state["global_preamble_data"] = None
    
    if not country_name:
        st.error("Please enter a country name.")
        return

    with st.spinner(f"Generating the Preamble of {country_name} with AI..."): # Updated message
        # 1. Fetch Preamble (now always Gemini generated)
        preamble_text, message, source = fetch_country_preamble(country_name)
        
        if not preamble_text:
            # If preamble_text is None, it means the AI generation failed.
            st.error(f"❌ Preamble fetch failed: {message}")
            return
        
        # Show a warning/info if the source isn't the primary goal (in this case, 
        # since it's always AI, we just proceed, but keep the message for clarity)
        if "Gemini" in source or source == "AI-Generated":
            st.info(f"Preamble content: {message}") # Changed to st.info for a positive result
        
        # 2. Store Preamble Data
        st.session_state["global_preamble_data"] = {
            "country": country_name,
            "preamble_text": preamble_text,
            "fetch_source": source,
            "fetch_message": message,
            "explanation": None, # Placeholder
            "compare_india": st.session_state.get("compare_india", False),
        }
    
    # Trigger explanation automatically after fetch
    st.rerun() # UPDATED: Changed st.experimental_rerun() to st.rerun()


def handle_global_explain(preamble_data):
    """Handles the LLM analysis of the fetched global preamble."""
    country_name = preamble_data['country']
    preamble_text = preamble_data['preamble_text']
    include_comparison = st.session_state.get("compare_india", False)
    
    with st.spinner(f"Analyzing the Preamble of {country_name} with AI..."):
        explanation = explain_preamble_global(
            country_name=country_name,
            preamble_text=preamble_text,
            include_comparison=include_comparison,
        )
        
    # Update global_preamble_data with explanation
    st.session_state["global_preamble_data"]["explanation"] = explanation
    
    # 3. Log to history
    st.session_state["history"].insert(
        0,
        {
            "type": "global",
            "country": country_name,
            "preamble_snippet": preamble_text[:100] + "...",
            "compare": include_comparison,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        },
    )


# ====================================================================
# MAIN APPLICATION
# ====================================================================

def main():
    st.set_page_config(
        page_title="AI-Powered Preamble Explainer 🇮🇳🌍",
        page_icon="🇮🇳",
        layout="wide",
        # Ensure we are in a light theme environment
        initial_sidebar_state="expanded", 
    )

    init_session_state()

    render_header()

    # --- Layout Setup ---
    col_left, col_right = st.columns([2, 1])

    with col_right:
        # History Panel (Sidebar Look)
        render_history_panel(st.session_state["history"])

    with col_left:
        # ----------------------------------------------------------------
        # SECTION 1: INDIAN PREAMBLE EXPLORER (Existing Logic)
        # ----------------------------------------------------------------
        st.markdown("## 🇮🇳 Indian Preamble Explorer") # Simplified heading
        render_preamble_card(PREAMBLE_TEXT)

        st.markdown("#### Configure Explanation")

        # Hindi toggle + depth slider for Indian Preamble
        c1, c2 = st.columns([1, 1])
        with c1:
            explain_in_hindi = st.toggle("Explain in Hindi 🇮🇳", value=False)
        with c2:
            depth = st.slider(
                "Explanation depth",
                min_value=1,
                max_value=3,
                value=2,
                key="indian_depth",
                help="1 = very short, 3 = more detailed",
            )

        selected_term = render_term_buttons(PREAMBLE_TERMS)

        if selected_term:
            st.session_state["selected_term"] = selected_term
            # Reset global state when switching back to Indian Preamble
            st.session_state["global_preamble_data"] = None

        active_term = st.session_state.get("selected_term")

        if active_term and not st.session_state.get("global_preamble_data"):
            # Ensure we only run for Indian Preamble if global data is not active
            explanation = explain_term_with_llm(
                term=active_term["label"],
                category=active_term["category"],
                explain_in_hindi=explain_in_hindi,
                depth=depth,
            )

            # Save to history
            if st.session_state.get("selected_term") is not None:
                st.session_state["history"].insert(
                    0,
                    {
                        "type": "indian",
                        "term": active_term["label"],
                        "category": active_term["category"],
                        "explanation": explanation,
                        "hindi": explain_in_hindi,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    },
                )
            
            # Render Indian Explanation
            render_explanation_card(
                term=active_term["label"],
                category=active_term["category"],
                explanation=explanation,
                explain_in_hindi=explain_in_hindi,
            )

        st.markdown("---")


        # ----------------------------------------------------------------
        # SECTION 2: WORLD PREAMBLE EXPLORER (NEW LOGIC)
        # ----------------------------------------------------------------
        st.markdown("## 🌍 World Preamble Explorer") # Simplified heading
        
        # Input and Button in a single form to handle the click event
        with st.form(key="global_fetch_form"):
            country_input = st.text_input(
                "Enter country name to generate its Constitutional Preamble (AI-Generated)",
                key="country_input_text",
                placeholder="e.g., Germany, USA, South Africa"
            )
            
            st.toggle(
                "Include comparison with Indian Preamble",
                key="compare_india",
                value=True,
                help="The AI will add a section comparing the generated Preamble with India's.",
            )
            
            submitted = st.form_submit_button("Generate & Analyze Preamble 🔎") # Updated button text

            if submitted:
                # Clear Indian Preamble term state
                st.session_state["selected_term"] = None 
                handle_global_fetch(country_input.strip())
        
        
        # Display the fetched preamble and explanation
        global_data = st.session_state.get("global_preamble_data")
        
        if global_data:
            # 1. Render the fetched preamble
            render_global_preamble_card(
                country=global_data['country'],
                preamble=global_data['preamble_text'],
                source=global_data['fetch_source'],
            )

            # 2. Check if explanation has been run, if not, run it.
            if global_data.get("explanation") is None:
                # Note: This is a re-run but triggered within a handler, so it works.
                handle_global_explain(global_data)
                # We need to manually re-run here to show the new explanation state
                st.rerun() # UPDATED: Changed st.experimental_rerun() to st.rerun()
            
            # 3. Render the explanation
            if global_data.get("explanation"):
                render_global_explanation_card(
                    country=global_data['country'],
                    explanation=global_data['explanation'],
                    include_comparison=global_data['compare_india'],
                )


    render_footer()


if __name__ == "__main__":
    # Removed requests.packages.urllib3.disable_warnings() as external API calls are gone.
    main()