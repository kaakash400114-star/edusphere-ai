"""The Practice Engine — replaces the paid Level engine (Stage 1 rework).

Every curriculum topic of the child's grade is freely open — no locks, no
prices, no buying. Finishing a topic still earns POINTS (a simple, honest
number), and every finish is one practice event for the honest improvement
rate (Stage 2).

The topic pool comes from curriculum_feed's section split of the real
knowledge files (same source the old levels used), so nothing is lost —
only the paywall is gone.
"""
from __future__ import annotations

from . import curriculum_feed

POINTS_PER_TOPIC = 10


def grade_topics(grade: int) -> list[dict]:
    """All free practice topics for a grade, ordered by subject then title."""
    topics = []
    for t in curriculum_feed.grade_tasks(grade):
        topics.append({
            "id": t["id"],
            "subject": t["subject"],
            "title": t["title"],
            "prompt": t["prompt"],
            "points": t["points"],
        })
    topics.sort(key=lambda t: (t["subject"], t["title"].lower()))
    return topics


def topic_by_id(grade: int, topic_id: str) -> dict | None:
    tid = str(topic_id)[:80]
    for t in grade_topics(grade):
        if t["id"] == tid:
            return t
    return None


def mark_done(raw: dict, topic: dict) -> dict:
    """Record a finished topic on the raw profile: once, +points, no locks.

    Re-finishing is allowed only after a new day (spaced repeat), and a
    same-day repeat earns no double points (honest counting).
    """
    import time
    done = raw.setdefault("practice_done", {})
    tid = topic["id"]
    today = time.strftime("%Y-%m-%d")
    entry = done.get(tid) or {}
    times = entry.get("times", [])
    first_time = not times
    already_today = bool(times and times[-1][:10] == today)
    if first_time or not already_today:
        raw["points"] = raw.get("points", 0) + POINTS_PER_TOPIC
        times.append(today)
        done[tid] = {"times": times[-20:]}  # keep the last 20 dates
    return {
        "topic": tid,
        "title": topic["title"],
        "first_time": first_time,
        "already_today": already_today,
        "points_awarded": POINTS_PER_TOPIC if (first_time or not already_today) else 0,
        "points": raw.get("points", 0),
    }
