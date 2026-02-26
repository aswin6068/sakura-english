"""
Sakura English Tutor API  v5.0
- Chat : groq SDK  (llama-3.3-70b-versatile)
- STT  : groq SDK  (whisper-large-v3-turbo)
- TTS  : groq SDK  (playai-tts)
Requires: groq>=1.0.0
"""

import os
import json
import tempfile
from typing import Optional, List
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from groq import Groq
import requests as _http
import logging

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "llama-3.3-70b-versatile")
STT_MODEL  = os.getenv("GROQ_STT_MODEL",  "whisper-large-v3-turbo")
TTS_MODEL  = os.getenv("GROQ_TTS_MODEL",  "canopylabs/orpheus-v1-english")
TTS_VOICE  = os.getenv("GROQ_TTS_VOICE",  "zoe")

SUPPORTED_AUDIO_FORMATS = {".webm", ".wav", ".mp3", ".m4a", ".ogg", ".flac", ".opus"}
MAX_AUDIO_SIZE_MB = 25

AVAILABLE_VOICES = [
    "zoe", "zac", "mia", "leah", "tara",   # Female
    "dan", "troy", "austin",                 # Male
]

client = Groq(api_key=GROQ_API_KEY)

# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("━━ Sakura English Tutor API v5.0 ━━")
    logger.info(f"Chat : {CHAT_MODEL}")
    logger.info(f"STT  : {STT_MODEL}")
    logger.info(f"TTS  : {TTS_MODEL} / {TTS_VOICE}")
    logger.info(f"Groq SDK: OK")
    yield
    logger.info("Shutting down.")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Sakura English Tutor API",
    description="AI English tutoring — Groq chat + STT + TTS",
    version="5.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Sakura (🌸), a warm and encouraging English teacher whose native language is Malayalam.

