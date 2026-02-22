"""
db.py — Supabase database operations.
"""

# ── Subjects ─────────────────────────────────────────────────────────────────

def get_user_subjects(supabase, user_id: str) -> list:
    result = supabase.table("subjects") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("name") \
        .execute()
    return result.data or []

def create_subject(supabase, user_id: str, name: str, colour: str = "#6c63ff") -> str:
    result = supabase.table("subjects").insert({
        "user_id": user_id,
        "name": name,
        "colour": colour,
    }).execute()
    return result.data[0]["id"]

def delete_subject(supabase, subject_id: str):
    supabase.table("subjects").delete().eq("id", subject_id).execute()

# ── Lectures ──────────────────────────────────────────────────────────────────

def save_lecture(supabase, user_id: str, title: str, source_type: str, source_ref: str, raw_transcript: str, subject_id: str = None) -> str:
    result = supabase.table("lectures").insert({
        "user_id": user_id,
        "subject_id": subject_id,
        "title": title,
        "source_type": source_type,
        "source_ref": source_ref,
        "raw_transcript": raw_transcript[:50_000],
    }).execute()
    return result.data[0]["id"]

def save_materials(supabase, lecture_id: str, user_id: str, materials: dict):
    supabase.table("study_materials").insert({
        "lecture_id": lecture_id,
        "user_id": user_id,
        "summary": materials.get("summary", ""),
        "notes": materials.get("notes", ""),
        "glossary": materials.get("glossary", []),
        "quiz": materials.get("quiz", []),
        "flashcards": materials.get("flashcards", []),
        "exam_topics": materials.get("exam_topics", ""),
    }).execute()

def get_user_lectures(supabase, user_id: str, subject_id: str = None) -> list:
    q = supabase.table("lectures") \
        .select("id, title, source_type, source_ref, subject_id, created_at") \
        .eq("user_id", user_id)
    if subject_id:
        q = q.eq("subject_id", subject_id)
    result = q.order("created_at", desc=True).execute()
    return result.data or []

def get_lecture_materials(supabase, lecture_id: str) -> dict:
    result = supabase.table("study_materials") \
        .select("*") \
        .eq("lecture_id", lecture_id) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None

def delete_lecture(supabase, lecture_id: str):
    supabase.table("lectures").delete().eq("id", lecture_id).execute()
