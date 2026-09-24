"""EduSphere AI — FastAPI app.

Serves the kid chat PWA + JSON API. Run:
    uvicorn app.main:app --host 0.0.0.0 --port 8100
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from . import characters, conversation, knowledge, profiles, tutor, worlds

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="EduSphere AI", docs_url=None, redoc_url=None)

# tiny in-memory rate limiter: pid -> last request ts
_last_req: dict[str, float] = {}


def _rate_ok(pid: str, min_gap: float = 2.0) -> bool:
    now = time.time()
    if now - _last_req.get(pid, 0) < min_gap:
        return False
    _last_req[pid] = now
    return True


# ---------------- models ----------------

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    grade: int = Field(default=0, ge=0, le=12)  # 0 = pre-school (worlds by age)
    parent_pin: str = Field(min_length=4, max_length=8)
    character: str = "auto"
    age: int | None = Field(default=None, ge=2, le=7)

    @field_validator("character")
    @classmethod
    def buddy_exists(cls, v: str) -> str:
        if v != "auto" and v not in characters.CHARACTERS:
            raise ValueError("unknown buddy")
        return v


class ProfileUpdate(BaseModel):
    grade: int | None = Field(default=None, ge=0, le=12)
    character: str | None = None
    age: int | None = Field(default=None, ge=2, le=7)


class ChatRequest(BaseModel):
    pid: str
    message: str = Field(min_length=1, max_length=2000)
    history: list[dict] = Field(default_factory=list, max_length=20)
    mode: str | None = None
    lang: str = "en"


class PinRequest(BaseModel):
    pid: str
    pin: str = Field(min_length=4, max_length=8)


# ---------------- API ----------------

@app.post("/api/profile")
def create_profile(body: ProfileCreate):
    try:
        profile = profiles.create_profile(
            body.name, body.grade, body.parent_pin, body.character,
            age=body.age)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {"pid": profile["pid"], "profile": profile}


@app.get("/api/profile/{pid}")
def get_profile(pid: str):
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


@app.post("/api/profile/{pid}/update")
def update_profile(pid: str, body: ProfileUpdate):
    if body.character is not None and body.character not in characters.CHARACTERS:
        raise HTTPException(400, "unknown buddy")
    profile = profiles.update_profile(pid, **body.model_dump())
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


@app.get("/api/characters")
def list_characters():
    """The Character Universe roster, in carousel order."""
    return {"characters": characters.roster()}


@app.get("/api/worlds")
def list_worlds():
    """The Four Worlds roster, in age order."""
    return {"worlds": worlds.roster()}


@app.get("/api/worlds/for-profile/{pid}")
def world_for_profile(pid: str):
    """The world this child belongs to right now."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    w = worlds.world_for_profile(profile)
    return {"world": worlds.public(w["id"])}


@app.get("/api/wardrobe")
def list_wardrobe():
    """Dress-up shop catalog with star costs."""
    return {"items": characters.accessories_public()}


class AccessoryRequest(BaseModel):
    pid: str
    item: str = Field(max_length=20)


@app.post("/api/profile/{pid}/wear")
def wear_accessory(pid: str, body: AccessoryRequest):
    item = body.item
    if not characters.valid_outfit(item):
        raise HTTPException(400, "unknown accessory")
    try:
        profile = profiles.update_profile(pid, accessory=item)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    if profile is None:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


@app.post("/api/profile/{pid}/buy")
def buy_accessory(pid: str, body: AccessoryRequest):
    acc = characters.ACCESSORIES.get(body.item)
    if not acc:
        raise HTTPException(400, "unknown accessory")
    try:
        profile = profiles.buy_item(pid, body.item, acc["cost"])
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {"profile": profile}


