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

    system_prompt = """You are an expert study assistant. You MUST respond with valid JSON only.
No markdown, no code fences, no explanation before or after. Just raw JSON starting with { and ending with }."""

    user_prompt = f"""Create study materials from this lecture content. Return ONLY a JSON object with these exact keys:

{{
  "title": "short lecture title",
  "summary": "3-4 sentence summary",
  "notes": "comprehensive markdown study notes with ## headers, minimum 400 words",
  "glossary": [
    {{"term": "word", "definition": "meaning"}}
  ],
  "quiz": [
    {{"question": "question text?", "options": ["A", "B", "C", "D"], "answer": "correct option text", "explanation": "why"}}
  ],
  "flashcards": [
    {{"front": "term", "back": "definition"}}
  ],
  "exam_topics": "- topic one\\n- topic two\\n- topic three"
}}

Rules:
- glossary: 8-12 terms
- quiz: 8-10 questions with 4 options each
- flashcards: 12-15 cards
- exam_topics: 6-10 topics, each on new line starting with -
- Return ONLY the JSON, nothing else

LECTURE CONTENT:
{text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if present
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    # Try direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object within the response
    try:
        start = raw.index('{')
        end = raw.rindex('}') + 1
        return json.loads(raw[start:end])
    except Exception:
        pass

    # Last resort: fix common issues and try again
    try:
        # Remove any text before first {
        cleaned = raw[raw.index('{'):]
        # Remove any text after last }
        cleaned = cleaned[:cleaned.rindex('}')+1]
        # Fix unescaped newlines inside strings
        cleaned = re.sub(r'(?<!\\)\n(?!["\s]*[,}\]])', ' ', cleaned)
        return json.loads(cleaned)
    except Exception:
        raise ValueError("AI returned malformed JSON. Try re-running — it usually works on the second attempt.")
