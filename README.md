# ⚡ StudyForge

Turn any university lecture into comprehensive study materials — completely free, persistent across sessions.

**Supports:** YouTube URLs (auto-captions) · PDF · PPTX · TXT · Pasted transcripts  
**Generates:** Structured notes · Key terms glossary · MCQ quiz · Flashcards · Exam topics

---

## Setup Guide

### 1. Clone & install

```bash
git clone https://github.com/yourusername/studyforge
cd studyforge
pip install -r requirements.txt
```

### 2. Get your free API keys

#### Groq (AI — free, no credit card)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with email
3. Go to API Keys → Create API Key
4. Copy the key

#### Supabase (database + auth — free tier is plenty)
1. Go to [supabase.com](https://supabase.com) → New Project
2. Give it a name and a database password
3. Once created, go to **Settings → API**
4. Copy **Project URL** and **anon/public** key
5. Go to **SQL Editor** and run the entire contents of `supabase_schema.sql`

### 3. Set environment variables

```bash
cp .env.example .env
# Edit .env and fill in your three keys
```

### 4. Run locally

```bash
streamlit run app.py
```

---

## Deploy to Streamlit Community Cloud (free, persistent)

This is the recommended way — your app stays live even when you close the tab.

1. Push your code to a **public or private GitHub repo**  
   ⚠️ Make sure `.env` is in `.gitignore` — never commit real keys!

2. Go to [share.streamlit.io](https://share.streamlit.io) → New App → connect your repo

3. In **Advanced Settings → Secrets**, paste:
   ```toml
   GROQ_API_KEY = "gsk_..."
   SUPABASE_URL = "https://xxxx.supabase.co"
   SUPABASE_ANON_KEY = "eyJ..."
   ```

4. Deploy! Your app gets a permanent URL like `https://yourapp.streamlit.app`

---

## How it works

```
User input (YouTube / PDF / PPTX / transcript)
        ↓
Text extraction (youtube-transcript-api / PyPDF2 / python-pptx)
        ↓
Groq API — Llama 3 70B generates all materials in one call
        ↓
Supabase — saves everything to your personal library
        ↓
Streamlit — displays notes, glossary, quiz, flashcards, exam topics
```

## YouTube videos with no captions

If a video has no captions, the app will tell you and prompt you to paste the transcript manually. You can usually find transcripts from:
- Your university's lecture portal / VLE
- The video's description or companion slides
- Upload the PPTX slides instead if available

## Free tier limits

| Service | Free limit |
|---------|-----------|
| Groq | 1,500 requests/day, 30 req/min |
| Supabase | 500MB database, 1GB storage |
| Streamlit Cloud | Unlimited deployments |

All more than enough for personal student use.

---

## Project structure

```
studyforge/
├── app.py              # Main Streamlit app + UI
├── auth.py             # Supabase auth (login/signup)
├── processor.py        # Text extraction for all source types
├── ai_generator.py     # Groq API call + JSON parsing
├── db.py               # Supabase database operations
├── supabase_schema.sql # Run this in Supabase SQL editor once
├── requirements.txt
├── .env.example        # Copy to .env and fill in keys
└── .streamlit/
    └── secrets.toml.example  # For Streamlit Cloud deployment
```
