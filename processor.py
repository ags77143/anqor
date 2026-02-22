"""
processor.py — Extract raw text from YouTube URLs, PDFs, PPTXs, and TXT files.
"""
import io
import re


def extract_text_from_source(source_type: str, url: str = None, file=None) -> tuple:
    if source_type == "youtube":
        return _extract_youtube(url)
    elif source_type == "file":
        return _extract_file(file)
    else:
        raise ValueError(f"Unknown source type: {source_type}")


def _parse_youtube_id(url: str):
    # Handle all common YouTube URL formats
    patterns = [
        r'(?:v=)([a-zA-Z0-9_-]{11})',           # ?v=xxxx
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',   # youtu.be/xxxx
        r'(?:embed\/)([a-zA-Z0-9_-]{11})',        # /embed/xxxx
        r'(?:shorts\/)([a-zA-Z0-9_-]{11})',       # /shorts/xxxx
        r'(?:live\/)([a-zA-Z0-9_-]{11})',         # /live/xxxx
        r'^([a-zA-Z0-9_-]{11})$',                 # bare ID
    ]
    url = url.strip()
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _extract_youtube(url: str) -> tuple:
    from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

    video_id = _parse_youtube_id(url)
    if not video_id:
        raise ValueError(
            f"Couldn't find a YouTube video ID in that URL.\n\n"
            f"URL received: `{url}`\n\n"
            f"Try copying the URL directly from your browser address bar."
        )

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript = None
        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
        except Exception:
            pass

        if not transcript:
            try:
                transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
            except Exception:
                pass

        if not transcript:
            for t in transcript_list:
                transcript = t
                break

        if not transcript:
            raise ValueError("No captions found. Please paste the transcript manually.")

        entries = transcript.fetch()
        text = " ".join(entry["text"] for entry in entries)
        text = re.sub(r"\[.*?\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text, ""

    except (NoTranscriptFound, TranscriptsDisabled):
        raise ValueError("This video has no captions. Please paste the transcript manually instead.")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to fetch transcript: {str(e)}")


def _extract_file(file) -> tuple:
    name = file.name.lower()
    if name.endswith(".txt"):
        return _extract_txt(file), file.name
    elif name.endswith(".pdf"):
        return _extract_pdf(file), file.name
    elif name.endswith(".pptx"):
        return _extract_pptx(file), file.name
    else:
        raise ValueError(f"Unsupported file type. Please upload PDF, PPTX, or TXT.")


def _extract_txt(file) -> str:
    content = file.read()
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def _extract_pdf(file) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages)
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")


def _extract_pptx(file) -> str:
    try:
        from pptx import Presentation
        prs = Presentation(io.BytesIO(file.read()))
        slides_text = []
        for i, slide in enumerate(prs.slides):
            parts = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    parts.append(shape.text.strip())
            if parts:
                slides_text.append(f"[Slide {i+1}]\n" + "\n".join(parts))
        return "\n\n".join(slides_text)
    except Exception as e:
        raise ValueError(f"Failed to read PPTX: {str(e)}")
