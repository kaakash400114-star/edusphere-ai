"""Story library verification: every interactive + read-along story checked."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import characters, conversation
from app.main import app

client = TestClient(app)


def _mk(name="StoryFan", grade=3, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- structural validation of every story ----------
def test_interactive_stories_structure():
    assert len(conversation.INTERACTIVE_STORIES) >= 16, \
        f"expected a big library, got {len(conversation.INTERACTIVE_STORIES)}"
    seen_titles = set()
    for sid, s in conversation.INTERACTIVE_STORIES.items():
        assert s["title"] and s["title"] not in seen_titles, f"{sid}: dup/empty title"
        seen_titles.add(s["title"])
        assert s["emoji"], f"{sid}: no emoji"
        assert s["character"], f"{sid}: no character"
        lo, hi = s["grade_band"]
        assert 1 <= lo <= hi <= 12, f"{sid}: bad grade_band {s['grade_band']}"
        assert s.get("topic_hint"), f"{sid}: no topic_hint"
        assert 5 <= len(s["beats"]) <= 8, f"{sid}: beats={len(s['beats'])}"
        assert s.get("moral") and len(s["moral"]) > 20, f"{sid}: weak moral"
        for i, beat in enumerate(s["beats"]):
            assert beat.strip(), f"{sid} beat {i}: empty"
            assert len(beat) < 600, f"{sid} beat {i}: too long ({len(beat)})"
        # last beat must contain the ending (no moral spill-over)
        assert "THE END" not in s["beats"][-1], f"{sid}: moral injected in beats"


def test_readalong_stories_structure():
    assert len(conversation.STORIES) >= 8, \
        f"expected a big read-along library, got {len(conversation.STORIES)}"
    for sid, s in conversation.STORIES.items():
        assert s["title"], f"{sid}: no title"
        assert s["emoji"] and s["character"], f"{sid}: missing emoji/character"
        assert 8 <= len(s["words"]) <= 20, f"{sid}: pages={len(s['words'])}"
        for i, line in enumerate(s["words"]):
            assert line.strip(), f"{sid} page {i}: empty line"
            words = line.split()
            # read-along pages must be short enough for word-by-word reading
            assert len(words) <= 9, f"{sid} page {i}: {len(words)} words too long"
            # kid-safe: no scary words
            low = line.lower()
            for bad in ("kill", "blood", "die", "hate"):
                assert bad not in low, f"{sid} page {i}: unsafe word '{bad}'"


def test_all_story_characters_are_real_buddies():
    """Every story's character should map to the buddy cast (checked loosely)."""
    first_names = {c["name"].split()[0].lower() for c in characters.roster()}
    first_names |= set(characters.CHARACTERS.keys())   # ids: nova etc.
    for sid, s in conversation.INTERACTIVE_STORIES.items():
        char = s["character"].lower()
        assert any(name in char for name in first_names), \
            f"{sid}: character '{s['character']}' not from the buddy cast"

# ---------- API behaviour across the whole library ----------
def test_interactive_roster_matches_dict():
    r = client.get("/api/stories/interactive")
    assert r.status_code == 200
    roster = r.json()["stories"]
    assert len(roster) == len(conversation.INTERACTIVE_STORIES)
    by_id = {s["id"] for s in roster}
    assert by_id == set(conversation.INTERACTIVE_STORIES.keys())


def test_every_interactive_story_full_walk_first_beats():
    """Walk beats 0-1 of EVERY interactive story (no live tutor in tests)."""
    pid = _mk("Walker", 4)
    for sid in conversation.INTERACTIVE_STORIES:
        for beat in (0, 1):
            r = client.post("/api/story/tell", json={
                "pid": pid, "story": sid, "beat": beat, "reply": ""})
            assert r.status_code == 200, f"{sid} beat {beat}: {r.text}"
            d = r.json()
            assert d["spoken"], f"{sid} beat {beat}: empty spoken"
            if beat == 0:
                assert "Walker" in d["spoken"]  # name personalization
            assert not d["final"]


def test_every_interactive_story_final_beat():
    pid = _mk("Finisher", 5)
    for sid, s in conversation.INTERACTIVE_STORIES.items():
        last = len(s["beats"]) - 1
        r = client.post("/api/story/tell", json={
            "pid": pid, "story": sid, "beat": last, "reply": ""})
        assert r.status_code == 200, f"{sid}: {r.text}"
        d = r.json()
        assert d["final"], f"{sid}: last beat not final"
        assert "THE END" in d["spoken"]
        assert d["moral"] == s["moral"]


def test_every_readalong_story_served():
    r = client.get("/api/stories")
    assert r.status_code == 200
    roster = r.json()["stories"]
    assert len(roster) == len(conversation.STORIES)
    for item in roster:
        d = client.get(f"/api/stories/{item['id']}")
        assert d.status_code == 200
        st = d.json()["story"]
        assert len(st["words"]) >= 8


def test_bad_story_requests_rejected():
    pid = _mk("Guarded", 3)
    assert client.post("/api/story/tell", json={
        "pid": pid, "story": "nope", "beat": 0}).status_code == 404
    sid = next(iter(conversation.INTERACTIVE_STORIES))
    assert client.post("/api/story/tell", json={
        "pid": pid, "story": sid, "beat": 99}).status_code == 422
