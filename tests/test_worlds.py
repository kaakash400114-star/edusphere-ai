"""Tests for Part 2 — The Four Worlds."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import characters, worlds
from app.main import app

client = TestClient(app)


# ---------- unit: world resolution ----------
def test_resolve_by_grade():
    assert worlds.resolve_world(1)["id"] == "village"
    assert worlds.resolve_world(2)["id"] == "village"
    assert worlds.resolve_world(3)["id"] == "mountains"
    assert worlds.resolve_world(5)["id"] == "mountains"
    assert worlds.resolve_world(8)["id"] == "mountains"  # top land


def test_resolve_by_age():
    assert worlds.resolve_world(None, 2)["id"] == "meadow"
    assert worlds.resolve_world(None, 3)["id"] == "meadow"
    assert worlds.resolve_world(None, 4)["id"] == "kindergarten"
    assert worlds.resolve_world(None, 5)["id"] == "kindergarten"
    assert worlds.resolve_world(None, None)["id"] == "kindergarten"  # default


def test_world_fields():
    for w in worlds.roster():
        assert w["name"] and w["emoji"] and w["tagline"]
        assert len(w["activities"]) >= 4
        assert all(a["prompt"] and a["label"] for a in w["activities"])
        assert all(h in characters.CHARACTERS for h in w["host_ids"])


def test_knowledge_hint():
    assert worlds.knowledge_subject_hint("meadow", "math") == "meadow"
    assert worlds.knowledge_subject_hint("kindergarten", "science") == "kindergarten"
    assert worlds.knowledge_subject_hint("village", "math") == "math"
    assert worlds.knowledge_subject_hint("mountains", "general") == "general"


def test_world_prompt_contains_style():
    p = worlds.world_prompt(worlds.WORLDS["meadow"])
    assert "Sunny Meadow" in p and "8 words" in p


# ---------- API: worlds ----------
def test_api_worlds():
    r = client.get("/api/worlds")
    assert r.status_code == 200
    ws = r.json()["worlds"]
    assert [w["id"] for w in ws] == ["meadow", "kindergarten", "village", "mountains"]


def test_api_world_for_profile():
    r = client.post("/api/profile", json={
        "name": "Worldy", "grade": 4, "parent_pin": "4321"})
    assert r.status_code == 200
    pid = r.json()["pid"]
    r2 = client.get(f"/api/worlds/for-profile/{pid}")
    assert r2.status_code == 200
    assert r2.json()["world"]["id"] == "mountains"


def test_api_preschool_profile():
    r = client.post("/api/profile", json={
        "name": "Tiny", "grade": 0, "parent_pin": "4321", "age": 3})
    assert r.status_code == 200
    pid = r.json()["pid"]
    prof = r.json()["profile"]
    assert prof["age"] == 3 and prof["grade"] == 0
    r2 = client.get(f"/api/worlds/for-profile/{pid}")
    assert r2.json()["world"]["id"] == "meadow"


def test_api_preschool_requires_age():
    r = client.post("/api/profile", json={
        "name": "NoAge", "grade": 0, "parent_pin": "4321"})
    assert r.status_code == 400


def test_chat_returns_world():
    r = client.post("/api/profile", json={
        "name": "Chatty", "grade": 1, "parent_pin": "4321"})
    pid = r.json()["pid"]
    r2 = client.post("/api/chat", json={"pid": pid, "message": "hello buddy"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["world"] == "village"
    assert data["world_name"] == "Explorer Village"
    assert data["answer"]


# ---------- knowledge routing ----------
def test_meadow_knowledge_file():
    from app import knowledge
    path = knowledge.knowledge_path("meadow", 0)
    assert path is not None and path.exists()
    assert "meadow_activities" in str(path)
    text = path.read_text(encoding="utf-8")
    assert "Animal Sounds" in text


def test_kindergarten_knowledge_file():
    from app import knowledge
    path = knowledge.knowledge_path("kindergarten", 0)
    assert path is not None and path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Letter of the Day" in text
