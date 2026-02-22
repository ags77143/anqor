"""
db.py — Supabase database operations.
"""
import json


def save_lecture(supabase, user_id: str, title: str, source_type: str, source_ref: str, raw_transcript: str) -> str:
    """Insert a lecture record and return its ID."""
    result = supabase.table("lectures").insert({
        "user_id": user_id,
        "title": title,
        "source_type": source_type,
        "source_ref": source_ref,
        "raw_transcript": raw_transcript[:50_000],  # cap at 50k chars
    }).execute()
    return result.data[0]["id"]


def save_materials(supabase, lecture_id: str, user_id: str, materials: dict):
    """Insert generated study materials linked to a lecture."""
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


def get_user_lectures(supabase, user_id: str) -> list:
    """Fetch all lectures for a user, newest first."""
    result = supabase.table("lectures") \
        .select("id, title, source_type, source_ref, created_at") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def get_lecture_materials(supabase, lecture_id: str) -> dict | None:
    """Fetch study materials for a specific lecture."""
    result = supabase.table("study_materials") \
        .select("*") \
        .eq("lecture_id", lecture_id) \
        .limit(1) \
        .execute()
    if result.data:
        return result.data[0]
    return None


def delete_lecture(supabase, lecture_id: str):
    """Delete a lecture (cascade deletes materials too via FK)."""
    supabase.table("lectures").delete().eq("id", lecture_id).execute()
