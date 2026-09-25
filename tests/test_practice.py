"""New tests for the rework: free practice engine (replaces paid levels)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import curriculum_feed, practice
from app.main import app

client = TestClient(app)


def _mk(name="Practica", grade=3, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- engine rules ----------
def test_every_grade_has_free_topics():
    for g in range(1, 13):
        topics = practice.grade_topics(g)
        assert len(topics) >= 12, f"grade {g} thin topic pool: {len(topics)}"
        assert all(t["points"] > 0 for t in topics)
        # no locks / prices anywhere in the payloads
        assert all("level" not in t and "price" not in t for t in topics)


def test_topic_ids_resolve():
    for g in (1, 6, 12):
        for t in practice.grade_topics(g):
            assert practice.topic_by_id(g, t["id"]) is not None


def test_curriculum_feed_feed_unchanged():
    # the knowledge-file section split still reaches every subject
    for g in (1, 4, 8, 12):
        subs = {t["subject"] for t in curriculum_feed.grade_tasks(g)}
        assert subs >= {"math"}, f"grade {g} missing math topics"


# ---------- API flow: everything open from day one ----------
def test_all_topics_open_immediately():
    pid = _mk("Opener", 5)
    d = client.get(f"/api/practice/{pid}").json()
    # old world: only level 1 open, rest locked/bought. New world: all open.
    assert d["points"] == 0
    # any topic can be finished right away, even the last one
    last = d["topics"][-1]
    r = client.post(f"/api/practice/{pid}/{last['id']}/done",
                    json={"topic_id": last["id"]})
    assert r.status_code == 200, r.text
    assert r.json()["profile"]["points"] == practice.POINTS_PER_TOPIC


def test_no_purchase_endpoint():
    pid = _mk("Nonbuyer", 6)
    # buying levels is gone; nothing to pay for, ever
    assert client.post(f"/api/practice/{pid}/buy",
                       json={"anything": 1}).status_code in (404, 405)
