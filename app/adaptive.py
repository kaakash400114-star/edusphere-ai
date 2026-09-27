"""Adaptive practice (Prodigy/IXL layer) — the RIGHT next topic, per kid.

Ranking signal mix (all from data already on the profile):
  1. DUE REVIEWS  — SRS topics whose next-review date arrived (SM-2 cards).
                    Reviewing at the edge of forgetting is the single
                    highest-yield study act (Spaced repetition).
  2. WEAK SPOTS   — topics the child answered wrongly before (weak_areas),
                    gently retried with encouragement.
  3. FRESH TOPICS — curriculum sections never attempted, in syllabus order,
                    skipping the ones far above/below the grade.

Every pick carries a kid-facing reason string. Pure + offline-testable:
  smart_topics(raw, grade, limit) -> [{topic, reason, priority}]
"""
from __future__ import annotations

import time

from . import curriculum_feed, practice, srs

LIMIT_DEFAULT = 6


def _today() -> str:
    return time.strftime("%Y-%m-%d")


def _due_cards(raw: dict) -> list[dict]:
    try:
        return srs.due_topics(raw) or []
    except Exception:
        return []


def smart_topics(raw: dict, grade: int, limit: int = LIMIT_DEFAULT) -> list[dict]:
    """Ranked next-best practice topics with kid-facing reasons."""
    grade = max(1, min(12, int(grade or 1)))
    limit = max(1, min(12, int(limit or LIMIT_DEFAULT)))
    pool = {t["id"]: t for t in practice.grade_topics(grade)}
    picks: list[dict] = []
    used_ids: set[str] = set()

    # 1) SRS reviews first (edge-of-forgetting)
    for card in _due_cards(raw):
        tid = card.get("topic_id") or card.get("id") or ""
        t = pool.get(tid)
        if not t or tid in used_ids:
            continue
        picks.append({"topic": t, "priority": 0,
                      "reason": "Review time — remember this one?"})
        used_ids.add(tid)
        if len(picks) >= limit:
            return picks

    # 2) weak spots (wrongly answered before)
    weak = raw.get("weak_areas") or {}
    ranked_weak = sorted(weak.items(), key=lambda kv: -kv[1])
    for topic_title, _count in ranked_weak:
        title_l = str(topic_title).lower()[:40]
        match = next((t for tid, t in pool.items()
                      if tid not in used_ids and
                      title_l[:18] in t["title"].lower()), None)
        if match:
            picks.append({"topic": match, "priority": 1,
                          "reason": "This one tricked you before — beat it now!"})
            used_ids.add(match["id"])
            if len(picks) >= limit:
                return picks

    # 3) fresh topics in syllabus order (skip done-today for honesty)
    done = raw.get("practice_done") or {}
    today = _today()
    for tid, t in pool.items():
        if tid in used_ids:
            continue
        times = (done.get(tid) or {}).get("times") or []
        fresh = not times
        if fresh:
            picks.append({"topic": t, "priority": 2,
                          "reason": "Brand new — let's explore it!"})
            used_ids.add(tid)
            if len(picks) >= limit:
                return picks

    # 4) fill with spaced repeats (done before, not today)
    for tid, t in pool.items():
        if len(picks) >= limit:
            break
        if tid in used_ids:
            continue
        times = (done.get(tid) or {}).get("times") or []
        if times and times[-1][:10] != today:
            picks.append({"topic": t, "priority": 3,
                          "reason": "Practice makes perfect!"})
            used_ids.add(tid)
    return picks[:limit]
