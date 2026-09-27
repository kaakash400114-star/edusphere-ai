"""Adaptive practice ranking (app/adaptive.py) — offline tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import adaptive, srs


def _raw() -> dict:
    return {"weak_areas": {}, "practice_done": {}, "srs_cards": {},
            "log": [], "topics_covered": []}


def test_fresh_topics_first_for_new_kid():
    picks = adaptive.smart_topics(_raw(), 4, limit=5)
    assert 0 < len(picks) <= 5
    assert all(p["priority"] == 2 for p in picks)
    assert all("new" in p["reason"].lower() for p in picks)


def test_srs_due_beats_everything():
    raw = _raw()
    pool = adaptive.practice.grade_topics(4)
    target = pool[0]["id"]
    card = {"topic_id": target, "title": pool[0]["title"],
            "subject": "math", "ease": 2.5, "interval": 1,
            "due": 1.0, "reps": 1}          # epoch seconds, long past
    raw["srs_cards"] = {target: card}
    picks = adaptive.smart_topics(raw, 4, limit=3)
    assert picks[0]["priority"] == 0
    assert picks[0]["topic"]["id"] == target
    assert "review" in picks[0]["reason"].lower()


def test_weak_spot_ranked_second():
    raw = _raw()
    pool = adaptive.practice.grade_topics(4)
    # find a topic whose title we can echo into weak_areas
    t = pool[5]
    raw["weak_areas"] = {t["title"]: 2}
    picks = adaptive.smart_topics(raw, 4, limit=2)
    assert any(p["priority"] == 1 for p in picks)
    assert any("tricked" in p["reason"].lower() for p in picks)


def test_limit_respected():
    raw = _raw()
    assert len(adaptive.smart_topics(raw, 6, limit=3)) == 3
    assert len(adaptive.smart_topics(raw, 6, limit=12)) <= 12


def test_grade_clamped():
    raw = _raw()
    picks = adaptive.smart_topics(raw, 99, limit=2)   # clamp to 12
    assert len(picks) == 2
    assert all(p["topic"]["id"].startswith(("math", "science", "english"))
               for p in picks)


def test_reasons_always_present():
    raw = _raw()
    for p in adaptive.smart_topics(raw, 3, limit=6):
        assert isinstance(p["reason"], str) and p["reason"]
