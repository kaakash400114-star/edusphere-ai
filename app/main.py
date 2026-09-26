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

from . import (boards, characters, conversation, improvement, knowledge,
               knowledge_fresh, kinder, neural_voice, practice, profiles,
               tutor, worlds)

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="EduSphere AI", docs_url=None, redoc_url=None)


@app.on_event("startup")
def _start_self_updating_knowledge() -> None:
    """The curriculum maintains itself from the moment the app boots."""
    knowledge_fresh.start()


# tiny in-memory rate limiter: pid -> last request ts
_last_req: dict[str, float] = {}
# hourly LLM budget per profile: pid -> [timestamps]
_chat_hist: dict[str, list[float]] = {}


def _rate_ok(pid: str, min_gap: float = 2.0) -> bool:
    now = time.time()
    if now - _last_req.get(pid, 0) < min_gap:
        return False
    _last_req[pid] = now
    # prune old entries so the dict cannot grow forever
    if len(_last_req) > 5000:
        cutoff = now - 3600
        for k in [k for k, v in _last_req.items() if v < cutoff]:
            _last_req.pop(k, None)
    return True


def _burst_ok(pid: str, max_per_hour: int = 240) -> bool:
    """Hourly cap per profile (default: 4 LLM chats a minute sustained)."""
    now = time.time()
    hist = [t for t in _chat_hist.get(pid, []) if now - t < 3600]
    if len(hist) >= max_per_hour:
        _chat_hist[pid] = hist
        return False
    hist.append(now)
    _chat_hist[pid] = hist
    return True


# ---------------- models ----------------

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    grade: int = Field(ge=0, le=12)  # grade 0 = KG little learners
    # PIN is OPTIONAL now — parents MAY set one to lock the report; kids can
    # sign up alone and are never blocked.
    parent_pin: str | None = Field(default=None, min_length=4, max_length=8)
    character: str = "auto"
    board: str = boards.DEFAULT_BOARD

    @field_validator("character")
    @classmethod
    def buddy_exists(cls, v: str) -> str:
        if v != "auto" and v not in characters.CHARACTERS:
            raise ValueError("unknown buddy")
        return v

    @field_validator("board")
    @classmethod
    def board_exists(cls, v: str) -> str:
        return boards.normalize_board(v)


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=20)
    grade: int | None = Field(default=None, ge=0, le=12)
    character: str | None = None
    board: str | None = None
    voice_speed: float | None = Field(default=None, ge=0.5, le=2.0)
    voice_on: bool | None = None
    parent_pin: str | None = Field(default=None, min_length=4, max_length=8)


class SettingsUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=20)
    grade: int | None = Field(default=None, ge=0, le=12)
    character: str | None = None
    board: str | None = None
    voice_speed: float | None = Field(default=None, ge=0.5, le=2.0)
    voice_on: bool | None = None
    current_pin: str | None = Field(default=None, max_length=8)
    # Empty string allowed = "remove the PIN"; 4-8 digits = set/change.
    new_pin: str | None = Field(default=None, max_length=8)


class ChatRequest(BaseModel):
    pid: str
    message: str = Field(min_length=1, max_length=2000)
    history: list[dict] = Field(default_factory=list, max_length=20)
    mode: str | None = None


class PinRequest(BaseModel):
    pid: str
    # Empty allowed: profiles with NO parent PIN never need one to read the report.
    pin: str = Field(default="", max_length=8)


class TaskDoneRequest(BaseModel):
    topic_id: str = Field(min_length=1, max_length=80)
    grade: int = Field(default=0, ge=0, le=12)


# ---------------- API ----------------

@app.post("/api/profile")
def create_profile(body: ProfileCreate):
    try:
        profile = profiles.create_profile(
            body.name, body.grade, body.parent_pin, body.character,
            board=body.board)
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
    changes = body.model_dump()
    if changes.get("parent_pin") is not None:
        if not profiles.check_pin(pid, changes.pop("current_pin") or ""):
            raise HTTPException(403, "current PIN is wrong")
    profile = profiles.update_profile(pid, **changes)
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"profile": profile}


