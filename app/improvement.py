"""Honest improvement rate (Stage 2 of the rework).

Reads the kid's practice_log (practice topics + arcade game results) and
answers ONE question honestly: how is this child actually doing?

Ratings are EARNED, never gifted:
    Worst / Bad / Fair / Good / Very Good / Amazing
- No practice data -> no rating. Never a fake "Good".
- Trend compares the last 14 days with the 14 before that: improving /
  steady / slipping is stated plainly.
- The VERDICT is identical for every age; only the SENTENCE tone scales
  with grade (gentle for grades 1-3, plain for 4-7, direct for 8-12).
"""
from __future__ import annotations

import time

RATING_BANDS: list[tuple[float, str]] = [
    (0.95, "Amazing"),
    (0.85, "Very Good"),
    (0.65, "Good"),
    (0.45, "Fair"),
    (0.25, "Bad"),
    (0.00, "Worst"),
]

WINDOW_DAYS = 14


def rating_for(accuracy: float) -> str:
    for threshold, name in RATING_BANDS:
        if accuracy >= threshold:
            return name
    return "Worst"


def _split_windows(events: list[dict], now: float | None = None):
    now = now or time.time()
    recent: list[dict] = []
    previous: list[dict] = []
    for e in events:
        try:
            t = time.mktime(time.strptime(e["t"], "%Y-%m-%dT%H:%M:%S"))
        except (KeyError, ValueError):
            continue
        age_days = (now - t) / 86400
        if age_days <= WINDOW_DAYS:
            recent.append(e)
        elif age_days <= WINDOW_DAYS * 2:
            previous.append(e)
    return recent, previous


def _acc(events: list[dict]) -> tuple[float | None, int, int]:
    correct = sum(int(e.get("correct", 0)) for e in events)
    total = sum(int(e.get("total", 0)) for e in events)
    if total <= 0:
        return None, correct, total
    return correct / total, correct, total


def _trend(recent_acc, prev_events: list[dict]):
    """improving / steady / slipping / new — never invented without data."""
    if not prev_events:
        return "new", None
    if recent_acc is None:
        return "idle", None
    prev_acc, _, _ = _acc(prev_events)
    if prev_acc is None:
        return "new", None
    delta = round((recent_acc - prev_acc) * 100)
    if delta >= 5:
        return "improving", delta
    if delta <= -5:
        return "slipping", delta
    return "steady", delta


def _note(rating: str, trend: str, delta, correct: int, total: int,
          grade: int, subject: str = "") -> str:
    """One honest sentence; tone scales with grade, verdict does not."""
    pct = round(correct / total * 100) if total else 0
    if grade <= 3:                                   # gentle
        base = f"You got {correct} of {total} right — that is {rating}!"
        if trend == "slipping":
            return base + " A little tricky lately — I will help you, let's practice!"
        if trend == "improving":
            return base + " You are getting better and better!"
        return base + " Let's keep playing and learn more!"
    if grade <= 7:                                   # plain
        base = f"{pct}% correct this week ({correct}/{total}) — {rating}."
        if trend == "slipping":
            return base + " That is lower than the two weeks before. More practice will fix it."
        if trend == "improving":
            return base + " Better than the two weeks before — nice work."
        if trend == "new":
            return base + " First results — keep practicing to see your trend."
        return base
    # direct (grades 8-12)
    base = f"{pct}% accuracy ({correct}/{total} attempts, last {WINDOW_DAYS} days) — {rating}."
    if trend == "slipping":
        return base + f" Down {abs(delta)} pts vs the previous period. Focus recommended."
    if trend == "improving":
        return base + f" Up {delta} pts vs the previous period."
    if trend == "new":
        return base + " Not enough history for a trend yet."
    return base + " Steady vs the previous period."


def improvement_report(raw: dict, grade: int) -> dict:
    """Public improvement payload for the settings page + parent report."""
    grade = max(1, min(12, int(grade or 1)))
    events = list(raw.get("practice_log", []))

    if not events:
        return {
            "overall": {"rating": None, "trend": "new", "delta": None,
                        "correct": 0, "total": 0,
                        "note": "No practice yet — the honest rating appears "
                                "after the first practice topics or games."},
            "subjects": [],
        }

    recent, previous = _split_windows(events)
    window = recent if recent else events          # stale data still honest
    acc, correct, total = _acc(window)
    trend, delta = _trend(acc, previous)
    rating = rating_for(acc) if acc is not None else None
    confidence = "ok" if len(recent) >= 3 else "low"

    overall = {
        "rating": rating,
        "trend": trend,
        "delta": delta,
        "correct": correct,
        "total": total,
        "events": len(window),
        "confidence": confidence,
        "note": _note(rating or "Fair", trend, delta, correct, total, grade),
    }

    # per subject, weakest first (the useful end of the list)
    subjects: dict[str, list[dict]] = {}
    for e in window:
        subjects.setdefault(e.get("subject", "general"), []).append(e)
    out = []
    for subj, evs in subjects.items():
        s_acc, s_c, s_t = _acc(evs)
        s_trend, s_delta = _trend(s_acc, [e for e in previous
                                          if e.get("subject") == subj])
        s_rating = rating_for(s_acc) if s_acc is not None else None
        out.append({
            "subject": subj,
            "rating": s_rating,
            "trend": s_trend,
            "delta": s_delta,
            "correct": s_c,
            "total": s_t,
            "note": _note(s_rating or "Fair", s_trend, s_delta, s_c, s_t,
                          grade, subj),
        })
    out.sort(key=lambda s: (s["correct"] / s["total"]) if s["total"] else 1)
    return {"overall": overall, "subjects": out}
