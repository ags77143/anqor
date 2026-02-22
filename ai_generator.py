"""
ai_generator.py — Generate study materials using Groq (Llama 3).
"""
import os
import json
import re
from groq import Groq


def get_groq_client() -> Groq:
    import streamlit as _st
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            api_key = _st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Add it to your .env or Streamlit secrets.")
    return Groq(api_key=api_key)


MAX_CHARS = 24_000


def generate_study_materials(text: str) -> dict:
    client = get_groq_client()

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[transcript truncated]"

    system_prompt = """You are an elite university tutor and study materials expert. You MUST respond with valid JSON only.
No markdown, no code fences, no explanation before or after. Just raw JSON starting with { and ending with }.
Your study materials should be genuinely excellent — the kind that help students ace exams."""

    user_prompt = f"""Create comprehensive, high-quality study materials from this lecture. Return ONLY a JSON object:

{{
  "title": "descriptive lecture title",
  "summary": "5-6 sentence summary covering all main themes, key arguments, and conclusions",
  "notes": "VERY COMPREHENSIVE markdown study notes. Use ## for main sections, ### for subsections. Must include: all key concepts explained in depth, important definitions, examples, diagrams described in text, relationships between concepts, real-world applications, common misconceptions, and anything a student needs to know for an exam. MINIMUM 800 words. Do not skip anything important.",
  "glossary": [
    {{"term": "word", "definition": "thorough definition with context and why it matters"}}
  ],
  "quiz": [
    {{"question": "question text?", "options": ["full option A", "full option B", "full option C", "full option D"], "answer": "exact correct option text", "explanation": "detailed explanation of why this is correct and why others are wrong"}}
  ],
  "flashcards": [
    {{"front": "term or concept", "back": "thorough explanation, not just a one-liner"}}
  ],
  "exam_topics": "- topic one\\n- topic two\\n- topic three"
}}

Requirements — do not cut corners:
- notes: MINIMUM 800 words, cover everything, use proper markdown headers and structure
- glossary: 12-18 key terms with thorough definitions
- quiz: 12-15 questions, mix of easy/medium/hard, 4 plausible options each, detailed explanations
- flashcards: 18-25 cards covering every important concept
- exam_topics: 10-14 high-priority topics a student should revise
- Return ONLY the JSON, nothing else

LECTURE CONTENT:
{text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=8192,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    try:
        start = raw.index('{')
        end = raw.rindex('}') + 1
        return json.loads(raw[start:end])
    except Exception:
        pass

    try:
        cleaned = raw[raw.index('{'):]
        cleaned = cleaned[:cleaned.rindex('}')+1]
        cleaned = re.sub(r'(?<!\\)\n(?!["\\s]*[,}\\]])', ' ', cleaned)
        return json.loads(cleaned)
    except Exception:
        raise ValueError("AI returned malformed JSON. Try re-running — it usually works on the second attempt.")