@app.get("/api/settings/{pid}")
def get_settings(pid: str):
    """Everything the Account Settings page shows, in one call."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    raw = profiles._raw(pid) or {}
    return {
        "profile": profile,
        "boards": boards.board_public(),
        "improvement": improvement.improvement_report(raw, profile["grade"]),
        # Frontend shows the PIN row only when a parent actually set one.
        "has_pin": profiles.has_pin(pid),
    }


@app.post("/api/settings/{pid}")
def save_settings(pid: str, body: SettingsUpdate):
    """Save the Account Settings page (PIN change requires the current PIN)."""
    if body.character is not None and body.character not in characters.CHARACTERS:
        raise HTTPException(400, "unknown buddy")
    changes = {"name": body.name, "grade": body.grade,
               "character": body.character, "board": body.board,
               "voice_speed": body.voice_speed, "voice_on": body.voice_on}
    changes = {k: v for k, v in changes.items() if v is not None}
    if body.new_pin is not None:
        if not profiles.check_pin(pid, body.current_pin or ""):
            raise HTTPException(403, "current PIN is wrong")
        changes["parent_pin"] = body.new_pin
    elif body.current_pin is not None and body.current_pin == "":
        changes["parent_pin"] = ""   # explicit clear — remove the PIN
    if changes.get("grade") is not None:
        raw = profiles._raw(pid)
        if raw and raw.get("grade") != changes["grade"]:
            raw["grade_changes"] = raw.get("grade_changes", [])
            raw["grade_changes"].append(
                {"t": time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "from": raw.get("grade"), "to": changes["grade"]})
            profiles._write_raw(pid, raw)
    profile = profiles.update_profile(pid, **changes)
    if not profile:
        raise HTTPException(404, "profile not found")
    raw = profiles._raw(pid) or {}
    return {"profile": profile,
            "improvement": improvement.improvement_report(raw, profile["grade"])}


@app.get("/api/characters")
def list_characters():
    """The Character Universe roster, in carousel order."""
    return {"characters": characters.roster()}


@app.get("/api/boards")
def list_boards():
    """Curriculum boards for onboarding + settings pickers."""
    return {"boards": boards.board_public()}


@app.get("/api/worlds")
def list_worlds():
    """The Four Worlds roster, in grade order."""
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
    if not _rate_ok(body.pid) or not _burst_ok(body.pid):
        return JSONResponse(
            {"error": "easy there! take a short break and try again."},
            status_code=429)
    subject = tutor.detect_subject(body.message, max(1, profile["grade"]))
    answer = tutor.ask(
        name=profile["name"], grade=profile["grade"],
        buddy=profile.get("character") or "auto",
        question=body.message, history=body.history, subject=subject,
        weak_areas=list(profile.get("weak_areas", {}).keys()),
        mode=body.mode,
        memories=list(profile.get("memories", [])),
        board=profile.get("board"))
    topic = _topic_from(subject, body.message)
    updated = profiles.record_activity(body.pid, "chat", topic)
    buddy = characters.public(profile.get("character") or "leo")
    world = worlds.world_for_profile(profile)
    # Stage 3: ONE voice profile shape — neural voice for the mp3 path,
    # voice_hints kept for the browser Web Speech fallback.
    voice = neural_voice.voice_public(buddy["id"])
    voice["pace"] = conversation.pace_for_grade(profile.get("grade"))
    voice["lang"] = "en-US"
    # human-like neural voice: pre-synthesize the reply mp3 server-side,
    # with the grade-scaled pace baked in (Stage 3)
    audio_url = None
    mp3 = neural_voice.synth(buddy["id"], answer[:600],
                             pace=conversation.pace_for_grade(profile.get("grade")))
    if mp3:
        audio_url = "/tts/" + os.path.basename(mp3)
    voice["engine"] = "edge" if audio_url else "browser"
    voice["audio_url"] = audio_url
    # stage 2: the buddy may tuck a 'MEMORY: ...' line into its answer —
    # split it off (case-insensitive), save it, show only the spoken part
    memory_note = ""
    upper = answer.upper()
    pos = upper.find("MEMORY:")
    if pos != -1:
        memory_note = answer[pos + len("MEMORY:"):].strip().splitlines()[0][:120]
        answer = answer[:pos]
        if memory_note:
            profiles.remember(body.pid, memory_note)
    answer = answer.strip()
    return {"answer": answer, "subject": subject, "topic": topic,
            "stars": updated["stars"] if updated else 0,
            "memory_saved": memory_note,
            "character": buddy["id"], "character_name": buddy["name"],
            "character_emoji": buddy["emoji"],
            "world": world["id"], "world_name": world["name"],
            "world_emoji": world["emoji"],
            "voice": voice}


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
    """Record one arcade game result: stars + one practice event."""
    profile = profiles.record_activity(
        body.pid, "game:" + body.game, body.topic or body.game,
        stars=body.stars)
    if not profile:
        raise HTTPException(404, "profile not found")
    profiles.log_practice(
        body.pid, subject=_subject_from_game(body.game),
        correct=body.score, total=_game_total(body.game, body.score),
        source="game:" + body.game)
    return {"profile": profiles.get_profile(body.pid)}


def _subject_from_game(game: str) -> str:
    return {"math_sprint": "math", "boss_battle": "math",
            "quiz_quest": "general", "spelling_bee": "english"}.get(game, "general")


def _game_total(game: str, score: int) -> int:
    # total questions each game asks at full play (upper-bounded by score)
    totals = {"math_sprint": score, "quiz_quest": 10,
              "spelling_bee": 8, "boss_battle": score}
    return totals.get(game, max(1, score))


@app.get("/api/stories")
def list_stories():
    """Read-along stories."""
    return {"stories": conversation.stories_roster()}


class StoryTellRequest(BaseModel):
    pid: str
    story: str = Field(min_length=1, max_length=60)
    beat: int = Field(ge=0, le=10)
    reply: str = Field(default="", max_length=1000)


def _interactive_roster() -> list[dict]:
    out = []
    for sid, s in conversation.INTERACTIVE_STORIES.items():
        out.append({"id": sid, "title": s["title"], "emoji": s["emoji"],
                    "character": s["character"], "beats": len(s["beats"])})
    return out


@app.get("/api/stories/interactive")
def list_interactive():
    """Stage G: conversational stories roster."""
    return {"stories": _interactive_roster()}


@app.get("/api/stories/interactive/{sid}")
def get_interactive(sid: str):
    s = conversation.INTERACTIVE_STORIES.get(sid)
    if not s:
        raise HTTPException(404, "story not found")
    return {"story": {"id": sid, **{k: s[k] for k in
            ("title", "emoji", "character")}, "beats": len(s["beats"]),
            "moral": s["moral"]}}


@app.post("/api/story/tell")
def story_tell(body: StoryTellRequest):
    """One interactive story turn: the animal speaks this beat.

    The child's reply to the previous beat is woven in. Returns the
    animal's spoken line + whether this was the final beat.
    """
    profile = profiles.get_profile(body.pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    s = conversation.INTERACTIVE_STORIES.get(body.story)
    if not s:
        raise HTTPException(404, "story not found")
    beats = s["beats"]
    if body.beat < 0 or body.beat >= len(beats):
        raise HTTPException(400, "beat out of range")
    narration = beats[body.beat]
    final = body.beat == len(beats) - 1

    # Personalize with the child's name in beat 0 and the final beat
    name = profile["name"]
    if body.beat == 0:
        narration = f"Hello {name}! Come close — I have a story for you. {narration}"
    if final:
        narration = f"{narration} THE END. Moral of the story: {s['moral']}"

    # If a reply was given, run one live tutor turn so the animal reacts to
    # the child's idea in-character (best-effort; fall back to narration).
    spoken = narration
    if body.reply.strip():
        reacted = tutor.ask(
            name=name, grade=profile["grade"],
            buddy=profile.get("character") or "auto",
            question=(f"[The child answers the story: '{body.reply.strip()}'] "
                      f"[Continue this story beat in-character: {narration}]"),
            history=[], subject="general",
            weak_areas=[], mode="story",
            memories=list(profile.get("memories", [])))
        if reacted and "brain took a nap" not in reacted \
                and "Setup needed" not in reacted:
            spoken = reacted
    profiles.record_activity(body.pid, "story:" + body.story,
                             "interactive story")
    return {"beat": body.beat, "final": final, "spoken": spoken,
            "moral": s["moral"] if final else ""}


@app.get("/api/stories/{sid}")
def get_story(sid: str):
    if sid not in conversation.STORIES:
        raise HTTPException(404, "story not found")
    return {"story": {"id": sid, **conversation.story_public(sid)}}


@app.post("/api/parent/report")
def parent_report(body: PinRequest):
    if not profiles.check_pin(body.pid, body.pin):
        raise HTTPException(403, "wrong PIN")
    report = profiles.parent_report(body.pid)
    if not report:
        raise HTTPException(404, "profile not found")
    report["improvement"] = profiles.improvement_section(body.pid)
    report["pin_protected"] = profiles.has_pin(body.pid)
    return {"report": report}


@app.get("/api/meta/grades")
def grade_meta():
    return {"subjects": {str(g): knowledge.list_available(g)
                         for g in range(1, 13)}}


# ---------------- practice (free, replaces paid levels) ----------------

@app.get("/api/practice/{pid}")
def get_practice(pid: str):
    """All free practice topics for the kid's grade, with done marks."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    topics = [] if profile["grade"] < 1 else practice.grade_topics(profile["grade"])
    return {"grade": profile["grade"],
            "points": profiles.get_points(profile),
            "topics": topics}


