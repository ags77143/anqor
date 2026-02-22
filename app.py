import streamlit as st
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first) ──────────────────────────────────────────────
st.set_page_config(
    page_title="Anqorr",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1100px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e30 !important;
}
section[data-testid="stSidebar"] * { color: #e8e6f0 !important; }

/* ── Logo / hero title ── */
.sf-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #c8f542 0%, #42f5a7 60%, #42c8f5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.1rem;
}
.sf-tagline {
    font-size: 0.72rem;
    color: #555570;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── Section headers ── */
.sf-section {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #c8f542;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 1.6rem 0 0.8rem 0;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid #1e1e30;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 6px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #c8f542 !important;
    box-shadow: 0 0 0 2px rgba(200,245,66,0.12) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #0f0f1a !important;
    border: 1px dashed #2a2a40 !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #c8f542 !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #d8ff55 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(200,245,66,0.3) !important;
}
.stButton > button:disabled {
    background: #2a2a40 !important;
    color: #555570 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1e1e30 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #555570 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 0.7rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    color: #c8f542 !important;
    border-bottom: 2px solid #c8f542 !important;
}

/* ── Cards ── */
.sf-card {
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.sf-card-accent {
    border-left: 3px solid #c8f542;
}

/* ── Glossary term ── */
.sf-term {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #c8f542;
    font-size: 0.95rem;
}
.sf-def {
    color: #a0a0c0;
    font-size: 0.82rem;
    margin-top: 0.2rem;
    line-height: 1.6;
}

/* ── Quiz ── */
.sf-q-num {
    font-size: 0.7rem;
    color: #555570;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.sf-question {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8e6f0;
    margin-bottom: 0.8rem;
}
.sf-option {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.55rem 0.9rem;
    background: #13131f;
    border: 1px solid #2a2a40;
    border-radius: 6px;
    margin-bottom: 0.4rem;
    cursor: pointer;
    font-size: 0.83rem;
    color: #c0c0d8;
    transition: border-color 0.12s;
}
.sf-option-label {
    font-weight: 700;
    color: #555570;
    font-size: 0.75rem;
    min-width: 1rem;
}
.sf-answer-box {
    background: rgba(200,245,66,0.08);
    border: 1px solid rgba(200,245,66,0.25);
    border-radius: 6px;
    padding: 0.7rem 1rem;
    margin-top: 0.6rem;
    font-size: 0.82rem;
    color: #c8f542;
}

/* ── Flashcard ── */
.sf-flashcard {
    background: #0f0f1a;
    border: 1px solid #2a2a40;
    border-radius: 10px;
    padding: 1.4rem;
    text-align: center;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.8rem;
}
.sf-flashcard-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #555570;
    margin-bottom: 0.6rem;
}
.sf-flashcard-text {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    color: #e8e6f0;
    line-height: 1.4;
}

/* ── Library items ── */
.sf-lib-item {
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: border-color 0.12s;
}
.sf-lib-item:hover { border-color: #c8f542; }
.sf-lib-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: #e8e6f0;
}
.sf-lib-meta {
    font-size: 0.72rem;
    color: #555570;
    margin-top: 0.2rem;
}

/* ── Status / info boxes ── */
.sf-info {
    background: rgba(66,197,245,0.07);
    border: 1px solid rgba(66,197,245,0.2);
    border-radius: 6px;
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: #42c8f5;
    margin-bottom: 1rem;
}
.sf-warn {
    background: rgba(245,175,66,0.07);
    border: 1px solid rgba(245,175,66,0.2);
    border-radius: 6px;
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: #f5af42;
    margin-bottom: 1rem;
}

/* ── Selectbox ── */
div[data-baseweb="select"] {
    background: #0f0f1a !important;
}
div[data-baseweb="select"] * {
    background: #0f0f1a !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Radio ── */
.stRadio label { font-size: 0.85rem !important; color: #a0a0c0 !important; }

/* ── Markdown inside app ── */
.stMarkdown p, .stMarkdown li { font-size: 0.88rem !important; line-height: 1.7 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Syne', sans-serif !important;
    color: #e8e6f0 !important;
}

/* ── Progress ── */
.stProgress > div > div { background: #c8f542 !important; }

/* ── Exam topics ── */
.sf-exam-topic {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #1a1a28;
    font-size: 0.85rem;
    color: #c0c0d8;
}
.sf-bullet { color: #c8f542; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

# ── Imports after page config ─────────────────────────────────────────────────
from auth import show_auth_page, get_supabase_client, get_current_user
from processor import extract_text_from_source
from ai_generator import generate_study_materials
from db import save_lecture, save_materials, get_user_lectures, get_lecture_materials, delete_lecture

# ── Auth gate ────────────────────────────────────────────────────────────────
supabase = get_supabase_client()
user = get_current_user(supabase)

if not user:
    show_auth_page(supabase)
    st.stop()

# ── Top nav bar (no sidebar needed) ─────────────────────────────────────────
st.markdown('''
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:0.7rem 1.2rem;background:#0f0f1a;border:1px solid #1e1e30;
            border-radius:10px;margin-bottom:1.5rem;">
    <span style="font-family:Syne,sans-serif;font-weight:800;font-size:1.3rem;
                 background:linear-gradient(135deg,#c8f542,#42f5a7);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        ⚡ StudyForge
    </span>
</div>''', unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state["page"] = "new"

col_n, col_l, col_s = st.columns([2, 2, 1])
with col_n:
    if st.button("⚡ New Lecture", key="nav_new", use_container_width=True):
        st.session_state["page"] = "new"
        st.rerun()
with col_l:
    if st.button("📚 My Library", key="nav_lib", use_container_width=True):
        st.session_state["page"] = "lib"
        st.rerun()
with col_s:
    if st.button("Sign Out", key="signout", use_container_width=True):
        supabase.auth.sign_out()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown(f'<div style="font-size:0.72rem;color:#555570;margin-bottom:1rem;">signed in as {user.email}</div>', unsafe_allow_html=True)

page = "⚡ New Lecture" if st.session_state["page"] == "new" else "📚 My Library"

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW LECTURE
# ═══════════════════════════════════════════════════════════════════════════════
if "⚡ New" in page:
    st.markdown('<div class="sf-logo" style="font-size:1.8rem;">⚡ New Lecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-tagline">Upload a lecture, get complete study materials instantly</div>', unsafe_allow_html=True)

    # ── Source selection ──────────────────────────────────────────────────────
    st.markdown('<div class="sf-section">Input Source</div>', unsafe_allow_html=True)
    source_type = st.radio(
        "Choose input type",
        ["🎬 YouTube URL", "📄 Paste Transcript", "📁 Upload File (PDF / PPTX / TXT)"],
        label_visibility="collapsed"
    )

    raw_text = None
    source_ref = ""
    title_input = st.text_input("Lecture title (optional — we'll auto-detect if blank)", placeholder="e.g. Week 4 — Cell Biology")

    if "🎬" in source_type:
        yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        st.markdown('<div class="sf-info">ℹ️ We grab auto-captions automatically. If the video has no captions, paste the transcript below instead.</div>', unsafe_allow_html=True)
        if yt_url:
            source_ref = yt_url

    elif "📄" in source_type:
        pasted = st.text_area("Paste your transcript here", height=260, placeholder="Paste lecture transcript, notes, or any text...")
        if pasted:
            raw_text = pasted
            source_ref = "pasted_transcript"

    else:
        uploaded = st.file_uploader("Upload file", type=["pdf", "pptx", "txt"])
        if uploaded:
            source_ref = uploaded.name

    # ── Generate button ───────────────────────────────────────────────────────
    st.markdown("")
    gen_clicked = st.button("⚡ Generate Study Materials", disabled=(not source_ref and not raw_text))

    if gen_clicked:
        with st.spinner(""):
            progress = st.progress(0, text="Extracting text...")

            # Step 1: Extract text
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
                st.markdown(f'<div class="sf-warn">⚠️ {str(e)}</div>', unsafe_allow_html=True)
                st.stop()

            if not text or len(text.strip()) < 100:
                st.markdown('<div class="sf-warn">⚠️ Not enough text found. Try pasting the transcript manually.</div>', unsafe_allow_html=True)
                st.stop()

            progress.progress(30, text="Sending to AI...")

            # Step 2: Generate with Groq
            try:
                materials = generate_study_materials(text)
            except Exception as e:
                st.markdown(f'<div class="sf-warn">⚠️ AI generation failed: {str(e)}</div>', unsafe_allow_html=True)
                st.stop()

            progress.progress(75, text="Saving to your library...")

            # Step 3: Save to Supabase
            final_title = title_input or materials.get("title", "Untitled Lecture")
            src_type_clean = "youtube" if "🎬" in source_type else ("transcript" if "📄" in source_type else source_ref.split(".")[-1])

            lecture_id = save_lecture(supabase, user.id, final_title, src_type_clean, source_ref, text)
            save_materials(supabase, lecture_id, user.id, materials)

            progress.progress(100, text="Done!")
            st.session_state["current_lecture_id"] = lecture_id
            st.session_state["current_materials"] = materials
            st.session_state["current_title"] = final_title

    # ── Display results ───────────────────────────────────────────────────────
    if "current_materials" in st.session_state:
        materials = st.session_state["current_materials"]
        title = st.session_state.get("current_title", "Lecture")

        st.markdown(f'<div class="sf-section">{title}</div>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Notes", "📖 Glossary", "❓ Quiz", "🃏 Flashcards", "🎯 Exam Topics"])

        with tab1:
            if materials.get("summary"):
                st.markdown('<div class="sf-card sf-card-accent"><strong style="color:#c8f542;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;">TL;DR</strong><br/>' + materials["summary"] + '</div>', unsafe_allow_html=True)
            st.markdown(materials.get("notes", "No notes generated."))

        with tab2:
            glossary = materials.get("glossary", [])
            if glossary:
                for item in glossary:
                    st.markdown(f"""
                    <div class="sf-card">
                        <div class="sf-term">{item.get('term','')}</div>
                        <div class="sf-def">{item.get('definition','')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.write("No glossary generated.")

        with tab3:
            quiz = materials.get("quiz", [])
            if quiz:
                if "quiz_revealed" not in st.session_state:
                    st.session_state["quiz_revealed"] = {}
                for i, q in enumerate(quiz):
                    st.markdown(f"""
                    <div class="sf-card">
                        <div class="sf-q-num">Question {i+1} of {len(quiz)}</div>
                        <div class="sf-question">{q.get('question','')}</div>
                    """, unsafe_allow_html=True)
                    options = q.get("options", [])
                    labels = ["A", "B", "C", "D"]
                    for j, opt in enumerate(options):
                        lbl = labels[j] if j < len(labels) else str(j+1)
                        st.markdown(f'<div class="sf-option"><span class="sf-option-label">{lbl}</span>{opt}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    revealed = st.session_state["quiz_revealed"].get(i, False)
                    if st.button(f"{'Hide' if revealed else 'Show'} Answer", key=f"quiz_reveal_{i}"):
                        st.session_state["quiz_revealed"][i] = not revealed
                        st.rerun()
                    if revealed:
                        st.markdown(f'<div class="sf-answer-box">✓ <strong>{q.get("answer","")}</strong><br/><span style="color:#a0a0c0;font-size:0.8rem;">{q.get("explanation","")}</span></div>', unsafe_allow_html=True)
            else:
                st.write("No quiz generated.")

        with tab4:
            flashcards = materials.get("flashcards", [])
            if flashcards:
                if "fc_index" not in st.session_state:
                    st.session_state["fc_index"] = 0
                if "fc_flipped" not in st.session_state:
                    st.session_state["fc_flipped"] = False

                fc = flashcards[st.session_state["fc_index"]]
                side = "back" if st.session_state["fc_flipped"] else "front"
                label = "Answer" if st.session_state["fc_flipped"] else "Term"
                text_shown = fc.get(side, "")

                st.markdown(f"""
                <div class="sf-flashcard">
                    <div class="sf-flashcard-label">{label} · {st.session_state["fc_index"]+1}/{len(flashcards)}</div>
                    <div class="sf-flashcard-text">{text_shown}</div>
                </div>""", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("← Prev", key="fc_prev"):
                        st.session_state["fc_index"] = max(0, st.session_state["fc_index"] - 1)
                        st.session_state["fc_flipped"] = False
                        st.rerun()
                with col2:
                    if st.button("Flip 🔄", key="fc_flip"):
                        st.session_state["fc_flipped"] = not st.session_state["fc_flipped"]
                        st.rerun()
                with col3:
                    if st.button("Next →", key="fc_next"):
                        st.session_state["fc_index"] = min(len(flashcards)-1, st.session_state["fc_index"] + 1)
                        st.session_state["fc_flipped"] = False
                        st.rerun()
            else:
                st.write("No flashcards generated.")

        with tab5:
            exam_topics = materials.get("exam_topics", "")
            if exam_topics:
                topics = [t.strip() for t in exam_topics.split("\n") if t.strip()]
                for topic in topics:
                    clean = topic.lstrip("-•*123456789. ")
                    st.markdown(f'<div class="sf-exam-topic"><span class="sf-bullet">▸</span>{clean}</div>', unsafe_allow_html=True)
            else:
                st.write("No exam topics generated.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="sf-logo" style="font-size:1.8rem;">📚 My Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-tagline">All your saved study materials</div>', unsafe_allow_html=True)

    lectures = get_user_lectures(supabase, user.id)

    if not lectures:
        st.markdown('<div class="sf-info">You haven\'t processed any lectures yet. Go to ⚡ New Lecture to get started!</div>', unsafe_allow_html=True)
    else:
        # Select lecture
        if "lib_selected" not in st.session_state:
            st.session_state["lib_selected"] = None

        st.markdown('<div class="sf-section">Your Lectures</div>', unsafe_allow_html=True)
        for lec in lectures:
            col1, col2 = st.columns([5, 1])
            with col1:
                created = lec.get("created_at", "")[:10] if lec.get("created_at") else ""
                src = lec.get("source_type", "")
                icon = {"youtube": "🎬", "pdf": "📄", "pptx": "📊", "txt": "📝", "transcript": "📋"}.get(src, "📁")
                if st.button(f'{icon} {lec["title"]}  ·  {created}', key=f'lib_{lec["id"]}'):
                    st.session_state["lib_selected"] = lec["id"]
                    st.session_state["lib_quiz_revealed"] = {}
                    st.session_state["lib_fc_index"] = 0
                    st.session_state["lib_fc_flipped"] = False
                    st.rerun()
            with col2:
                if st.button("🗑", key=f'del_{lec["id"]}'):
                    delete_lecture(supabase, lec["id"])
                    if st.session_state.get("lib_selected") == lec["id"]:
                        st.session_state["lib_selected"] = None
                    st.rerun()

        # Show selected lecture materials
        if st.session_state.get("lib_selected"):
            lec_id = st.session_state["lib_selected"]
            materials = get_lecture_materials(supabase, lec_id)
            lec_info = next((l for l in lectures if l["id"] == lec_id), {})

            if materials:
                st.markdown(f'<div class="sf-section">{lec_info.get("title","")}</div>', unsafe_allow_html=True)

                tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Notes", "📖 Glossary", "❓ Quiz", "🃏 Flashcards", "🎯 Exam Topics"])

                with tab1:
                    if materials.get("summary"):
                        st.markdown('<div class="sf-card sf-card-accent"><strong style="color:#c8f542;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;">TL;DR</strong><br/>' + materials["summary"] + '</div>', unsafe_allow_html=True)
                    st.markdown(materials.get("notes", ""))

                with tab2:
                    for item in (materials.get("glossary") or []):
                        st.markdown(f"""
                        <div class="sf-card">
                            <div class="sf-term">{item.get('term','')}</div>
                            <div class="sf-def">{item.get('definition','')}</div>
                        </div>""", unsafe_allow_html=True)

                with tab3:
                    quiz = materials.get("quiz") or []
                    for i, q in enumerate(quiz):
                        st.markdown(f"""
                        <div class="sf-card">
                            <div class="sf-q-num">Question {i+1} of {len(quiz)}</div>
                            <div class="sf-question">{q.get('question','')}</div>
                        """, unsafe_allow_html=True)
                        for j, opt in enumerate(q.get("options", [])):
                            lbl = ["A","B","C","D"][j] if j < 4 else str(j+1)
                            st.markdown(f'<div class="sf-option"><span class="sf-option-label">{lbl}</span>{opt}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if "lib_quiz_revealed" not in st.session_state:
                            st.session_state["lib_quiz_revealed"] = {}
                        revealed = st.session_state["lib_quiz_revealed"].get(i, False)
                        if st.button(f"{'Hide' if revealed else 'Show'} Answer", key=f"libquiz_{lec_id}_{i}"):
                            st.session_state["lib_quiz_revealed"][i] = not revealed
                            st.rerun()
                        if revealed:
                            st.markdown(f'<div class="sf-answer-box">✓ <strong>{q.get("answer","")}</strong><br/><span style="color:#a0a0c0;font-size:0.8rem;">{q.get("explanation","")}</span></div>', unsafe_allow_html=True)

                with tab4:
                    flashcards = materials.get("flashcards") or []
                    if flashcards:
                        idx = st.session_state.get("lib_fc_index", 0)
                        flipped = st.session_state.get("lib_fc_flipped", False)
                        fc = flashcards[idx]
                        side = "back" if flipped else "front"
                        label = "Answer" if flipped else "Term"
                        st.markdown(f"""
                        <div class="sf-flashcard">
                            <div class="sf-flashcard-label">{label} · {idx+1}/{len(flashcards)}</div>
                            <div class="sf-flashcard-text">{fc.get(side,'')}</div>
                        </div>""", unsafe_allow_html=True)
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            if st.button("← Prev", key="libfc_prev"):
                                st.session_state["lib_fc_index"] = max(0, idx-1)
                                st.session_state["lib_fc_flipped"] = False
                                st.rerun()
                        with c2:
                            if st.button("Flip 🔄", key="libfc_flip"):
                                st.session_state["lib_fc_flipped"] = not flipped
                                st.rerun()
                        with c3:
                            if st.button("Next →", key="libfc_next"):
                                st.session_state["lib_fc_index"] = min(len(flashcards)-1, idx+1)
                                st.session_state["lib_fc_flipped"] = False
                                st.rerun()

                with tab5:
                    exam_topics = materials.get("exam_topics", "")
                    if exam_topics:
                        for topic in exam_topics.split("\n"):
                            clean = topic.strip().lstrip("-•*123456789. ")
                            if clean:
                                st.markdown(f'<div class="sf-exam-topic"><span class="sf-bullet">▸</span>{clean}</div>', unsafe_allow_html=True)