@app.post("/api/chat")
def chat(body: ChatRequest):
    profile = profiles.get_profile(body.pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    if not _rate_ok(body.pid):
        return JSONResponse(
            {"error": "easy there! try again in a couple of seconds."},
            status_code=429)
    subject = tutor.detect_subject(body.message, profile["grade"])
    answer = tutor.ask(
        name=profile["name"], grade=profile["grade"],
        buddy=profile.get("character") or "auto",
        question=body.message, history=body.history, subject=subject,
        weak_areas=list(profile.get("weak_areas", {}).keys()),
        mode=body.mode, age=profile.get("age"),
        lang=body.lang if body.lang in conversation.LANGUAGES else "en",
        memories=list(profile.get("memories", [])))
    topic = _topic_from(subject, body.message)
    updated = profiles.record_activity(body.pid, "chat", topic)
    buddy = characters.public(profile.get("character") or "leo")
    world = worlds.world_for_profile(profile)
    # stage 1+2: voice profile + speaking pace for the frontend TTS engine
    voice = conversation.voice_public(buddy["id"])
    voice["pace"] = conversation.pace_for_grade(profile.get("grade"),
                                                profile.get("age"))
    voice["lang"] = conversation.LANGUAGES.get(
        body.lang, conversation.LANGUAGES["en"])["voice_lang"]
    # stage 6: sticker for the first chat of the session comes from frontend
    return {"answer": answer, "subject": subject, "topic": topic,
            "stars": updated["stars"] if updated else 0,
            "character": buddy["id"], "character_name": buddy["name"],
            "character_emoji": buddy["emoji"],
            "world": world["id"], "world_name": world["name"],
            "world_emoji": world["emoji"],
            "voice": voice}


class StickerRequest(BaseModel):
    sticker: str = Field(min_length=1, max_length=40)


@app.post("/api/profile/{pid}/sticker")
def award_sticker(pid: str, body: StickerRequest):
    """Stage 6: drop a sticker into the child's album."""
    profile = profiles.award_sticker(pid, body.sticker)
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


class RememberBody(BaseModel):
    text: str = Field(min_length=2, max_length=120)


@app.post("/api/profile/{pid}/remember")
def remember(pid: str, body: RememberBody):
    """Stage 2: buddy remembers a life detail across days."""
    profile = profiles.remember(pid, body.text)
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


class GameResult(BaseModel):
    pid: str
    game: str = Field(min_length=1, max_length=40)
    score: int = Field(ge=0)
    stars: int = Field(default=0, ge=0, le=20)
    topic: str = Field(default="", max_length=80)


@app.post("/api/game/result")
def game_result(body: GameResult):
    """Stage 5: record a game result, award stars + a sticker."""
    profile = profiles.record_activity(
        body.pid, "game:" + body.game, body.topic or body.game,
        stars=body.stars)
    if not profile:
        raise HTTPException(404, "profile not found")
    profile = profiles.award_sticker(body.pid, body.game)
    return {"profile": profile}


@app.post("/api/parent/report")
def parent_report(body: PinRequest):
    if not profiles.check_pin(body.pid, body.pin):
        raise HTTPException(403, "wrong PIN")
    report = profiles.parent_report(body.pid)
    if not report:
        raise HTTPException(404, "profile not found")
    return {"report": report}


@app.get("/api/meta/grades")
def grade_meta():
    return {"subjects": {str(g): knowledge.list_available(g)
                         for g in range(1, 13)}}


@app.get("/api/meta/languages")
def language_meta():
    """Stage 8: languages buddies can speak."""
    return {"languages": [{"id": k, "name": v["name"], "voice_lang": v["voice_lang"]}
                          for k, v in conversation.LANGUAGES.items()]}


def _topic_from(subject: str, message: str) -> str:
    words = [w for w in message.split() if len(w) > 3][:4]
    return f"{subject}: {' '.join(words)}" if words else subject


# ---------------- static + PWA ----------------

@app.get("/manifest.json")
def manifest():
    return FileResponse(STATIC_DIR / "manifest.json", media_type="application/manifest+json")


@app.get("/sw.js")
def service_worker():
    return FileResponse(STATIC_DIR / "sw.js", media_type="application/javascript")


@app.get("/favicon.svg")
def favicon():
    return FileResponse(STATIC_DIR / "icons/favicon.svg", media_type="image/svg+xml")


@app.get("/icon-{rest}")
def icons(rest: str):
    path = STATIC_DIR / "icons" / f"icon-{rest}"
    if path.exists():
        return FileResponse(path)
    raise HTTPException(404)


@app.get("/health")
def health():
    return {"ok": True, "model": tutor.MODEL}


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
