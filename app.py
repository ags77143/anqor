import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Anqorr",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color: #f5f0e8 !important; color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
#MainMenu, footer, header, section[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }

/* Top nav */
.aq-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 2rem; background: #ede8df;
    border-bottom: 1px solid #d9d2c4; margin-bottom: 1.5rem;
    position: sticky; top: 0; z-index: 999;
}
.aq-nav-logo { font-family: 'Lora', serif; font-weight: 600; font-size: 1.5rem; color: #2c2416; letter-spacing: -0.02em; }
.aq-nav-logo span { color: #c17b2e; }
.aq-nav-links { display: flex; gap: 0.4rem; align-items: center; }
.aq-nav-email { font-size: 0.75rem; color: #8c7d65; }

/* Nav buttons via streamlit — override to look inline */
.aq-navbtn > div > button {
    background: transparent !important; color: #2c2416 !important;
    border: none !important; font-weight: 600 !important; font-size: 0.88rem !important;
    text-transform: none !important; letter-spacing: 0 !important;
    padding: 0.4rem 0.9rem !important; border-radius: 6px !important;
    box-shadow: none !important;
}
.aq-navbtn > div > button:hover { background: #d9d2c4 !important; transform: none !important; box-shadow: none !important; }
.aq-navbtn-active > div > button { background: #2c2416 !important; color: #f5f0e8 !important; }

/* Main layout */
.aq-main { padding: 0 1.5rem 2rem 1.5rem; }

/* Section label */
.aq-section { font-weight: 700; font-size: 0.68rem; color: #8c7d65; letter-spacing: 0.12em;
    text-transform: uppercase; margin: 1.2rem 0 0.5rem 0; padding-bottom: 0.3rem; border-bottom: 1px solid #d9d2c4; }

/* Main buttons */
.stButton > button { background: #2c2416 !important; color: #f5f0e8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.85rem !important; text-transform: none !important; letter-spacing: 0.01em !important;
    border: none !important; border-radius: 8px !important; padding: 0.55rem 1.4rem !important; transition: all 0.15s !important; }
.stButton > button:hover { background: #3d3320 !important; transform: translateY(-1px) !important; box-shadow: 0 3px 12px rgba(44,36,22,0.2) !important; }
.stButton > button:disabled { background: #d9d2c4 !important; color: #8c7d65 !important; transform: none !important; box-shadow: none !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea { background: #faf7f2 !important; border: 1.5px solid #d9d2c4 !important;
    border-radius: 8px !important; color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #c17b2e !important; box-shadow: 0 0 0 3px rgba(193,123,46,0.1) !important; }
[data-testid="stFileUploader"] { background: #faf7f2 !important; border: 1.5px dashed #d9d2c4 !important; border-radius: 8px !important; }
div[data-baseweb="select"] > div { background: #faf7f2 !important; border-color: #d9d2c4 !important; border-radius: 8px !important; }
div[data-baseweb="select"] * { color: #2c2416 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1.5px solid #d9d2c4 !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #8c7d65 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.8rem !important; border: none !important; padding: 0.65rem 1.1rem !important; }
.stTabs [aria-selected="true"] { color: #2c2416 !important; border-bottom: 2px solid #c17b2e !important; }

/* Cards */
.aq-card { background: #faf7f2; border: 1px solid #e0d9cc; border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem; }
.aq-card-accent { border-left: 3px solid #c17b2e; }
.aq-term { font-weight: 700; color: #c17b2e; font-size: 0.92rem; }
.aq-def { color: #5a4f3c; font-size: 0.83rem; margin-top: 0.2rem; line-height: 1.6; }
.aq-q-num { font-size: 0.68rem; color: #8c7d65; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.aq-question { font-weight: 700; font-size: 0.92rem; color: #2c2416; margin-bottom: 0.75rem; }
.aq-option { display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 0.85rem;
    background: #f5f0e8; border: 1px solid #d9d2c4; border-radius: 6px; margin-bottom: 0.35rem; font-size: 0.83rem; color: #3d3320; }
.aq-option-label { font-weight: 700; color: #8c7d65; font-size: 0.72rem; min-width: 1rem; }
.aq-answer-box { background: #fdf3e3; border: 1px solid #e8c98a; border-radius: 6px;
    padding: 0.65rem 1rem; margin-top: 0.5rem; font-size: 0.82rem; color: #8a5c0a; }
.aq-flashcard { background: #faf7f2; border: 1.5px solid #d9d2c4; border-radius: 12px;
    padding: 2rem 1.5rem; text-align: center; min-height: 160px;
    display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 0.8rem; }
.aq-flashcard-label { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #8c7d65; margin-bottom: 0.7rem; }
.aq-flashcard-text { font-family: 'Lora', serif; font-size: 1.1rem; color: #2c2416; line-height: 1.5; }
.aq-info { background: #eef4fb; border: 1px solid #bdd4ee; border-radius: 6px; padding: 0.65rem 1rem; font-size: 0.82rem; color: #2a5f9e; margin-bottom: 1rem; }
.aq-warn { background: #fdf3e3; border: 1px solid #e8c98a; border-radius: 6px; padding: 0.65rem 1rem; font-size: 0.82rem; color: #8a5c0a; margin-bottom: 1rem; }
.aq-exam-topic { display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.5rem 0; border-bottom: 1px solid #e0d9cc; font-size: 0.85rem; color: #3d3320; }
.aq-bullet { color: #c17b2e; flex-shrink: 0; }
.stProgress > div > div { background: #c17b2e !important; }
.stRadio label { font-size: 0.85rem !important; color: #3d3320 !important; }
.stMarkdown p, .stMarkdown li { font-size: 0.88rem !important; line-height: 1.75 !important; color: #3d3320 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family: 'Lora', serif !important; color: #2c2416 !important; }
.aq-page-title { font-family: 'Lora', serif; font-size: 1.6rem; font-weight: 600; color: #2c2416; margin-bottom: 0.2rem; }
.aq-page-sub { font-size: 0.8rem; color: #8c7d65; margin-bottom: 1.5rem; }

/* Chat panel */
.aq-chat-panel {
    background: #faf7f2; border: 1px solid #e0d9cc; border-radius: 12px;
    padding: 1rem; height: 100%; min-height: 500px;
    display: flex; flex-direction: column;
}
.aq-chat-title { font-family: 'Lora', serif; font-weight: 600; font-size: 1rem; color: #2c2416; margin-bottom: 0.8rem; }
.aq-chat-msg-user {
    background: #2c2416; color: #f5f0e8; border-radius: 10px 10px 2px 10px;
    padding: 0.6rem 0.9rem; font-size: 0.83rem; margin-bottom: 0.5rem;
    max-width: 85%; align-self: flex-end; margin-left: auto;
}
.aq-chat-msg-ai {
    background: #ede8df; color: #2c2416; border-radius: 10px 10px 10px 2px;
    padding: 0.6rem 0.9rem; font-size: 0.83rem; margin-bottom: 0.5rem;
    max-width: 90%; line-height: 1.55;
}
.aq-chat-empty { font-size: 0.82rem; color: #8c7d65; text-align: center; padding: 2rem 0.5rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

from auth import show_auth_page, get_supabase_client, get_current_user
from processor import extract_text_from_source
from ai_generator import generate_study_materials, get_groq_client
from db import (save_lecture, save_materials, get_user_lectures, get_lecture_materials,
                delete_lecture, get_user_subjects, create_subject, delete_subject, update_lecture_subject)

supabase = get_supabase_client()
user = get_current_user(supabase)

if not user:
    show_auth_page(supabase)
    st.stop()

for k, v in [("page", "new"), ("selected_subject", None), ("lib_selected", None), ("chat_history", []), ("chat_context", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Materials renderer ────────────────────────────────────────────────────────
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
            st.markdown(f'<div class="aq-flashcard"><div class="aq-flashcard-label">{"Answer" if flipped else "Term"} · {idx+1}/{len(flashcards)}</div><div class="aq-flashcard-text">{fc.get("back" if flipped else "front","")}</div></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("← Prev", key=f"{prefix}_fc_prev"):
                    st.session_state[idx_key] = max(0, idx-1); st.session_state[flip_key] = False; st.rerun()
            with c2:
                if st.button("Flip 🔄", key=f"{prefix}_fc_flipbtn2"):
                    st.session_state[flip_key] = not flipped; st.rerun()
            with c3:
                if st.button("Next →", key=f"{prefix}_fc_next"):
                    st.session_state[idx_key] = min(len(flashcards)-1, idx+1); st.session_state[flip_key] = False; st.rerun()

    with tab5:
        for topic in (materials.get("exam_topics") or "").split("\n"):
            clean = topic.strip().lstrip("-•*123456789. ")
            if clean:
                st.markdown(f'<div class="aq-exam-topic"><span class="aq-bullet">▸</span>{clean}</div>', unsafe_allow_html=True)

# ── Top nav ───────────────────────────────────────────────────────────────────
st.markdown('<div class="aq-nav">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3 = st.columns([2, 3, 2])

with nav_col1:
    st.markdown('<div class="aq-nav-logo">an<span>q</span>orr</div>', unsafe_allow_html=True)

with nav_col2:
    b1, b2 = st.columns(2)
    with b1:
        active_new = st.session_state["page"] == "new"
        st.markdown(f'<div class="{"aq-navbtn aq-navbtn-active" if active_new else "aq-navbtn"}">', unsafe_allow_html=True)
        if st.button("⚡ New Lecture", key="nav_new"):
            st.session_state["page"] = "new"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        active_lib = st.session_state["page"] == "lib"
        st.markdown(f'<div class="{"aq-navbtn aq-navbtn-active" if active_lib else "aq-navbtn"}">', unsafe_allow_html=True)
        if st.button("📚 My Library", key="nav_lib"):
            st.session_state["page"] = "lib"
            st.session_state["lib_selected"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with nav_col3:
    st.markdown(f'<div class="aq-nav-email" style="text-align:right;padding-top:0.5rem;">{user.email}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Page layout: content + chatbot ───────────────────────────────────────────
main_col, chat_col = st.columns([3, 1])

with main_col:
    st.markdown('<div class="aq-main">', unsafe_allow_html=True)

    # ── NEW LECTURE ───────────────────────────────────────────────────────────
    if st.session_state["page"] == "new":
        st.markdown('<div class="aq-page-title">New Lecture</div>', unsafe_allow_html=True)
        st.markdown('<div class="aq-page-sub">Upload a lecture and get full study materials instantly</div>', unsafe_allow_html=True)

        st.markdown('<div class="aq-section">1. Type of lecture</div>', unsafe_allow_html=True)
        source_type = st.radio("", ["🎬 YouTube URL", "📄 Paste Transcript", "📁 Upload File (PDF / PPTX / TXT)"], label_visibility="collapsed")

        raw_text = None
        source_ref = ""
        uploaded = None

        if "🎬" in source_type:
            yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
            st.markdown('<div class="aq-info">ℹ️ Auto-captions grabbed automatically. If none, paste transcript instead.</div>', unsafe_allow_html=True)
            if yt_url: source_ref = yt_url
        elif "📄" in source_type:
            pasted = st.text_area("Paste transcript", height=220, placeholder="Paste lecture transcript or notes...")
            if pasted: raw_text = pasted; source_ref = "pasted_transcript"
        else:
            uploaded = st.file_uploader("Upload file", type=["pdf", "pptx", "txt"])
            if uploaded: source_ref = uploaded.name

        st.markdown('<div class="aq-section">2. Lecture name</div>', unsafe_allow_html=True)
        title_input = st.text_input("", placeholder="e.g. Week 4 — Cell Biology", label_visibility="collapsed")

        st.markdown('<div class="aq-section">3. Subject folder (optional)</div>', unsafe_allow_html=True)
        subjects = get_user_subjects(supabase, user.id)
        subj_options = {s["name"]: s["id"] for s in subjects}
        chosen_subj_name = st.selectbox("", ["No subject"] + list(subj_options.keys()), label_visibility="collapsed")
        chosen_subj_id = subj_options.get(chosen_subj_name)
        new_subj_name = st.text_input("", placeholder="Or type a new subject name to create one", key="new_subj_inline", label_visibility="collapsed")

        st.markdown("")
        gen_clicked = st.button("⚡ Generate Study Materials", disabled=(not source_ref and not raw_text))

        if gen_clicked:
            if new_subj_name.strip():
                COLOURS = ["#c17b2e","#2e7bc1","#2ec17b","#c12e7b","#7b2ec1","#c1c12e"]
                chosen_subj_id = create_subject(supabase, user.id, new_subj_name.strip(), COLOURS[len(subjects) % len(COLOURS)])

            progress = st.progress(0, text="Extracting text...")
            try:
                if raw_text:
                    text = raw_text
                elif "🎬" in source_type:
                    text, detected = extract_text_from_source("youtube", url=source_ref)
                    if not title_input and detected: title_input = detected
                else:
                    text, detected = extract_text_from_source("file", file=uploaded)
                    if not title_input and detected: title_input = detected
            except Exception as e:
                st.markdown(f'<div class="aq-warn">⚠️ {str(e)}</div>', unsafe_allow_html=True)
                st.stop()

            if not text or len(text.strip()) < 100:
                st.markdown('<div class="aq-warn">⚠️ Not enough text. Try pasting the transcript manually.</div>', unsafe_allow_html=True)
                st.stop()

            progress.progress(30, text="Generating study materials...")
            try:
                materials = generate_study_materials(text)
            except Exception as e:
                st.markdown(f'<div class="aq-warn">⚠️ AI generation failed: {str(e)}</div>', unsafe_allow_html=True)
                st.stop()

            progress.progress(75, text="Saving...")
            final_title = title_input or materials.get("title", "Untitled Lecture")
            src_clean = "youtube" if "🎬" in source_type else ("transcript" if "📄" in source_type else source_ref.split(".")[-1])
            lecture_id = save_lecture(supabase, user.id, final_title, src_clean, source_ref, text, chosen_subj_id)
            save_materials(supabase, lecture_id, user.id, materials)
            progress.progress(100, text="Done!")

            st.session_state["current_materials"] = materials
            st.session_state["current_title"] = final_title
            st.session_state["chat_context"] = text[:8000]
            st.session_state["chat_history"] = []
            st.rerun()

        if "current_materials" in st.session_state:
            st.markdown(f'<div class="aq-page-title">{st.session_state.get("current_title","Lecture")}</div>', unsafe_allow_html=True)
            show_materials(st.session_state["current_materials"], prefix="new")

    # ── LIBRARY ───────────────────────────────────────────────────────────────
    elif st.session_state["page"] == "lib":
        subjects = get_user_subjects(supabase, user.id)
        subj_map = {s["id"]: s["name"] for s in subjects}

        st.markdown('<div class="aq-page-title">📚 My Library</div>', unsafe_allow_html=True)
        st.markdown('<div class="aq-page-sub">Click a lecture to view its study materials</div>', unsafe_allow_html=True)

        # Subject filter pills
        if subjects:
            st.markdown('<div class="aq-section">Filter by subject</div>', unsafe_allow_html=True)
            pill_cols = st.columns(len(subjects) + 1)
            with pill_cols[0]:
                if st.button("All", key="filter_all"):
                    st.session_state["selected_subject"] = None; st.rerun()
            for i, s in enumerate(subjects):
                with pill_cols[i+1]:
                    if st.button(s["name"], key=f"filter_{s['id']}"):
                        st.session_state["selected_subject"] = s["id"]; st.rerun()

        lectures = get_user_lectures(supabase, user.id, subject_id=st.session_state["selected_subject"])

        if not lectures:
            st.markdown('<div class="aq-info">No lectures here yet — go to ⚡ New Lecture to add one!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="aq-section">Lectures</div>', unsafe_allow_html=True)
            for lec in lectures:
                c1, c2 = st.columns([5, 1])
                with c1:
                    icon = {"youtube":"🎬","pdf":"📄","pptx":"📊","txt":"📝","transcript":"📋"}.get(lec.get("source_type",""), "📁")
                    created = lec.get("created_at","")[:10]
                    subj_label = f"  ·  {subj_map.get(lec.get('subject_id'),'')}" if not st.session_state["selected_subject"] and lec.get("subject_id") else ""
                    if st.button(f"{icon}  {lec['title']}  ·  {created}{subj_label}", key=f"lib_{lec['id']}", use_container_width=True):
                        st.session_state["lib_selected"] = lec["id"]
                        st.session_state["chat_history"] = []
                        raw = lec.get("raw_transcript", "")
                        if not raw:
                            full = get_lecture_materials(supabase, lec["id"])
                            raw = (full or {}).get("notes", "")
                        st.session_state["chat_context"] = raw[:8000]
                        st.rerun()
                with c2:
                    if st.button("🗑", key=f"del_{lec['id']}"):
                        delete_lecture(supabase, lec["id"])
                        if st.session_state.get("lib_selected") == lec["id"]:
                            st.session_state["lib_selected"] = None
                        st.rerun()
                # Move to subject
                if st.session_state.get("lib_selected") == lec["id"] and subjects:
                    move_options = ["— move to subject —"] + [s["name"] for s in subjects]
                    move_choice = st.selectbox("", move_options, key=f"move_{lec['id']}", label_visibility="collapsed")
                    if move_choice != "— move to subject —":
                        new_subj_id = next(s["id"] for s in subjects if s["name"] == move_choice)
                        update_lecture_subject(supabase, lec["id"], new_subj_id)
                        st.rerun()

            if st.session_state.get("lib_selected"):
                lec_id = st.session_state["lib_selected"]
                materials = get_lecture_materials(supabase, lec_id)
                lec_info = next((l for l in lectures if l["id"] == lec_id), {})
                if materials:
                    st.markdown("---")
                    st.markdown(f'<div class="aq-page-title">{lec_info.get("title","")}</div>', unsafe_allow_html=True)
                    show_materials(materials, prefix=f"lib_{lec_id}")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Chat panel ────────────────────────────────────────────────────────────────
with chat_col:
    st.markdown('<div class="aq-chat-panel">', unsafe_allow_html=True)
    st.markdown('<div class="aq-chat-title">💬 Ask about this lecture</div>', unsafe_allow_html=True)

    chat_history = st.session_state.get("chat_history", [])
    chat_context = st.session_state.get("chat_context", "")

    if not chat_context:
        st.markdown('<div class="aq-chat-empty">Open a lecture or generate study materials to start chatting about it.</div>', unsafe_allow_html=True)
    else:
        # Show messages
        for msg in chat_history:
            css_class = "aq-chat-msg-user" if msg["role"] == "user" else "aq-chat-msg-ai"
            st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

        # Input
        user_q = st.text_input("", placeholder="Ask anything about this lecture...", key="chat_input", label_visibility="collapsed")
        if st.button("Send", key="chat_send") and user_q.strip():
            chat_history.append({"role": "user", "content": user_q})
            try:
                client = get_groq_client()
                messages = [
                    {"role": "system", "content": f"You are a helpful study assistant. Answer questions about this lecture content concisely and clearly. Lecture content:\n\n{chat_context}"},
                ] + [{"role": m["role"], "content": m["content"]} for m in chat_history]

                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.4,
                    max_tokens=512,
                )
                answer = resp.choices[0].message.content.strip()
                chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                chat_history.append({"role": "assistant", "content": f"Sorry, something went wrong: {str(e)}"})

            st.session_state["chat_history"] = chat_history
            st.rerun()

        if chat_history and st.button("Clear chat", key="chat_clear"):
            st.session_state["chat_history"] = []
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
