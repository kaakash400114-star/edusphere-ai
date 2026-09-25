"""Stage 9 magic extras + English-only language rules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import conversation
from app.main import app

client = TestClient(app)


def _mk(name="Questy", grade=2, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


def test_english_only_languages():
    assert list(conversation.LANGUAGES.keys()) == ["en"]
    assert conversation.LANGUAGES["en"]["voice_lang"] == "en-US"


def test_quests_list_and_complete():
    r = client.get("/api/quests")
    assert r.status_code == 200
    quests = r.json()["quests"]
    assert len(quests) >= 5 and all("id" in q and "title" in q for q in quests)
    pid = _mk()
    qid = quests[0]["id"]
    r2 = client.post(f"/api/profile/{pid}/quest/{qid}")
    assert r2.status_code == 200
    prof = r2.json()["profile"]
    assert prof["stars"] >= 2
    assert prof["stickers"].get("quest_" + qid, 0) == 1
    assert any(e["kind"] == "quest:" + qid for e in prof["log"])


def test_quest_unknown_rejected():
    pid = _mk()
    r = client.post(f"/api/profile/{pid}/quest/nope")
    assert r.status_code == 400


def test_stories_roster_and_reader():
    r = client.get("/api/stories")
    assert r.status_code == 200
    roster = r.json()["stories"]
    assert len(roster) >= 3
    sid = roster[0]["id"]
    r2 = client.get(f"/api/stories/{sid}")
    assert r2.status_code == 200
    st = r2.json()["story"]
    assert len(st["words"]) >= 8 and all(isinstance(w, str) for w in st["words"])
    assert "character" in st  # stage G: interactive stories use animal names
    assert client.get("/api/stories/missing_id").status_code == 404


def test_why_rules_exist():
    assert "BUT WHY MODE" in conversation.WHY_RULES
    assert "because I said so" in conversation.WHY_RULES
