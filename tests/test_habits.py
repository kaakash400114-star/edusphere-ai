"""Stage 6 — habit engine: streak freeze repair + daily quests (offline)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import habits, profiles


def _mk(name="HabitKid", grade=4, stars=50):
    return profiles.create_profile(name, grade, None, board="cbse",
                                   character="leo")["pid"] if False else None


def _mk_profile(name="HabitKid", grade=4, stars=50):
    from app.profiles import _raw, _write_raw
    pid = profiles.create_profile(name, grade, None, board="cbse",
                                  character="leo").get("pid")
    raw = profiles._raw(pid)
    raw["stars"] = stars
    profiles._write_raw(pid, raw)
    return pid


def test_buy_freeze_success_and_max():
    pid = _mk_profile(stars=25)
    r1 = habits.buy_freeze(pid)
    assert r1["ok"] and r1["freezes"] == 1 and r1["stars"] == 15
    r2 = habits.buy_freeze(pid)
    assert r2["ok"] and r2["freezes"] == 2 and r2["stars"] == 5
    r3 = habits.buy_freeze(pid)                     # max 2 held
    assert not r3["ok"] and "already" in r3["reason"]


def test_buy_freeze_insufficient_stars():
    pid = _mk_profile(stars=5)
    r = habits.buy_freeze(pid)
    assert not r["ok"] and "stars" in r["reason"]


def test_freeze_repairs_one_day_gap():
    pid = _mk_profile(stars=50)
    raw = profiles._raw(pid)
    raw["streak"] = {"count": 7, "last_day": "2026-01-01"}
    raw["freezes"] = 1
    profiles._write_raw(pid, raw)
    streak = habits.touch_streak(pid, today="2026-01-03")
    assert streak["count"] == 8                    # repaired, not reset
    raw = profiles._raw(pid)
    assert raw["freezes"] == 0                     # freeze consumed


def test_broken_streak_without_freeze_resets():
    pid = _mk_profile(stars=50)
    raw = profiles._raw(pid)
    raw["streak"] = {"count": 7, "last_day": "2026-01-01"}
    profiles._write_raw(pid, raw)
    streak = habits.touch_streak(pid, today="2026-01-09")
    assert streak["count"] == 1                    # honest restart


def test_contiguous_day_increments():
    pid = _mk_profile(stars=50)
    raw = profiles._raw(pid)
    raw["streak"] = {"count": 3, "last_day": "2026-01-04"}
    profiles._write_raw(pid, raw)
    streak = habits.touch_streak(pid, today="2026-01-05")
    assert streak["count"] == 4


def test_same_day_idempotent():
    pid = _mk_profile(stars=50)
    raw = profiles._raw(pid)
    raw["streak"] = {"count": 3, "last_day": "2026-01-05"}
    profiles._write_raw(pid, raw)
    streak = habits.touch_streak(pid, today="2026-01-05")
    assert streak["count"] == 3                    # not double counted


def test_daily_quests_progress_and_claim():
    pid = _mk_profile(stars=0)
    info = habits.daily_quests(pid, today="2026-02-01")
    assert len(info["quests"]) == 3
    assert all(q["progress"] == 0 for q in info["quests"])
    # simulate a chat event today
    import time as _t
    raw = profiles._raw(pid)
    raw["log"].append({"t": "2026-02-01T10:00:00", "kind": "chat", "topic": "x"})
    profiles._write_raw(pid, raw)
    info = habits.daily_quests(pid, today="2026-02-01")
    learn = [q for q in info["quests"] if q["id"] == "learn"][0]
    assert learn["done"] and not learn["claimed"]
    r = habits.claim_quest(pid, "learn", today="2026-02-01")
    assert r["ok"] and r["reward"] == 2
    again = habits.claim_quest(pid, "learn", today="2026-02-01")
    assert not again["ok"] and "already" in again["reason"]
    notdone = habits.claim_quest(pid, "play", today="2026-02-01")
    assert not notdone["ok"]
