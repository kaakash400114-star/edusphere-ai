"""Tests for stages 1,2,5,6,7,8 — voices, memory, games, stickers, report, languages."""
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


# ---------- stage 1: voices ----------
def test_voices_exist_for_all_buddies():
    from app import characters
    for cid in characters.CHARACTERS:
        v = conversation.voice_public(cid)
        assert "rate" in v and "pitch" in v and "act" in v
    assert conversation.voice_public("chintu")["pitch"] < 0.8  # deep elephant
    assert conversation.voice_public("pip")["pitch"] > 1.2     # squeaky squirrel


def test_pace_for_grade():
    assert conversation.pace_for_grade(1) < conversation.pace_for_grade(6)
    assert conversation.pace_for_grade(None, 3) < conversation.pace_for_grade(6)


def test_chat_returns_voice_profile():
    pid = _mkprofile("Voicey", 3)
    r = client.post("/api/chat", json={"pid": pid, "message": "hello there"})
    assert r.status_code == 200
    v = r.json()["voice"]
    assert "rate" in v and "pace" in v and v["lang"] == "en-US"


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


# ---------- stage 8: languages ----------
def test_languages_meta():
    r = client.get("/api/meta/languages")
    langs = {l["id"]: l for l in r.json()["languages"]}
    assert langs["hi"]["voice_lang"] == "hi-IN"
    assert langs["ta"]["voice_lang"] == "ta-IN"


def test_chat_with_hindi_lang():
    pid = _mkprofile("HindiKid", 3)
    r = client.post("/api/chat", json={
        "pid": pid, "message": "hello", "lang": "hi"})
    assert r.status_code == 200
    assert r.json()["voice"]["lang"] == "hi-IN"
