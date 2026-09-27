"""Habit engine (Stage 6) — Duolingo's retention mechanics, kid-honest.

Streak freeze:
  - a child with >= 10 stars may buy a freeze (costs 10 stars, max 2 held)
  - on the first activity of a new day, if yesterday had NO activity and a
    freeze is held, the freeze is consumed and the streak survives
  - the consumption happens lazily inside touch_streak() so no cron is needed

Daily quests:
  - three fixed quests a day (learn/chat, practice, play a game), progress
    read from the activity log, +2 stars each on completion
  - quests are computed from data — nothing to schedule, nothing to fake

All offline-testable; time is injectable via _today().
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import profiles

FREEZE_COST = 10
FREEZE_MAX = 2
QUEST_STAR_REWARD = 2

QUESTS = [
    {"id": "learn", "emoji": "💬", "label": "Talk & learn something new",
     "goal": 1, "kinds": {"chat"}},
    {"id": "practice", "emoji": "🧭", "label": "Finish a practice topic",
     "goal": 1, "kinds": {"practice"}},
    {"id": "play", "emoji": "🎮", "label": "Play one learning game",
     "goal": 1, "kinds": {"game", "kinder"}},
]


def _today() -> str:
    return time.strftime("%Y-%m-%d")


def _yesterday(today: str | None = None) -> str:
    ref = today or _today()
    try:
        t = time.mktime(time.strptime(ref, "%Y-%m-%d")) - 86400
        return time.strftime("%Y-%m-%d", time.localtime(t))
    except ValueError:
        return ref


def buy_freeze(pid: str) -> dict:
    """Spend stars to hold one streak freeze (max FREEZE_MAX)."""
    raw = profiles._raw(pid)
    if raw is None:
        return {"ok": False, "reason": "profile not found"}
    held = raw.get("freezes", 0)
    if held >= FREEZE_MAX:
        return {"ok": False, "reason": f"You already hold {FREEZE_MAX} freezes!"}
    stars = raw.get("stars", 0)
    if stars < FREEZE_COST:
        return {"ok": False,
                "reason": f"A freeze costs {FREEZE_COST} stars — you have {stars}. "
                          "Learn something today and you will get there!"}
    raw["stars"] = stars - FREEZE_COST
    raw["freezes"] = held + 1
    profiles._write_raw(pid, raw)
    return {"ok": True, "stars": raw["stars"], "freezes": raw["freezes"]}


def touch_streak(pid: str, today: str | None = None) -> dict:
    """First activity of the day: repair the streak with a held freeze
    when yesterday was missed. Returns the (possibly updated) streak."""
    today = today or _today()
    raw = profiles._raw(pid)
    if raw is None:
        return {"count": 0, "last_day": ""}
    streak = raw.get("streak", {"count": 0, "last_day": ""})
    if streak.get("last_day") == today:
        return streak                       # already counted today
    yesterday = _yesterday(today)
    if streak.get("last_day") != yesterday:
        freezes = raw.get("freezes", 0)
        gap_ok = streak.get("last_day", "") and freezes > 0
        if gap_ok:
            # does the freeze bridge the exact gap? (last_day < yesterday)
            try:
                t_last = time.mktime(time.strptime(streak["last_day"], "%Y-%m-%d"))
                t_yest = time.mktime(time.strptime(yesterday, "%Y-%m-%d"))
                t_today = time.mktime(time.strptime(today, "%Y-%m-%d"))
                missed = int((t_yest - t_last) / 86400)
            except (ValueError, KeyError):
                missed = 99
            if 0 < missed <= freezes:
                raw["freezes"] = freezes - missed
                streak["count"] = streak.get("count", 0) + 1
                streak["last_day"] = today
                raw["streak"] = streak
                profiles._write_raw(pid, raw)
                return streak
        streak["count"] = 1                  # streak broken — restart honestly
        streak["last_day"] = today
        raw["streak"] = streak
        profiles._write_raw(pid, raw)
        return streak
    # contiguous day: normal increment (matches record_activity behaviour)
    streak["count"] = streak.get("count", 0) + 1
    streak["last_day"] = today
    raw["streak"] = streak
    profiles._write_raw(pid, raw)
    return streak


def daily_quests(pid: str, today: str | None = None) -> dict:
    """Compute today's quest progress from the activity log."""
    today = today or _today()
    raw = profiles._raw(pid)
    if raw is None:
        return {"quests": [], "date": today}
    todays = [e for e in raw.get("log", [])
              if (e.get("t") or "").startswith(today)]
    claimed_today = set(raw.get("quests_claimed", {}).get(today, []))
    out = []
    for q in QUESTS:
        done = sum(1 for e in todays if e.get("kind") in q["kinds"])
        out.append({
            "id": q["id"], "emoji": q["emoji"], "label": q["label"],
            "goal": q["goal"], "progress": min(done, q["goal"]),
            "done": done >= q["goal"],
            "claimed": q["id"] in claimed_today,
            "stars": QUEST_STAR_REWARD,
        })
    return {"quests": out, "date": today,
            "streak": raw.get("streak", {}),
            "freezes": raw.get("freezes", 0),
            "stars": raw.get("stars", 0)}


def claim_quest(pid: str, quest_id: str, today: str | None = None) -> dict:
    """Claim the reward for a completed-but-unclaimed quest."""
    today = today or _today()
    info = daily_quests(pid, today)
    for q in info["quests"]:
        if q["id"] == quest_id:
            break
    else:
        return {"ok": False, "reason": "no such quest"}
    if not q["done"]:
        return {"ok": False, "reason": "not finished yet — you can do it!"}
    if q["claimed"]:
        return {"ok": False, "reason": "already claimed today"}
    raw = profiles._raw(pid)
    claimed = raw.setdefault("quests_claimed", {})
    claimed[today] = claimed.get(today, []) + [quest_id]
    claimed[today] = list(set(claimed[today]))
    # trim old days
    for d in list(claimed):
        if d < _yesterday(today):
            claimed.pop(d)
    raw["stars"] = raw.get("stars", 0) + QUEST_STAR_REWARD
    profiles._write_raw(pid, raw)
    return {"ok": True, "stars": raw["stars"],
            "quest": quest_id, "reward": QUEST_STAR_REWARD}
