"""Stage G: interactive conversational stories."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import conversation
from app.main import app

client = TestClient(app)


def _mk(name="Story", grade=2):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234"})
    assert r.status_code == 200
    return r.json()["pid"]


def test_interactive_roster():
    r = client.get("/api/stories/interactive")
    assert r.status_code == 200
    stories = r.json()["stories"]
    assert len(stories) >= 4
    assert all(s["beats"] >= 4 for s in stories)
    assert all(s["character"] for s in stories)


def test_story_detail_and_404():
    r = client.get("/api/stories/interactive/brave_mouse")
    assert r.status_code == 200
    assert r.json()["story"]["moral"]
    assert client.get("/api/stories/interactive/nope").status_code == 404


def test_beats_flow_and_final_moral():
    pid = _mk()
    for beat in range(6):
        r = client.post("/api/story/tell", json={
            "pid": pid, "story": "brave_mouse", "beat": beat,
            "reply": "I think Chintu should help!" if beat else ""})
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["spoken"]
        if beat < 5:
            assert not d["final"]
        else:
            assert d["final"]
            assert d["moral"]
            assert "THE END" in d["spoken"] or d["moral"] in d["spoken"]
    prof = client.get(f"/api/profile/{pid}").json()["profile"]
    assert prof["stickers"].get("story_brave_mouse", 0) == 1
    import pathlib
    pathlib.Path(f"data/profiles/{pid}.json").unlink(missing_ok=True)


def test_beat_out_of_range():
    pid = _mk()
    r = client.post("/api/story/tell", json={
        "pid": pid, "story": "brave_mouse", "beat": 99})
    assert r.status_code == 422
    r = client.post("/api/story/tell", json={
        "pid": pid, "story": "unknown", "beat": 0})
    assert r.status_code == 404
    import pathlib
    pathlib.Path(f"data/profiles/{pid}.json").unlink(missing_ok=True)


def test_story_rules_exist():
    assert "INTERACTIVE STORY MODE" in conversation.STORY_RULES