@app.get("/api/practice/{pid}/{topic_id}")
def get_topic(pid: str, topic_id: str):
    """One practice topic's full prompt (frontend starts the chat task)."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    t = practice.topic_by_id(profile["grade"], topic_id)
    if not t:
        raise HTTPException(404, "topic not found")
    return {"topic": t, "grade": profile["grade"]}


@app.post("/api/practice/{pid}/{topic_id}/done")
def finish_topic(pid: str, topic_id: str, body: TaskDoneRequest):
    """Mark one practice topic done: +points, no locks, no price."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    t = practice.topic_by_id(profile["grade"], topic_id)
    if not t:
        raise HTTPException(400, "unknown topic")
    raw = profiles._raw(pid)
    payload = practice.mark_done(raw, t)
    profiles._write_raw(pid, raw)
    profiles.log_practice(pid, subject=t["subject"], correct=1, total=1,
                          source="practice")
    return {"result": payload, "profile": profiles.get_profile(pid)}


def _topic_from(subject: str, message: str) -> str:
    words = [w for w in message.split() if len(w) > 3][:4]
    return f"{subject}: {' '.join(words)}" if words else subject


# ---------------- kinder corner (little learners, KG) --------------------

class KinderFinish(BaseModel):
    kind: str = Field(min_length=1, max_length=20)
    correct: int = Field(default=0, ge=0, le=50)
    total: int = Field(default=5, ge=0, le=50)


