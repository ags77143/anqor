"""
ai_generator.py — Focused generation. Notes+glossary upfront, quiz+flashcards on demand.
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


MAX_CHARS = 20_000


def _call(client, prompt, max_tokens=4096):
    system = "You are an elite university tutor. Respond with valid JSON only. No markdown fences, no explanation. Raw JSON starting with { or [ only."
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=max_tokens,
    )
    return r.choices[0].message.content.strip()


def _parse_obj(raw: str) -> dict:
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()
    for attempt in [raw, raw[raw.find('{'):raw.rfind('}')+1] if '{' in raw else '']:
        try:
            return json.loads(attempt)
        except Exception:
            pass
    raise ValueError("Malformed JSON. Try re-running.")


def _parse_list(raw: str) -> list:
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()
    for attempt in [raw, raw[raw.find('['):raw.rfind(']')+1] if '[' in raw else '']:
        try:
            result = json.loads(attempt)
            return result if isinstance(result, list) else []
        except Exception:
            pass
    raise ValueError("Malformed JSON. Try re-running.")


def generate_study_materials(text: str) -> dict:
    """
    Call 1: Comprehensive notes + summary
    Call 2: Detailed glossary
    Both get full 4096 token budgets.
    """
    client = get_groq_client()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[truncated]"

    # ── Call 1: Notes + summary ───────────────────────────────────────────────
    p1 = f"""From this lecture produce a JSON object with these keys:

{{
  "title": "specific descriptive title",
  "summary": "7-9 sentence executive summary covering every major theme, argument, finding and conclusion. Be specific, not vague.",
  "notes": "Write deeply comprehensive markdown study notes a student could use to ace an exam without reading anything else. Structure with ## main sections and ### subsections. For each concept: define it precisely, explain how it works, give examples, explain why it matters, connect it to other concepts. Include: all terminology, any formulas or frameworks, step-by-step processes, comparisons between concepts, edge cases, real-world applications. End with a ## Key Takeaways section. MINIMUM 1200 words. Do not summarise — teach."
}}

LECTURE:
{text}"""

    r1 = _parse_obj(_call(client, p1, max_tokens=4096))

    # ── Call 2: Glossary ──────────────────────────────────────────────────────
    p2 = f"""From this lecture produce a JSON object with one key:

{{
  "glossary": [
    {{
      "term": "exact term as used in the lecture",
      "definition": "Write 3-5 sentences: what it means precisely, where it comes from or why it exists, how it relates to other concepts in this lecture, and when/how it is applied. Be thorough."
    }}
  ]
}}

Include 15-20 terms. Cover every important concept, technique, person, theory, or framework mentioned.

LECTURE:
{text}"""

    r2 = _parse_obj(_call(client, p2, max_tokens=4096))

    return {
        "title": r1.get("title", "Untitled Lecture"),
        "summary": r1.get("summary", ""),
        "notes": r1.get("notes", ""),
        "glossary": r2.get("glossary", []),
        "quiz": [],
        "flashcards": [],
    }


def generate_quiz(text: str) -> list:
    """Dedicated call for quiz — full token budget."""
    client = get_groq_client()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = f"""From this lecture create a challenging and comprehensive quiz. Return a JSON array:

[
  {{
    "question": "Clear, specific question testing real understanding (not just memorisation)",
    "options": ["Plausible option A", "Plausible option B", "Plausible option C", "Plausible option D"],
    "answer": "Exact text of correct option",
    "explanation": "2-3 sentences: why this answer is correct, why each wrong option is wrong, and what the underlying concept is."
  }}
]

Requirements:
- 15-18 questions
- Cover all major topics from the lecture
- Mix: 30% recall, 40% understanding, 30% application/analysis
- All 4 options must be genuinely plausible — no obviously wrong options
- Questions should range from straightforward to challenging

LECTURE:
{text}"""

    return _parse_list(_call(client, prompt, max_tokens=4096))


def generate_flashcards(text: str) -> list:
    """Dedicated call for flashcards — full token budget."""
    client = get_groq_client()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = f"""From this lecture create comprehensive flashcards for active recall studying. Return a JSON array:

[
  {{
    "front": "A specific question or prompt (not just a term — phrase it as something to actively recall)",
    "back": "Complete answer in 2-4 sentences. Include the definition, context, significance, and a memory hook or example where helpful."
  }}
]

Requirements:
- 22-28 flashcards
- Cover every important concept, definition, process, and relationship
- Front should be a question or prompt, not just a word
- Back should be genuinely useful, not a one-liner
- Include cards for: key terms, processes, comparisons, applications, common mistakes

LECTURE:
{text}"""

    return _parse_list(_call(client, prompt, max_tokens=4096))
