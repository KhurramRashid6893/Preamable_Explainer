import streamlit as st


# ====================================================================
# SHARED CSS STYLES (Cleaned up and simplified)
# ====================================================================

CUSTOM_CSS = """
<style>
    /* Global Streamlit overrides for a cleaner light mode */
    .stApp {
        background-color: #fcfcfc; /* Pure off-white background */
    }
    
    /* Custom Card Styling */
    .custom-card {
        background-color: white; 
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); /* Lighter, subtle shadow */
        margin-bottom: 25px;
        border: 1px solid #e9ecef; /* Very light border */
    }
    
    /* Specific Card Borders for visual separation */
    .indian-card {
        border-left: 6px solid #FF9933; /* Saffron/Orange */
    }
    .global-card {
        border-left: 6px solid #000080; /* Navy Blue */
    }
    .history-panel-card {
        background-color: #f7f7f7; /* Very light grey for the sidebar panel */
        padding: 15px;
        border: 1px solid #dee2e6;
    }

    /* Typography and Headings */
    h1, h2, h3, h4 {
        color: #1b2a49; /* Deep blue/black for text */
        font-weight: 700;
        margin-top: 0;
    }
    p, div {
        color: #343a40; /* Dark grey for body text */
        line-height: 1.6;
    }
    
    /* Preamble Text Box for better quote feel */
    .preamble-text-box {
        background-color: #f8f9fa; /* Slightly shaded background */
        border-left: 3px solid #ced4da;
        padding: 15px;
        border-radius: 6px;
        font-family: 'Georgia', serif;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    /* Custom Button Styling for Terms (using a green for action) */
    .stButton>button {
        background-color: #d4edda; /* Light Green */
        color: #155724; /* Dark Green text */
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #c3e6cb; 
        border-color: #155724;
    }
    
    /* History List Items (more compact) */
    .history-item {
        padding: 6px 0;
        border-bottom: 1px dotted #e9ecef;
    }
    .history-item:last-child {
        border-bottom: none;
    }

</style>
"""


def render_header():
    # Inject custom CSS first
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.markdown(f"""
        <h1 style="text-align: center; color: #1b2a49; margin-bottom: 5px;">
            🇮🇳🌍 Preamble Explorer
        </h1>
        <p style="text-align: center; color: #555; font-size: 1.05rem; margin-bottom: 25px;">
            A tool for understanding core constitutional values globally, powered by AI.
        </p>
    """, unsafe_allow_html=True)
    st.divider()


# ====================================================================
# INDIAN PREAMBLE COMPONENTS
# ====================================================================

def render_preamble_card(text):
    # Using an expander to keep the UI compact
    with st.expander("📜 Preamble of the Constitution of India (View Full Text)", expanded=False):
        st.markdown(f"""
            <div class="preamble-text-box">
                {text}
            </div>
        """, unsafe_allow_html=True)


def render_term_buttons(terms):
    st.markdown("### 🇮🇳 Explore Key Constitutional Values")
    
    cols = st.columns(3)
    selected = None

    for i, term in enumerate(terms):
        with cols[i % 3]:
            if st.button(term["label"], key=f"term_{term['label']}", use_container_width=True):
                selected = term

    return selected


def render_explanation_card(term, category, explanation, explain_in_hindi):
    lang = "Hindi + English" if explain_in_hindi else "English"

    st.markdown(f"""
        <div class="custom-card indian-card">
            <h4>🧠 Explanation: {term}</h4>
            <p style="margin-top:-8px; color:#6c757d; font-size: 0.9rem;">
                Category: <b>{category}</b> · Mode: {lang} · Model: {explanation['model_used']}
            </p>
            <div style="margin-top: 15px; overflow-wrap: break-word;">
                {explanation['text']}
            </div>
        </div>
    """, unsafe_allow_html=True)


# ====================================================================
# GLOBAL PREAMBLE COMPONENTS
# ====================================================================

def render_global_preamble_card(country: str, preamble: str, source: str):
    st.markdown(f"""
        <div class="custom-card global-card">
            <h4>🌍 Preamble of {country}</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin-top: -10px;">
                Source: {source}
            </p>
            <div class="preamble-text-box">
                {preamble}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_global_explanation_card(country: str, explanation: dict, include_comparison: bool):
    comparison_mode = "with India Comparison" if include_comparison else "Analysis Only"
    
    st.markdown(f"""
        <div class="custom-card">
            <h4>🧠 Analysis: {country}'s Preamble</h4>
            <p style="margin-top:-8px; color:#6c757d; font-size: 0.9rem;">
                Mode: {comparison_mode} · Model: {explanation['model_used']}
            </p>
            <div style="margin-top: 15px; overflow-wrap: break-word;">
                {explanation['text']}
            </div>
        </div>
    """, unsafe_allow_html=True)


# ====================================================================
# HISTORY PANEL (UPDATED)
# ====================================================================

def render_history_panel(history):
    st.markdown(f"""
        <div class="custom-card history-panel-card">
            <h4 style="margin-bottom: 5px;">⏳ Recent Lookups</h4>
    """, unsafe_allow_html=True)

    if len(history) == 0:
        st.caption("No lookups yet. Explore a term or country.")
    else:
        # Use an expander for the history details
        with st.expander("View History Details", expanded=True):
            for i, item in enumerate(history[:10]):
                
                if 'term' in item: # Indian Preamble Term
                    title = f"🇮🇳 {item['term']}"
                    detail = f"Category: {item['category']} ({'Hindi' if item.get('hindi') else 'English'})"
                elif 'country' in item: # Global Preamble
                    title = f"🌍 {item['country']}"
                    comparison = "w/ Compare" if item.get('compare') else "Summary"
                    detail = f"Global Preamble ({comparison})"
                else:
                    continue

                st.markdown(f"""
                    <div class="history-item">
                        <p style="margin: 0; font-weight: 600; color: #1b2a49; font-size: 0.95rem;">
                            {i+1}. {title} 
                        </p>
                        <p style="margin: 0; font-size: 0.8rem; color: #777;">
                            {detail}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ====================================================================
# FOOTER
# ====================================================================

def render_footer():
    st.divider()
    st.markdown("""
        <p style="text-align:center; color:#777; font-size:0.9rem; margin-top: 10px;">
            Built for Educational Purposes (Samvidhan Divas) · Version 1.0
By Khurram Rashid
        </p>
    """, unsafe_allow_html=True)
