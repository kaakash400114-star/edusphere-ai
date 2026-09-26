"""Spaced Repetition System (SRS) for EduSphere AI.

Based on the SM-2 algorithm (SuperMemo 2) — the gold standard used by
Anki, Duolingo, and every serious learning system.

How it works:
  - Each topic a child has practiced gets a card entry.
  - After every practice event, update the card with quality (0-5):
      5 = perfect recall  4 = correct with hesitation
      3 = correct but hard  2 = incorrect but seemed easy
      1 = incorrect  0 = total blank
  - The SM-2 algorithm computes the next review date.
  - Topics due for review are returned by `due_topics(pid)`.
  - The tutor automatically mentions one due topic at the end of sessions.

Storage: profile raw dict, key "srs_cards" → {topic_id: card}.
"""
from __future__ import annotations

import time
from pathlib import Path

# ── SM-2 algorithm ─────────────────────────────────────────────────────────────

def _sm2(card: dict, quality: int) -> dict:
    """Update a card using the SM-2 algorithm.

    quality: 0-5 (0=blackout, 5=perfect)
    Returns updated card dict.
    """
    quality = max(0, min(5, int(quality)))
    ef = card.get("ef", 2.5)          # easiness factor
    interval = card.get("interval", 1)
    reps = card.get("reps", 0)

    if quality >= 3:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1
    else:
        # Wrong answer: reset to start
        reps = 0
        interval = 1

    # Update easiness factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)

    now = time.time()
    return {
        **card,
        "ef": round(ef, 3),
        "interval": interval,
        "reps": reps,
        "last_quality": quality,
        "last_reviewed": now,
        "due": now + interval * 86400,   # seconds
    }


def _new_card(topic_id: str, topic_label: str, subject: str) -> dict:
    now = time.time()
    return {
        "topic_id": topic_id,
        "label": topic_label,
        "subject": subject,
        "ef": 2.5,
        "interval": 1,
        "reps": 0,
        "last_quality": -1,
        "last_reviewed": 0,
        "due": now,                      # due immediately for first review
        "created": now,
    }


# ── Public API ────────────────────────────────────────────────────────────────

def update_card(raw: dict, topic_id: str, topic_label: str,
                subject: str, quality: int) -> dict:
    """Record a practice event. raw is the profile JSON dict (mutated in-place).
    quality: 0-5 (use 4 for correct answers, 1 for wrong ones).
    Returns the updated card.
    """
    cards = raw.setdefault("srs_cards", {})
    card = cards.get(topic_id) or _new_card(topic_id, topic_label, subject)
    updated = _sm2(card, quality)
    cards[topic_id] = updated
    return updated


def due_topics(raw: dict, limit: int = 5) -> list[dict]:
    """Return topics that are due for review right now, sorted by overdue-ness.

    Returns at most `limit` topics, oldest-due first.
    """
    now = time.time()
    cards = raw.get("srs_cards", {})
    due = [c for c in cards.values() if c.get("due", 0) <= now]
    due.sort(key=lambda c: c.get("due", 0))
    return due[:limit]


def upcoming_topics(raw: dict, hours: int = 24, limit: int = 5) -> list[dict]:
    """Topics coming due within the next `hours` hours."""
    now = time.time()
    cutoff = now + hours * 3600
    cards = raw.get("srs_cards", {})
    upcoming = [c for c in cards.values()
                if now < c.get("due", 0) <= cutoff]
    upcoming.sort(key=lambda c: c.get("due", 0))
    return upcoming[:limit]


def srs_summary(raw: dict) -> dict:
    """Summary for the parent report / settings page."""
    cards = raw.get("srs_cards", {})
    now = time.time()
    due_count = sum(1 for c in cards.values() if c.get("due", 0) <= now)
    mastered = sum(1 for c in cards.values() if c.get("reps", 0) >= 5)
    return {
        "total_cards": len(cards),
        "due_now": due_count,
        "mastered": mastered,
        "learning": len(cards) - mastered,
    }


def quality_from_accuracy(correct: int, total: int) -> int:
    """Convert a correct/total ratio to SM-2 quality (0-5)."""
    if total <= 0:
        return 0
    ratio = correct / total
    if ratio >= 0.95:
        return 5
    if ratio >= 0.85:
        return 4
    if ratio >= 0.65:
        return 3
    if ratio >= 0.45:
        return 2
    if ratio >= 0.25:
        return 1
    return 0