OUTPUT RULE — MOST IMPORTANT:
Respond with ONLY a raw JSON object. Nothing before {. Nothing after }. No markdown. No ```json fences. No explanations outside the JSON.

Your personality:
- Friendly, patient, supportive like a best friend teacher
- Teach in English by default
- Switch to Malayalam explanations only when user asks ("explain in Malayalam", "meaning", "arth", "Malayalam-ൽ പറ")
- Never judge mistakes harshly

Every response must:
1. Continue conversation naturally with a follow-up question
2. Correct any grammar/word errors gently
3. Explain mistakes in English by default (Malayalam only if requested)
4. Give exactly 2 alternative phrasings
5. Give 1 practice prompt with answer

JSON FORMAT (output this structure and nothing else):
{
  "reply_to_user": "Your natural conversational reply here",
  "language_used": "en",
  "correction": {
    "original": "learner's original sentence",
    "corrected": "corrected sentence",
    "mistakes": [
      {
        "type": "grammar|tense|article|word_choice|preposition|fluency",
        "message_en": "Short English explanation",
        "message_ml": "മലയാളം വിശദീകരണം",
        "fix_en": "How to fix in English",
        "fix_ml": "എങ്ങനെ ശരിയാക്കാം"
      }
    ]
  },
  "alternatives": ["Alternative 1", "Alternative 2"],
  "practice": { "prompt": "Practice question", "answer": "Correct answer" }
}

If sentence is perfect: set "correction": null
"""


# ── Pydantic models ───────────────────────────────────────────────────────────
class MistakeDetail(BaseModel):
    type: str
    message_en: str
    message_ml: str
    fix_en: str
    fix_ml: str

class Correction(BaseModel):
    original: str
    corrected: str
    mistakes: List[MistakeDetail]

class Practice(BaseModel):
    prompt: str
    answer: str

class TutorResponse(BaseModel):
    reply_to_user: str
    language_used: str = "en"
    correction: Optional[Correction]
    alternatives: List[str]
    practice: Practice

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=1000)
    scenario: str = Field(default="general")
    level: str = Field(default="beginner")
    history: List[ChatMessage] = Field(default_factory=list)

    @field_validator("user_message")
    @classmethod
    def strip_msg(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v

    @field_validator("scenario")
    @classmethod
    def check_scenario(cls, v):
        allowed = {"cafe", "restaurant", "shopping", "travel", "office", "general"}
        v = v.lower()
        if v not in allowed:
            raise ValueError(f"Scenario must be one of: {', '.join(allowed)}")
        return v

    @field_validator("level")
    @classmethod
    def check_level(cls, v):
        allowed = {"beginner", "intermediate", "advanced"}
        v = v.lower()
        if v not in allowed:
            raise ValueError(f"Level must be one of: {', '.join(allowed)}")
        return v

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    voice: Optional[str] = None

    @field_validator("text")
    @classmethod
    def strip_text(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty")
        return v

class STTResponse(BaseModel):
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None


# ── Routes ────────────────────────────────────────────────────────────────────
''' Basic health check and info endpoint 
@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Sakura English Tutor API",
        "version": "5.0.0",
        "models": {
            "chat": CHAT_MODEL,
            "stt":  STT_MODEL,
            "tts":  f"{TTS_MODEL} / {TTS_VOICE}",
        },
    }'''
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app")

@app.get("/app", response_class=HTMLResponse)
def serve_app():
    path = os.path.join("static", "index.html")
    if not os.path.exists(path):
        raise HTTPException(404, "Web UI not found. Ensure static/index.html exists.")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# ── JSON helper ───────────────────────────────────────────────────────────────

def _parse_json(raw: str):
    """Strip markdown fences, extract first {...} block, parse JSON. Returns None on failure."""
    raw = raw.replace("```json", "").replace("```", "").strip()
    start = raw.find("{")
    end   = raw.rfind("}") + 1
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(raw[start:end])
    except json.JSONDecodeError:
        return None


# ── Chat ──────────────────────────────────────────────────────────────────────

@app.post("/chat", response_model=TutorResponse)
async def chat(req: ChatRequest):
    """Full conversational chat with history support."""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in req.history[-20:]:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({
            "role": "user",
            "content": f"[Scenario: {req.scenario} | Level: {req.level}]\n{req.user_message}"
        })

        logger.info(f"Chat | {req.scenario}/{req.level} history={len(req.history)} '{req.user_message[:60]}'")

        completion = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.55,
            max_tokens=1200,
        )

        raw = completion.choices[0].message.content.strip()
        logger.info(f"Raw LLM: {raw[:200]}")
        data = _parse_json(raw)

        if data is None:
            logger.warning("JSON parse failed — retrying with strict prompt")
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "Your last reply was not valid JSON. Output ONLY the JSON object with no extra text, no markdown, no explanation."})
            retry = client.chat.completions.create(
                model=CHAT_MODEL, messages=messages, temperature=0.1, max_tokens=1200
            )
            raw = retry.choices[0].message.content.strip()
            data = _parse_json(raw)

        if data is None:
            logger.error(f"JSON failed after retry:\n{raw}")
            raise HTTPException(500, "AI returned malformed JSON. Please try again.")

        data.setdefault("language_used", "en")
        data.setdefault("alternatives", ["", ""])
        data.setdefault("practice", {"prompt": "", "answer": ""})
        return data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(500, f"Chat failed: {e}")


# ── STT ───────────────────────────────────────────────────────────────────────

def _mime_for(suffix: str) -> str:
    return {
        ".webm": "audio/webm",
        ".wav":  "audio/wav",
        ".mp3":  "audio/mpeg",
        ".m4a":  "audio/mp4",
        ".ogg":  "audio/ogg",
        ".flac": "audio/flac",
        ".opus": "audio/opus",
    }.get(suffix, "audio/webm")


@app.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None),
):
    """Speech-to-text via Groq Whisper SDK."""
    tmp_path = None
    try:
        filename = audio.filename or "recording.webm"
        suffix   = os.path.splitext(filename)[1].lower() or ".webm"

        if suffix not in SUPPORTED_AUDIO_FORMATS:
            raise HTTPException(400, f"Unsupported format '{suffix}'.")

        audio_bytes = await audio.read()
        size_mb = len(audio_bytes) / (1024 * 1024)

        if size_mb > MAX_AUDIO_SIZE_MB:
            raise HTTPException(400, f"File too large ({size_mb:.1f} MB). Max {MAX_AUDIO_SIZE_MB} MB.")
        if len(audio_bytes) < 200:
            raise HTTPException(400, "Audio is too short. Please record for at least 1 second.")

        logger.info(f"STT | {filename} {size_mb:.3f}MB")

        # Write to temp file so SDK can open it properly
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model=STT_MODEL,
                file=(filename, f, _mime_for(suffix)),
                response_format="verbose_json",
                language=language if language else None,
            )

        text     = getattr(transcription, "text", "").strip()
        duration = getattr(transcription, "duration", None)

        if not text:
            raise HTTPException(422, "Could not understand audio. Please speak clearly and try again.")

        logger.info(f"STT | '{text[:80]}' duration={duration}s")
        return STTResponse(text=text, language=language, duration=duration)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"STT error: {e}")
        raise HTTPException(500, f"Speech recognition failed: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


# ── TTS ───────────────────────────────────────────────────────────────────────

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    """Text-to-speech via Groq Orpheus REST API (direct HTTP — no SDK audio dependency)."""
    try:
        voice = req.voice if req.voice in AVAILABLE_VOICES else TTS_VOICE
        text  = req.text[:300] + ("..." if len(req.text) > 300 else "")

        logger.info(f"TTS | model={TTS_MODEL} voice={voice} chars={len(text)}")

        resp = _http.post(
            "https://api.groq.com/openai/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": TTS_MODEL,
                "voice": voice,
                "input": text,
                "response_format": "wav",
            },
            timeout=60,
        )

        if resp.status_code != 200:
            err = resp.json().get("error", {}).get("message", resp.text[:300])
            logger.error(f"TTS HTTP {resp.status_code}: {err}")
            raise HTTPException(502, f"Groq TTS error: {err}")

        audio_bytes = resp.content
        if len(audio_bytes) < 100:
            raise RuntimeError("TTS returned empty audio.")

        logger.info(f"TTS | received {len(audio_bytes)} bytes")
        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=speech.wav"},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(500, f"Speech generation failed: {e}")


# ── Utility endpoints ─────────────────────────────────────────────────────────

@app.get("/voices")
def list_voices():
    return {"voices": AVAILABLE_VOICES, "default": TTS_VOICE}

@app.get("/scenarios")
def list_scenarios():
    return {"scenarios": [
        {"id": "cafe",       "name": "Coffee Shop",         "emoji": "☕"},
        {"id": "restaurant", "name": "Restaurant",          "emoji": "🍽️"},
        {"id": "shopping",   "name": "Shopping",            "emoji": "🛍️"},
        {"id": "travel",     "name": "Travel & Tourism",    "emoji": "✈️"},
        {"id": "office",     "name": "Office / Workplace",  "emoji": "💼"},
        {"id": "general",    "name": "General Conversation","emoji": "💬"},
    ]}

@app.get("/levels")
def list_levels():
    return {"levels": [
        {"id": "beginner",     "name": "Beginner",     "emoji": "🌱"},
        {"id": "intermediate", "name": "Intermediate", "emoji": "🌿"},
        {"id": "advanced",     "name": "Advanced",     "emoji": "🌳"},
    ]}


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
