import streamlit as st
import google.generativeai as genai
from typing import Dict, Tuple

from .prompts import (
    BASE_SYSTEM_INSTRUCTIONS,
    PROMPT_TEMPLATE_ENGLISH,
    PROMPT_TEMPLATE_HINDI,
    PROMPT_TEMPLATE_GLOBAL_EXPLAINER,
    PROMPT_TEMPLATE_COMPARISON_SECTION,
)

# =====================================================================
# GEMINI API KEY CONFIGURATION (5-Key Rotation)
#
# IMPORTANT: Replace these 5 placeholder values with your actual Gemini keys.
# =====================================================================

GEMINI_KEYS = [
        "AIzaSyAVfzxvB-6WSp3i7Yfv4n1PWsA3To-rR8k",
        "AIzaSyAXHLvsz3nEqe99ry_BQ8sbadCvHhDdtBE",
        "AIzaSyBDTz3gHHDfDOZU6FARjrVju-framMJ3CI",
        "AIzaSyAplo7Gv3oisIorskeHhrbQ1uev5_wyDiA",
        "AIzaSyA_5Bzcs6wVCTPp9HxLEZVw-ztHDeVMU8I",
        "AIzaSyBoNXhxWY3bR5HDk5UDNqvUuBEhgH4fISk",
        "AIzaSyAwnYTCg1rl4lcyDkik1AskYZgzaXNnVMw
]


# =====================================================================
# GEMINI GENERATION CORE
# =====================================================================

def gemini_generate(prompt: str) -> Tuple[str | None, str | None]:
    """
    Generates content using the configured Gemini model, rotating through the 
    list of 5 API keys until a successful response is received.
    Returns (text, model_used_name).
    """
    
    # Check if all keys are missing or set to placeholders
    if not any(key and key != f"YOUR_GEMINI_API_KEY_{i+1}" for i, key in enumerate(GEMINI_KEYS)):
        st.error("❌ All Gemini API Keys are missing or set to placeholders. Please update core/llm_client.py with your 5 keys.")
        return None, None
    
    # Iterate through keys for rotation
    for idx, key in enumerate(GEMINI_KEYS):
        if not key or key == f"YOUR_GEMINI_API_KEY_{idx+1}":
            # Skip empty or placeholder keys
            continue
            
        try:
            # Configure and call the model with the current key
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt)
            text = getattr(response, "text", "").strip()

            if text:
                return text, f"Gemini (Key {idx+1})"

        except Exception:
            # If the current key fails, suppress the error and try the next one
            continue

    # If the loop finishes without returning, all valid keys failed
    st.error("⚠️ All provided Gemini API keys failed to generate content.")
    return None, None


# =====================================================================
# PROMPT BUILDER (FOR INDIAN PREAMBLE)
# =====================================================================

def build_prompt(term: str, category: str, depth: int, explain_in_hindi: bool) -> str:
    base_prompt = PROMPT_TEMPLATE_ENGLISH.format(
        term=term,
        category=category,
        depth=depth,
    )

    if explain_in_hindi:
        return (
            BASE_SYSTEM_INSTRUCTIONS
            + "\n\n"
            + base_prompt
            + "\n\n"
            + PROMPT_TEMPLATE_HINDI
        )

    return BASE_SYSTEM_INSTRUCTIONS + "\n\n" + base_prompt


# =====================================================================
# MAIN FUNCTION — INDIAN PREAMBLE EXPLAINER
# ====================================================================

def explain_term_with_llm(
    term: str,
    category: str,
    explain_in_hindi: bool = False,
    depth: int = 2,
) -> Dict[str, str]:
    """
    Main LLM interface for explaining Indian Preamble terms (Gemini only).
    """

    prompt = build_prompt(term, category, depth, explain_in_hindi)

    result, key_used = gemini_generate(prompt)

    if result:
        return {
            "text": result,
            "model_used": key_used or "Gemini"
        }

    # FINAL FALLBACK
    return {
        "text": "⚠️ LLM generation failed. Check API keys and network connection.",
        "model_used": "None"
    }


# =====================================================================
# GLOBAL PREAMBLE EXPLORER FUNCTIONS
# =====================================================================

def build_global_prompt(country_name: str, preamble_text: str, include_comparison: bool) -> str:
    comparison_section = PROMPT_TEMPLATE_COMPARISON_SECTION if include_comparison else ""
    
    return PROMPT_TEMPLATE_GLOBAL_EXPLAINER.format(
        country_name=country_name,
        preamble_text=preamble_text,
        comparison_section=comparison_section
    )


def explain_preamble_global(country_name: str, preamble_text: str, include_comparison: bool) -> Dict[str, str]:
    """
    Generates an explanation and analysis for a country's preamble.
    """
    prompt = build_global_prompt(country_name, preamble_text, include_comparison)
    
    result, key_used = gemini_generate(prompt)

    if result:
        return {
            "text": result,
            "model_used": key_used or "Gemini"
        }

    return {
        "text": "⚠️ LLM analysis failed. Check API keys and network connection.",
        "model_used": "None"
    }


def fetch_country_preamble(country: str) -> Tuple[str | None, str, str]:
    """
    Uses Gemini to write the constitutional preamble of a country in an authentic style.
    
    Returns (preamble_text, message, source).
    """
    
    system_prompt = "You are a political science expert. Your task is to write a highly authentic and formal constitutional preamble for the given country, based on typical democratic principles. Output ONLY the preamble text."
    llm_query = f"Write the constitutional preamble of {country} in an authentic formal style, focusing on its core values."
    
    prompt = f"{system_prompt}\n\n{llm_query}"
    
    result, key_used = gemini_generate(prompt)
    
    source = key_used or "Gemini (AI-Generated)"

    if result:
        message = "✅ Preamble generated successfully by AI."
        return result, message, source
    else:
        message = "❌ AI generation failed. Check API keys and logs."
        return None, message, "None"