@app.get("/api/kinder/{pid}")
def kinder_round(pid: str):
    """A fresh little-learner round: phonics, counting, shapes, colors, rhymes."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    return {"grade": profile["grade"],
            "points": profiles.get_points(profile),
            "games": kinder.KINDS,
            "tasks": kinder.make_round()}


@app.get("/api/kinder/{pid}/{kind}")
def kinder_one(pid: str, kind: str):
    """More tasks of one kind (e.g. more phonics taps)."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    if kind not in kinder.KINDS:
        raise HTTPException(404, "unknown kinder game")
    tasks = [kinder.make_task(kind) for _ in range(kinder.kinder_round_size())]
    return {"kind": kind, "tasks": [t for t in tasks if t]}


@app.post("/api/kinder/{pid}/finish")
def kinder_finish(pid: str, body: KinderFinish):
    """One finished kinder round: +2 points for the first correct round of
    the day per game, one honest practice event."""
    profile = profiles.get_profile(pid)
    if not profile:
        raise HTTPException(404, "profile not found")
    raw = profiles._raw(pid)
    payload = kinder.mark_round(raw, body.kind, body.correct, body.total)
    profiles._write_raw(pid, raw)
    if body.correct >= 1:
        profiles.log_practice(pid,
                              subject=("english" if body.kind in
                                       ("phonics", "rhymes") else "math"),
                              correct=body.correct,
                              total=max(1, body.total),
                              source="kinder:" + body.kind)
    profiles.record_activity(pid, "kinder:" + body.kind, "kinder corner")
    return {"result": payload, "profile": profiles.get_profile(pid)}


# ---------------- self-updating knowledge ----------------

@app.get("/api/knowledge/health")
def knowledge_health():
    """Live self-check: is every curriculum section backed by real content?"""
    return knowledge_fresh.health()


@app.post("/api/knowledge/refresh")
def knowledge_refresh():
    """Manual trigger for one healing pass (also runs automatically)."""
    return knowledge_fresh.refresh_pass(max_files=6)


# ---------------- neural TTS audio serving ----------------

@app.get("/tts/{fname}")
def tts_audio(fname: str):
    import tempfile
    path = os.path.join(tempfile.gettempdir(), "edusphere_tts", fname)
    # only hashed mp3 filenames, no traversal
    if (fname.endswith(".mp3") and "/" not in fname and "\\" not in fname
            and os.path.exists(path)):
        return FileResponse(path, media_type="audio/mpeg")
    raise HTTPException(404)


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


# static frontend last, so API routes above win
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
