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
    from app import characters
    seen_hints = []
    for cid in characters.CHARACTERS:
        v = conversation.voice_public(cid)
        assert "rate" in v and "pitch" in v and "act" in v
        assert v.get("voice_hints"), f"{cid} has no voice_hints"
        seen_hints.append(v["voice_hints"][0])
    assert conversation.voice_public("chintu")["pitch"] < 0.8  # deep elephant
    # distinct lead voices: at least 3 different real voices across the cast
    assert len(set(seen_hints)) >= 3, f"voices too uniform: {seen_hints}"
    # pitches stay human (no cartoon squeak/deep)
    for cid in characters.CHARACTERS:
        assert 0.6 <= conversation.voice_public(cid)["pitch"] <= 1.3


def test_pace_for_grade():
    assert conversation.pace_for_grade(1) < conversation.pace_for_grade(6)
    assert conversation.pace_for_grade(2) == 0.85


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
def test_game_result_awards_stars_and_sticker():
    pid = _mkprofile("Gamer", 4)
    r = client.post("/api/game/result", json={
        "pid": pid, "game": "math_sprint", "score": 7, "stars": 3})
    assert r.status_code == 200
    prof = r.json()["profile"]
    assert prof["stars"] >= 3
    assert prof["stickers"].get("math_sprint", 0) >= 1


# ---------- stage 6: stickers ----------
def test_sticker_award():
    pid = _mkprofile("Sticky", 1)
    r = client.post(f"/api/profile/{pid}/sticker", json={"sticker": "chat"})
    assert r.status_code == 200
    assert r.json()["profile"]["stickers"]["chat"] == 1


# ---------- stage 7: weekly report ----------
def test_report_has_week_and_stickers():
    pid = _mkprofile("Reporty", 5)
    client.post("/api/game/result", json={
        "pid": pid, "game": "quiz_quest", "score": 5, "stars": 2})
    r = client.post("/api/parent/report", json={"pid": pid, "pin": "1234"})
    assert r.status_code == 200
    rep = r.json()["report"]
    assert "week" in rep and "stickers" in rep
    assert rep["stickers"].get("quiz_quest", 0) >= 1
