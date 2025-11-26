BASE_SYSTEM_INSTRUCTIONS = """
You are an expert constitutional law tutor explaining concepts from the Preamble 
to the Constitution of India to university students and general citizens.

Your explanations must:
- Be accurate to the Indian Constitution and democratic values.
- Use very clear, simple language.
- Connect each term to real-life Indian situations.
- Avoid giving legal advice; only provide general educational information.
"""

PROMPT_TEMPLATE_ENGLISH = """
Explain the term "{term}" as it appears in the Preamble of the Constitution of India.

Context:
- Term category: {category}
- Audience: university students + general citizens
- Depth level: {depth} (1 = very short, 3 = detailed)

Structure your answer in this format:

1. Simple meaning (2–3 lines)
2. Constitutional significance (How does it shape India's democracy?)
3. Real-life example from everyday Indian life (non-technical)
4. Related constitutional references (like Articles or important cases, short and simple)

Write clearly and concisely. Do not use bullet points inside headings; just simple paragraphs.
"""

PROMPT_TEMPLATE_HINDI = """
अब आप वही बात हिंदी में समझाएँ।

संरचना (Structure):

1. सरल अर्थ (2–3 पंक्तियाँ)
2. भारतीय संविधान में महत्व
3. आम भारतीय जीवन से जुड़ा उदाहरण
4. यदि ज़रूरी हो तो संबंधित अनुच्छेद या प्रावधान का छोटा उल्लेख

भाषा सरल, सम्मानजनक और आसानी से समझ आने वाली रखें।
"""

# --- NEW PROMPT FOR WORLD PREAMBLE EXPLORER ---

PROMPT_TEMPLATE_GLOBAL_EXPLAINER = """
Analyze the following Constitutional Preamble for the country: "{country_name}".

Preamble Text:
---
{preamble_text}
---

Your task is to provide a comprehensive analysis based on the structure below.
The analysis should be insightful and educational, suitable for general citizens.

Structure your answer in this format:

1. Main Values & Themes (Identify 3-5 core principles, e.g., unity, sovereignty, faith).
2. Constitutional Significance (What is the Preamble's role in this country's system?)
3. Summary of Key Goals (Concisely explain what the people are establishing or securing).
{comparison_section}

Write clearly and concisely. Do not use bullet points inside headings; just simple paragraphs.
"""

PROMPT_TEMPLATE_COMPARISON_SECTION = """
4. Comparison to the Indian Preamble (Briefly contrast or compare 1-2 key differences or similarities with the Preamble to the Constitution of India: 'SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC... JUSTICE, LIBERTY, EQUALITY, FRATERNITY...').
"""