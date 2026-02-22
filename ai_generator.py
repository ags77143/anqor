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


# Max characters to send to Groq (Llama 3 70B context ~8k tokens ≈ 32k chars)
MAX_CHARS = 28_000


def generate_study_materials(text: str) -> dict:
    """
    Send lecture text to Groq and return structured study materials as a dict.
    """
    client = get_groq_client()

    # Truncate if needed
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[transcript truncated due to length]"

    system_prompt = """You are an expert study assistant and university tutor. 
Your job is to transform raw lecture content into comprehensive, high-quality study materials.
Always respond with ONLY valid JSON — no markdown fences, no explanation, no preamble.
Be thorough, accurate, and pedagogically excellent."""

    user_prompt = f"""Analyse this lecture content and generate comprehensive study materials.

LECTURE CONTENT:
{text}

Respond with this exact JSON structure (all fields required):

{{
  "title": "A concise descriptive title for this lecture",
  "summary": "A 3-4 sentence TL;DR of the key message and main points",
  "notes": "Comprehensive, well-structured markdown study notes. Use ## for main sections, ### for subsections. Include all key concepts, explanations, examples, and important details. Should be thorough enough to study from without the original. Minimum 500 words.",
  "glossary": [
    {{"term": "Term name", "definition": "Clear, complete definition in context of this lecture"}}
  ],
  "quiz": [
    {{
      "question": "Full question text?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "answer": "The correct option text (copy exactly from options)",
      "explanation": "Why this answer is correct and others are wrong"
    }}
  ],
  "flashcards": [
    {{"front": "Term or concept", "back": "Definition or explanation"}}
  ],
  "exam_topics": "Bullet list of the most likely exam topics, one per line, starting with -"
}}

Requirements:
- glossary: 8-15 key terms
- quiz: 10-12 questions, mix of difficulty, 4 options each, plausible distractors
- flashcards: 15-20 cards covering all key concepts
- exam_topics: 8-12 high-priority topics
- notes: must be genuinely comprehensive — a student should be able to study this alone"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()

    # Strip any accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to salvage partial JSON
        try:
            # Find the first { and last }
            start = raw.index("{")
            end = raw.rindex("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            raise ValueError(
                "AI returned malformed JSON. This can happen with very short inputs. "
                "Try adding more content or re-running."
            )
