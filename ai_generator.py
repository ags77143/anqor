"""
ai_generator.py — Generate study materials using Groq.
Notes + glossary generated upfront. Quiz and flashcards on demand.
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
        raise ValueError("GROQ_API_KEY not set.")
    return Groq(api_key=api_key)


MAX_CHARS = 24_000


def _parse_json(raw: str) -> dict:
    raw = re.sub(r'^```(?:json)?\s*', '', raw.strip())
    raw = re.sub(r'\s*```$', '', raw).strip()
    try:
        return json.loads(raw)
    except Exception:
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
        raise ValueError("Malformed JSON from AI. Try re-running.")


def generate_study_materials(text: str) -> dict:
    """Generate notes, summary, glossary and exam topics only."""
    client = get_groq_client()

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[transcript truncated]"

    system = """You are an elite university tutor. Respond with valid JSON only — no markdown fences, no preamble. Raw JSON starting with { only."""

    prompt = f"""From this lecture, return a JSON object with ONLY these keys:

{{
  "title": "descriptive title for this lecture",
  "summary": "6-8 sentence summary covering all main themes, arguments, and conclusions",
  "notes": "EXTREMELY COMPREHENSIVE markdown study notes. Use ## for main sections, ### for subsections. Cover EVERY concept, definition, theory, example, formula, and detail. Explain clearly as if teaching from scratch. Include background context, all key concepts in depth, worked examples, relationships between ideas, real-world applications, common exam traps, and a summary at the end. MINIMUM 1000 words.",
  "glossary": [
    {{"term": "term", "definition": "thorough definition with context and significance — not just a one-liner"}}
  ],
  "exam_topics": "- topic one\\n- topic two\\n- topic three"
}}

Rules:
- notes: minimum 1000 words, comprehensive, do not skip anything
- glossary: 14-18 key terms with detailed definitions
- exam_topics: 10-14 specific high-priority topics
- Return ONLY the JSON

LECTURE:
{text}"""

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4096,
    )
    result = _parse_json(r.choices[0].message.content)
    # Ensure quiz and flashcards are empty so UI shows generate buttons
    result.setdefault("quiz", [])
    result.setdefault("flashcards", [])
    return result


def generate_quiz(text: str) -> list:
    """Generate quiz questions on demand."""
    client = get_groq_client()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    system = "You are an expert tutor. Respond with valid JSON only — raw JSON array, no fences."

    prompt = f"""Create a quiz from this lecture. Return ONLY a JSON array:

[
  {{"question": "full question?", "options": ["option A", "option B", "option C", "option D"], "answer": "exact correct option text", "explanation": "why this is correct and others are wrong"}}
]

Rules:
- 14-16 questions
- Mix of easy, medium, hard
- All 4 options must be plausible
- Detailed explanations

LECTURE:
{text}"""

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4096,
    )
    raw = r.choices[0].message.content.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()
    try:
        result = json.loads(raw)
        return result if isinstance(result, list) else result.get("quiz", [])
    except Exception:
        try:
            start = raw.index('[')
            end = raw.rindex(']') + 1
            return json.loads(raw[start:end])
        except Exception:
            raise ValueError("Failed to generate quiz. Try again.")


def generate_flashcards(text: str) -> list:
    """Generate flashcards on demand."""
    client = get_groq_client()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    system = "You are an expert tutor. Respond with valid JSON only — raw JSON array, no fences."

    prompt = f"""Create flashcards from this lecture. Return ONLY a JSON array:

[
  {{"front": "term or concept", "back": "thorough explanation, minimum 2 sentences"}}
]

Rules:
- 20-25 flashcards
- Cover every important concept
- Backs should be genuinely useful, not just a one-liner

LECTURE:
{text}"""

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4096,
    )
    raw = r.choices[0].message.content.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()
    try:
        result = json.loads(raw)
        return result if isinstance(result, list) else result.get("flashcards", [])
    except Exception:
        try:
            start = raw.index('[')
            end = raw.rindex(']') + 1
            return json.loads(raw[start:end])
        except Exception:
            raise ValueError("Failed to generate flashcards. Try again.")
