"""Kinder Corner + grade-0 (KG) support tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import kinder, worlds
from app.main import app

client = TestClient(app)


def _mkprofile(name="Kiddo", grade=0, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- grade 0 onboarding ----------

def test_grade0_profile():
    pid = _mkprofile("ZeroKid", 0)
    r = client.get(f"/api/profile/{pid}")
    assert r.status_code == 200
    assert r.json()["profile"]["grade"] == 0


def test_grade0_world_is_meadow():
    pid = _mkprofile("MeadowKid", 0)
    r = client.get(f"/api/worlds/for-profile/{pid}")
    assert r.status_code == 200
    assert r.json()["world"]["id"] == "meadow"


def test_meadow_in_roster():
    ids = {w["id"] for w in worlds.roster()}
    assert "meadow" in ids and "village" in ids


def test_resolve_world_kg():
    assert worlds.resolve_world(0)["id"] == "meadow"
    assert worlds.resolve_world(None)["id"] == "meadow"
    assert worlds.resolve_world(1)["id"] == "village"


# ---------- kinder tasks ----------

def test_make_task_all_kinds():
    for kind in kinder.KINDS:
        t = kinder.make_task(kind)
        assert t and t["kind"] == kind
        assert len(t["options"]) == 3
        ids = [o["id"] for o in t["options"]]
        assert len(set(ids)) == 3, "options must be distinct"
        assert t["answer"] in ids
        assert t["say"].strip()


def test_make_round_five_tasks():
    tasks = kinder.make_round()
    assert len(tasks) == 5
    kinds = {t["kind"] for t in tasks}
    assert kinds == set(kinder.KINDS)


def test_kinder_context_letters():
    ctx = kinder.kinder_context("what sound does the letter B make?")
    assert "PHONICS" in ctx.upper()
    ctx2 = kinder.kinder_context("let's count to ten")
    assert "COUNTING" in ctx2.upper()
    ctx3 = kinder.kinder_context("what shape is a ball?")
    assert "SHAPES" in ctx3.upper()
    assert kinder.kinder_context("who is the president") == ""


def test_kinder_tone_only_little():
    assert "LITTLE LEARNER" in kinder.kinder_tone(0)
    assert "LITTLE LEARNER" in kinder.kinder_tone(2)
    assert kinder.kinder_tone(3) == ""


# ---------- kinder API ----------

def test_kinder_round_api():
    pid = _mkprofile("ApiKid", 0)
    r = client.get(f"/api/kinder/{pid}")
    assert r.status_code == 200
    d = r.json()
    assert len(d["tasks"]) == 5
    assert d["grade"] == 0
    r2 = client.get(f"/api/kinder/{pid}/phonics")
    assert r2.status_code == 200
    assert len(r2.json()["tasks"]) == 5
    assert client.get(f"/api/kinder/{pid}/nope").status_code == 404
    assert client.get("/api/kinder/nope").status_code == 404


def test_kinder_finish_points_once_a_day():
    pid = _mkprofile("PointKid", 0)
    r = client.post(f"/api/kinder/{pid}/finish",
                    json={"kind": "phonics", "correct": 4, "total": 5})
    assert r.status_code == 200
    d = r.json()["result"]
    assert d["points_awarded"] == 2
    # same-day repeat: honest zero
    r2 = client.post(f"/api/kinder/{pid}/finish",
                     json={"kind": "phonics", "correct": 5, "total": 5})
    assert r2.json()["result"]["points_awarded"] == 0
    # different game still pays
    r3 = client.post(f"/api/kinder/{pid}/finish",
                     json={"kind": "counting", "correct": 3, "total": 5})
    assert r3.json()["result"]["points_awarded"] == 2


def test_kg_practice_list_empty():
    pid = _mkprofile("EmptyKid", 0)
    r = client.get(f"/api/practice/{pid}")
    assert r.status_code == 200
    assert r.json()["topics"] == []


def test_pace_and_style_for_kg():
    from app import conversation, neural_voice
    assert conversation.pace_for_grade(0) == 0.82
    assert neural_voice.grade_style(0)["max_words_per_breath"] == 6
