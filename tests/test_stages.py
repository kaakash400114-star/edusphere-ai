"""Tests for voices, memory, games, stickers, report (English-only app)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import conversation
from app.main import app

client = TestClient(app)


def _mkprofile(name="StageTester", grade=3, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- grade rules (final spec: 1-12 only, English only) ----------
def test_grade_1_to_12_only():
    r = client.post("/api/profile", json={
        "name": "Zero", "grade": 0, "parent_pin": "1234"})
    assert r.status_code == 422
    r = client.post("/api/profile", json={
        "name": "Thirteen", "grade": 13, "parent_pin": "1234"})
    assert r.status_code == 422
    assert client.post("/api/profile", json={
        "name": "One", "grade": 1, "parent_pin": "1234"}).status_code == 200
    assert client.post("/api/profile", json={
        "name": "Twelve", "grade": 12, "parent_pin": "1234"}).status_code == 200


def test_no_age_field_needed():
    r = client.post("/api/profile", json={
        "name": "Ageless", "grade": 4, "parent_pin": "1234"})
    assert r.status_code == 200
    assert "age" not in r.json()["profile"]


# ---------- stage 1: voices ----------
def test_voices_exist_for_all_buddies():
    from app import characters, neural_voice
    seen_voices = []
    for cid in characters.CHARACTERS:
        v = neural_voice.voice_public(cid)
        assert "rate" in v and "pitch" in v and "voice_hints" in v
        assert v.get("voice"), f"{cid} has no neural voice"
        seen_voices.append(v["voice"])
    assert len(set(seen_voices)) >= 8, f"voices too uniform: {seen_voices}"
    # distinct neural speaker per buddy across the cast
    # pitches stay human (Hz offsets, no cartoon extremes)
    for cid in characters.CHARACTERS:
        hz = int(neural_voice.BUDDY_VOICES[cid]["pitch"].replace("Hz", ""))
        assert -20 <= hz <= 20


def test_pace_for_grade():
    assert conversation.pace_for_grade(1) < conversation.pace_for_grade(6)
    assert conversation.pace_for_grade(2) == 0.90
    assert conversation.pace_for_grade(12) == 1.18


def test_chat_returns_english_voice_profile():
    pid = _mkprofile("Voicey", 3)
    r = client.post("/api/chat", json={"pid": pid, "message": "hello there"})
    assert r.status_code == 200
    v = r.json()["voice"]
    assert "rate" in v and "pace" in v
    assert v["lang"] == "en-US"


# ---------- stage 2: memory ----------
def test_remember_and_report():
    pid = _mkprofile("Memo", 2)
    r = client.post(f"/api/profile/{pid}/remember",
                    json={"text": "has a dog named Kutta"})
    assert r.status_code == 200
    assert "has a dog named Kutta" in r.json()["profile"]["memories"]


# ---------- stage 5: games ----------
def test_game_result_awards_stars_and_practice_event():
    pid = _mkprofile("Gamer", 4)
    r = client.post("/api/game/result", json={
        "pid": pid, "game": "math_sprint", "score": 7, "stars": 3})
    assert r.status_code == 200
    prof = r.json()["profile"]
    assert prof["stars"] >= 3
    assert not hasattr(prof, "stickers") and "stickers" not in prof
    # one practice event recorded for the honest improvement rate
    assert prof["practice_log"], "game result missing from practice_log"
    ev = prof["practice_log"][-1]
    assert ev["subject"] == "math" and ev["correct"] == 7 and ev["total"] == 7


# ---------- stage 7: weekly report (stickers gone, points in) ----------
def test_report_has_week_and_points():
    pid = _mkprofile("Reporty", 5)
    client.post("/api/game/result", json={
        "pid": pid, "game": "quiz_quest", "score": 5, "stars": 2})
    r = client.post("/api/parent/report", json={"pid": pid, "pin": "1234"})
    assert r.status_code == 200
    rep = r.json()["report"]
    assert "week" in rep and "points" in rep
    assert "stickers" not in rep
