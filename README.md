# 🇮🇳🌍 Preamble Explorer  
AI-Powered Constitutional Learning Tool

**Preamble Explorer** is an educational AI application designed to help students, educators, and citizens understand constitutional values — beginning with India's Preamble and extending to the preambles of countries across the world.

This project was built on **26 November (Constitution Day / Samvidhan Divas)** to commemorate the adoption of the Constitution of India in 1949.

---

## Key Features

### 1. Indian Preamble Deep Dive  
Explore the foundational pillars of the Indian Constitution such as **Justice, Liberty, Equality, Fraternity, Sovereign, Secular, Democratic,** and **Republic**.

- **Structured explanations**: Meaning, constitutional significance, and real-world examples.  
- **Multilingual support**: Toggle explanations between English and Hindi.  
- **Adjustable depth**: Choose concise (1), standard (2), or detailed (3) explanation levels.

---

### 2. World Preamble Explorer  
Analyze constitutional preambles of nations across the globe.

- **AI-generated preambles**: Enter any country name to generate a formal-style preamble.  
- **Insightful analysis**: Identify key values, themes, and constitutional philosophy.  
- **Comparison option**: Compare any country's preamble with India’s Preamble.

---

### 3. Integrated History Panel  
A persistent history panel tracks all your explored Indian values and country preambles for easy revisiting.

---

## Technologies Used

- **Framework**: Streamlit (Python)  
- **AI Engine**: Google Gemini API with multi-key rotation  

---

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt

2. Configure Gemini API Keys

1. Open the file core/llm_client.py.


2. Locate the following:



GEMINI_KEYS = [
    "YOUR_GEMINI_API_KEY_1",
    "YOUR_GEMINI_API_KEY_2",
    ...
]

3. Replace the placeholder values with your actual Gemini API keys.



3. Run the Application

streamlit run core/app.py


---

Project Structure

Preamble_Explorer/
│
├── core/
│   ├── app.py              # Main Streamlit app
│   ├── llm_client.py       # Gemini LLM engine
│   ├── ui_components.py    # UI utilities
│   ├── preamble_data.py    # Indian Preamble data
│   ├── prompts.py          # Prompt templates
│
├── .streamlit/
│   └── config.toml         # Light theme configuration
│
├── requirements.txt
└── README.md


---

Purpose

This project aims to promote constitutional literacy by making complex legal ideas simple and approachable. It serves:

Students

Teachers

UPSC/Judiciary aspirants

Researchers

Civically engaged citizens
