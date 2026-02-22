import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Anqorr",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color: #f5f0e8 !important; color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 1000px !important; }
section[data-testid="stSidebar"] { background: #ede8df !important; border-right: 1px solid #d9d2c4 !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #5a4f3c !important; font-size: 0.83rem !important; }
section[data-testid="stSidebar"] .stButton > button { background: transparent !important; color: #2c2416 !important; border: 1px solid #c8bfae !important; font-weight: 500 !important; text-transform: none !important; letter-spacing: 0 !important; font-size: 0.85rem !important; padding: 0.5rem 0.9rem !important; }
section[data-testid="stSidebar"] .stButton > button:hover { background: #d9d2c4 !important; transform: none !important; box-shadow: none !important; }
.aq-logo { font-family: 'Lora', serif; font-weight: 600; font-size: 1.7rem; color: #2c2416; letter-spacing: -0.02em; margin-bottom: 0.1rem; }
.aq-logo span { color: #c17b2e; }
.aq-tagline { font-size: 0.72rem; color: #8c7d65; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.5rem; }
.aq-section { font-weight: 700; font-size: 0.72rem; color: #8c7d65; letter-spacing: 0.12em; text-transform: uppercase; margin: 1.4rem 0 0.6rem 0; padding-bottom: 0.3rem; border-bottom: 1px solid #d9d2c4; }
.stButton > button { background: #2c2416 !important; color: #f5f0e8 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.85rem !important; letter-spacing: 0.02em !important; text-transform: none !important; border: none !important; border-radius: 8px !important; padding: 0.55rem 1.4rem !important; transition: all 0.15s ease !important; }
.stButton > button:hover { background: #3d3320 !important; transform: translateY(-1px) !important; box-shadow: 0 3px 12px rgba(44,36,22,0.2) !important; }
.stButton > button:disabled { background: #d9d2c4 !important; color: #8c7d65 !important; }
.stTextInput input, .stTextArea textarea { background: #faf7f2 !important; border: 1.5px solid #d9d2c4 !important; border-radius: 8px !important; color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #c17b2e !important; box-shadow: 0 0 0 3px rgba(193,123,46,0.1) !important; }
[data-testid="stFileUploader"] { background: #faf7f2 !important; border: 1.5px dashed #d9d2c4 !important; border-radius: 8px !important; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1.5px solid #d9d2c4 !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #8c7d65 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.8rem !important; border: none !important; padding: 0.65rem 1.1rem !important; }
.stTabs [aria-selected="true"] { color: #2c2416 !important; border-bottom: 2px solid #c17b2e !important; }
.aq-card { background: #faf7f2; border: 1px solid #e0d9cc; border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem; }
.aq-card-accent { border-left: 3px solid #c17b2e; }
.aq-term { font-weight: 700; color: #c17b2e; font-size: 0.92rem; }
.aq-def { color: #5a4f3c; font-size: 0.83rem; margin-top: 0.2rem; line-height: 1.6; }
.aq-q-num { font-size: 0.68rem; color: #8c7d65; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.aq-question { font-weight: 700; font-size: 0.92rem; color: #2c2416; margin-bottom: 0.75rem; }
.aq-option { display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 0.85rem; background: #f5f0e8; border: 1px solid #d9d2c4; border-radius: 6px; margin-bottom: 0.35rem; font-size: 0.83rem; color: #3d3320; }
.aq-option-label { font-weight: 700; color: #8c7d65; font-size: 0.72rem; min-width: 1rem; }
.aq-answer-box { background: #fdf3e3; border: 1px solid #e8c98a; border-radius: 6px; padding: 0.65rem 1rem; margin-top: 0.5rem; font-size: 0.82rem; color: #8a5c0a; }
.aq-flashcard { background: #faf7f2; border: 1.5px solid #d9d2c4; border-radius: 12px; padding: 2rem 1.5rem; text-align: center; min-height: 160px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 0.8rem; }
.aq-flashcard-label { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #8c7d65; margin-bottom: 0.7rem; }
.aq-flashcard-text { font-family: 'Lora', serif; font-size: 1.1rem; color: #2c2416; line-height: 1.5; }
.aq-info { background: #eef4fb; border: 1px solid #bdd4ee; border-radius: 6px; padding: 0.65rem 1rem; font-size: 0.82rem; color: #2a5f9e; margin-bottom: 1rem; }
.aq-warn { background: #fdf3e3; border: 1px solid #e8c98a; border-radius: 6px; padding: 0.65rem 1rem; font-size: 0.82rem; color: #8a5c0a; margin-bottom: 1rem; }
.aq-exam-topic { display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.5rem 0; border-bottom: 1px solid #e0d9cc; font-size: 0.85rem; color: #3d3320; }
.aq-bullet { color: #c17b2e; flex-shrink: 0; }
.stProgress > div > div { background: #c17b2e !important; }
.stRadio label { font-size: 0.85rem !important; color: #3d3320 !important; }
div[data-baseweb="select"] { background: #faf7f2 !important; }
div[data-baseweb="select"] * { background: #faf7f2 !important; color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stMarkdown p, .stMarkdown li { font-size: 0.88rem !important; line-height: 1.75 !important; color: #3d3320 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family: 'Lora', serif !important; color: #2c2416 !important; }
.aq-page-title { font-family: 'Lora', serif; font-size: 1.6rem; font-weight: 600; color: #2c2416; margin-bottom: 0.2rem; }
.aq-page-sub { font-size: 0.8rem; color: #8c7d65; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

from auth import show_auth_page, get_supabase_client, get_current_user
from processor import extract_text_from_source
from ai_generator import generate_study_materials
from db import (save_lecture, save_materials, get_user_lectures, get_lecture_materials,
                delete_lecture, get_user_subjects, create_subject, delete_subject)

supabase = get_supabase_client()
user = get_current_user(supabase)

if not user:
    show_auth_page(supabase)
    st.stop()

for k, v in [("page", "new"), ("selected_subject", None), ("lib_selected", None),
             ("lib_quiz_revealed", {}), ("lib_fc_index", 0), ("lib_fc_flipped", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Shared materials renderer ─────────────────────────────────────────────────
def show_materials(materials, prefix):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Notes", "📖 Glossary", "❓ Quiz", "🃏 Flashcards", "🎯 Exam Topics"])

    with tab1:
        if materials.get("summary"):
            st.markdown(f'<div class="aq-card aq-card-accent"><strong style="color:#c17b2e;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;">TL;DR</strong><br/>{materials["summary"]}</div>', unsafe_allow_html=True)
        st.markdown(materials.get("notes", "No notes generated."))

    with tab2:
        for item in (materials.get("glossary") or []):
            st.markdown(f'<div class="aq-card"><div class="aq-term">{item.get("term","")}</div><div class="aq-def">{item.get("definition","")}</div></div>', unsafe_allow_html=True)

    with tab3:
        quiz = materials.get("quiz") or []
        qr_key = f"{prefix}_qr"
        if qr_key not in st.session_state:
            st.session_state[qr_key] = {}
        for i, q in enumerate(quiz):
            st.markdown(f'<div class="aq-card"><div class="aq-q-num">Question {i+1} of {len(quiz)}</div><div class="aq-question">{q.get("question","")}</div>', unsafe_allow_html=True)
            for j, opt in enumerate(q.get("options", [])):
                lbl = ["A","B","C","D"][j] if j < 4 else str(j+1)
                st.markdown(f'<div class="aq-option"><span class="aq-option-label">{lbl}</span>{opt}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            revealed = st.session_state[qr_key].get(i, False)
            if st.button(f"{'Hide' if revealed else 'Show'} Answer", key=f"{prefix}_qbtn_{i}"):
                st.session_state[qr_key][i] = not revealed
                st.rerun()
            if revealed:
                st.markdown(f'<div class="aq-answer-box">✓ <strong>{q.get("answer","")}</strong><br/><span style="color:#5a4f3c;font-size:0.8rem;">{q.get("explanation","")}</span></div>', unsafe_allow_html=True)

    with tab4:
        flashcards = materials.get("flashcards") or []
        if flashcards:
            idx_key = f"{prefix}_fc_idx"
            flip_key = f"{prefix}_fc_flip"
            if idx_key not in st.session_state: st.session_state[idx_key] = 0
            if flip_key not in st.session_state: st.session_state[flip_key] = False
            idx = st.session_state[idx_key]
            flipped = st.session_state[flip_key]
            fc = flashcards[idx]
            side = "back" if flipped else "front"
            label = "Answer" if flipped else "Term"
            st.markdown(f'<div class="aq-flashcard"><div class="aq-flashcard-label">{label} · {idx+1}/{len(flashcards)}</div><div class="aq-flashcard-text">{fc.get(side,"")}</div></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("← Prev", key=f"{prefix}_fc_prev"):
                    st.session_state[idx_key] = max(0, idx-1)
                    st.session_state[flip_key] = False
                    st.rerun()
            with c2:
                if st.button("Flip 🔄", key=f"{prefix}_fc_flip"):
                    st.session_state[flip_key] = not flipped
                    st.rerun()
            with c3:
                if st.button("Next →", key=f"{prefix}_fc_next"):
                    st.session_state[idx_key] = min(len(flashcards)-1, idx+1)
                    st.session_state[flip_key] = False
                    st.rerun()

    with tab5:
        for topic in (materials.get("exam_topics") or "").split("\n"):
            clean = topic.strip().lstrip("-•*123456789. ")
            if clean:
                st.markdown(f'<div class="aq-exam-topic"><span class="aq-bullet">▸</span>{clean}</div>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="aq-logo">an<span>q</span>orr</div>', unsafe_allow_html=True)
    st.markdown('<div class="aq-tagline">Study smarter</div>', unsafe_allow_html=True)

    if st.button("⚡  New Lecture", key="nav_new", use_container_width=True):
        st.session_state["page"] = "new"
        st.rerun()
    st.markdown("")
    if st.button("📚  All Lectures", key="nav_lib", use_container_width=True):
        st.session_state["page"] = "lib"
        st.session_state["selected_subject"] = None
        st.session_state["lib_selected"] = None
        st.rerun()

    st.markdown('<div class="aq-section">Subjects</div>', unsafe_allow_html=True)
    subjects = get_user_subjects(supabase, user.id)
    COLOURS = ["#c17b2e","#2e7bc1","#2ec17b","#c12e7b","#7b2ec1","#c1c12e"]

    for subj in subjects:
        col1, col2 = st.columns([4, 1])
        active = st.session_state["selected_subject"] == subj["id"]
        with col1:
            label = f"{'▸ ' if active else ''}{subj['name']}"
            if st.button(label, key=f"subj_{subj['id']}", use_container_width=True):
                st.session_state["selected_subject"] = subj["id"]
                st.session_state["page"] = "lib"
                st.session_state["lib_selected"] = None
                st.rerun()
        with col2:
            if st.button("✕", key=f"delsubj_{subj['id']}"):
                delete_subject(supabase, subj["id"])
                if st.session_state["selected_subject"] == subj["id"]:
                    st.session_state["selected_subject"] = None
                st.rerun()

    new_subj = st.text_input("", placeholder="+ New subject", key="new_subj_input", label_visibility="collapsed")
    if new_subj and st.button("Add", key="add_subj", use_container_width=True):
        idx = len(subjects) % len(COLOURS)
        create_subject(supabase, user.id, new_subj.strip(), COLOURS[idx])
        st.rerun()

    st.markdown("---")
    st.markdown(f'<div style="font-size:0.72rem;color:#8c7d65;">{user.email}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW LECTURE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state["page"] == "new":
    st.markdown('<div class="aq-page-title">New Lecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="aq-page-sub">Upload a lecture and get full study materials in seconds</div>', unsafe_allow_html=True)

    subjects = get_user_subjects(supabase, user.id)
    subj_options = {s["name"]: s["id"] for s in subjects}
    subj_names = ["No subject"] + list(subj_options.keys())
    chosen_subj_name = st.selectbox("Subject folder", subj_names)
    chosen_subj_id = subj_options.get(chosen_subj_name) if chosen_subj_name != "No subject" else None

    st.markdown('<div class="aq-section">Input Source</div>', unsafe_allow_html=True)
    source_type = st.radio("", ["🎬 YouTube URL", "📄 Paste Transcript", "📁 Upload File (PDF / PPTX / TXT)"], label_visibility="collapsed")

    raw_text = None
    source_ref = ""
    title_input = st.text_input("Lecture title (optional)", placeholder="e.g. Week 4 — Cell Biology")

    if "🎬" in source_type:
        yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        st.markdown('<div class="aq-info">ℹ️ Auto-captions are grabbed automatically. If none exist, paste the transcript instead.</div>', unsafe_allow_html=True)
        if yt_url:
            source_ref = yt_url
    elif "📄" in source_type:
        pasted = st.text_area("Paste transcript", height=240, placeholder="Paste lecture transcript, notes, or any text...")
        if pasted:
            raw_text = pasted
            source_ref = "pasted_transcript"
    else:
        uploaded = st.file_uploader("Upload file", type=["pdf", "pptx", "txt"])
        if uploaded:
            source_ref = uploaded.name

    st.markdown("")
    gen_clicked = st.button("⚡ Generate Study Materials", disabled=(not source_ref and not raw_text))

    if gen_clicked:
        progress = st.progress(0, text="Extracting text...")
        try:
            if raw_text:
                text = raw_text
            elif "🎬" in source_type:
                text, detected_title = extract_text_from_source("youtube", url=source_ref)
                if not title_input and detected_title:
                    title_input = detected_title
            else:
                text, detected_title = extract_text_from_source("file", file=uploaded)
                if not title_input and detected_title:
                    title_input = detected_title
        except Exception as e:
            st.markdown(f'<div class="aq-warn">⚠️ {str(e)}</div>', unsafe_allow_html=True)
            st.stop()

        if not text or len(text.strip()) < 100:
            st.markdown('<div class="aq-warn">⚠️ Not enough text found. Try pasting the transcript manually.</div>', unsafe_allow_html=True)
            st.stop()

        progress.progress(30, text="Generating study materials...")
        try:
            materials = generate_study_materials(text)
        except Exception as e:
            st.markdown(f'<div class="aq-warn">⚠️ AI generation failed: {str(e)}</div>', unsafe_allow_html=True)
            st.stop()

        progress.progress(75, text="Saving...")
        final_title = title_input or materials.get("title", "Untitled Lecture")
        src_type_clean = "youtube" if "🎬" in source_type else ("transcript" if "📄" in source_type else source_ref.split(".")[-1])
        lecture_id = save_lecture(supabase, user.id, final_title, src_type_clean, source_ref, text, chosen_subj_id)
        save_materials(supabase, lecture_id, user.id, materials)
        progress.progress(100, text="Done!")
        st.session_state["current_lecture_id"] = lecture_id
        st.session_state["current_materials"] = materials
        st.session_state["current_title"] = final_title

    if "current_materials" in st.session_state:
        materials = st.session_state["current_materials"]
        title = st.session_state.get("current_title", "Lecture")
        st.markdown(f'<div class="aq-section">{title}</div>', unsafe_allow_html=True)
        show_materials(materials, prefix="new")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "lib":
    selected_subj_id = st.session_state["selected_subject"]
    subjects = get_user_subjects(supabase, user.id)
    subj_map = {s["id"]: s["name"] for s in subjects}

    if selected_subj_id:
        subj_name = subj_map.get(selected_subj_id, "Subject")
        st.markdown(f'<div class="aq-page-title">📁 {subj_name}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="aq-page-title">📚 All Lectures</div>', unsafe_allow_html=True)
    st.markdown('<div class="aq-page-sub">Click a lecture to view its study materials</div>', unsafe_allow_html=True)

    lectures = get_user_lectures(supabase, user.id, subject_id=selected_subj_id)

    if not lectures:
        st.markdown('<div class="aq-info">No lectures here yet. Go to ⚡ New Lecture to add one!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="aq-section">Lectures</div>', unsafe_allow_html=True)
        for lec in lectures:
            col1, col2 = st.columns([5, 1])
            with col1:
                created = lec.get("created_at", "")[:10]
                src = lec.get("source_type", "")
                icon = {"youtube": "🎬", "pdf": "📄", "pptx": "📊", "txt": "📝", "transcript": "📋"}.get(src, "📁")
                subj_label = f"  ·  {subj_map.get(lec.get('subject_id'), '')}" if not selected_subj_id and lec.get("subject_id") else ""
                if st.button(f"{icon}  {lec['title']}  ·  {created}{subj_label}", key=f"lib_{lec['id']}", use_container_width=True):
                    st.session_state["lib_selected"] = lec["id"]
                    st.session_state["lib_quiz_revealed"] = {}
                    st.session_state["lib_fc_index"] = 0
                    st.session_state["lib_fc_flipped"] = False
                    st.rerun()
            with col2:
                if st.button("🗑", key=f"del_{lec['id']}"):
                    delete_lecture(supabase, lec["id"])
                    if st.session_state.get("lib_selected") == lec["id"]:
                        st.session_state["lib_selected"] = None
                    st.rerun()

        if st.session_state.get("lib_selected"):
            lec_id = st.session_state["lib_selected"]
            materials = get_lecture_materials(supabase, lec_id)
            lec_info = next((l for l in lectures if l["id"] == lec_id), {})
            if materials:
                st.markdown(f'<div class="aq-section">{lec_info.get("title","")}</div>', unsafe_allow_html=True)
                show_materials(materials, prefix=f"lib_{lec_id}")
