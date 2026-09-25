"""Rework tests: but-why, quests, stickers, paid levels are GONE.

Free practice + points remain. English-only language rules stay.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import conversation
from app.main import app

client = TestClient(app)


def _mk(name="Reworky", grade=2, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


def test_english_only_languages():
    assert list(conversation.LANGUAGES.keys()) == ["en"]
    assert conversation.LANGUAGES["en"]["voice_lang"] == "en-US"


# ---------- removed features stay removed ----------
def test_but_why_removed():
    assert not hasattr(conversation, "WHY_RULES")
    assert not hasattr(conversation, "QUEST_POOL")
    assert not hasattr(conversation, "quest_public")


def test_quest_and_sticker_endpoints_gone():
    pid = _mk()
    assert client.get("/api/quests").status_code in (404, 405)
    assert client.post(f"/api/profile/{pid}/quest/nope").status_code in (404, 405)
    assert client.post(f"/api/profile/{pid}/sticker",
                       json={"sticker": "chat"}).status_code in (404, 405)


def test_levels_endpoints_gone():
    pid = _mk()
    assert client.get(f"/api/levels/{pid}").status_code in (404, 405)
    assert client.post(f"/api/levels/{pid}/buy",
                       json={"level": 2}).status_code in (404, 405)


# ---------- free practice works ----------
def test_practice_list_free_no_locks():
    from app import practice
    pid = _mk("Freer", 4)
    r = client.get(f"/api/practice/{pid}")
    assert r.status_code == 200
    d = r.json()
    assert d["grade"] == 4
    assert d["points"] == 0
    topics = d["topics"]
    assert len(topics) >= 12  # a full curriculum spread, all open
    assert all("price" not in t and "locked" not in t for t in topics)
    assert all(t["points"] > 0 for t in topics)
    # engine level: every topic open for every grade
    for g in range(1, 13):
        assert len(practice.grade_topics(g)) >= 12


def test_practice_done_awards_points_once_per_day():
    pid = _mk("Pointy", 3)
    topics = client.get(f"/api/practice/{pid}").json()["topics"]
    t = topics[0]
    r = client.post(f"/api/practice/{pid}/{t['id']}/done",
                    json={"topic_id": t["id"]})
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["result"]["points_awarded"] == 10
    assert d["profile"]["points"] == 10
    assert d["profile"]["practice_done"][t["id"]]["times"]

    # same-day repeat: no double points, still allowed
    r2 = client.post(f"/api/practice/{pid}/{t['id']}/done",
                     json={"topic_id": t["id"]})
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["result"]["points_awarded"] == 0
    assert d2["profile"]["points"] == 10

    # a different topic still pays
    t2 = topics[1]
    r3 = client.post(f"/api/practice/{pid}/{t2['id']}/done",
                     json={"topic_id": t2["id"]})
    assert r3.json()["profile"]["points"] == 20


def test_practice_unknown_topic_rejected():
    pid = _mk("Unknowny", 5)
    r = client.post(f"/api/practice/{pid}/nope_topic/done",
                    json={"topic_id": "nope_topic"})
    assert r.status_code == 400


def test_practice_topic_detail():
    pid = _mk("Detaily", 6)
    topics = client.get(f"/api/practice/{pid}").json()["topics"]
    t = topics[0]
    r = client.get(f"/api/practice/{pid}/{t['id']}")
    assert r.status_code == 200
    assert r.json()["topic"]["title"] == t["title"]


# ---------- stories keep working (no stickers) ----------
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
    assert "character" in st
    assert client.get("/api/stories/missing_id").status_code == 404
