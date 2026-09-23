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

from . import characters, knowledge, profiles, tutor

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
    grade: int = Field(ge=1, le=12)
    parent_pin: str = Field(min_length=4, max_length=8)
    character: str = "auto"

    @field_validator("character")
    @classmethod
    def buddy_exists(cls, v: str) -> str:
        if v != "auto" and v not in characters.CHARACTERS:
            raise ValueError("unknown buddy")
        return v


class ProfileUpdate(BaseModel):
    grade: int | None = Field(default=None, ge=1, le=12)
    character: str | None = None


class ChatRequest(BaseModel):
    pid: str
    message: str = Field(min_length=1, max_length=2000)
    history: list[dict] = Field(default_factory=list, max_length=20)


class PinRequest(BaseModel):
    pid: str
    pin: str = Field(min_length=4, max_length=8)


# ---------------- API ----------------

@app.post("/api/profile")
def create_profile(body: ProfileCreate):
    try:
        profile = profiles.create_profile(
            body.name, body.grade, body.parent_pin, body.character)
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
        weak_areas=list(profile.get("weak_areas", {}).keys()))
    topic = _topic_from(subject, body.message)
    updated = profiles.record_activity(body.pid, "chat", topic)
    buddy = characters.public(profile.get("character") or "leo")
    return {"answer": answer, "subject": subject, "topic": topic,
            "stars": updated["stars"] if updated else 0,
            "character": buddy["id"], "character_name": buddy["name"],
            "character_emoji": buddy["emoji"]}


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
