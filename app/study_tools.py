"""EduSphere Study Tools Engine — Flashcards, Notes & Interactive Quizzes.

Bridges the study-helper capabilities directly into the web application,
grounded in curriculum knowledge, spaced repetition (SM-2), and profile rewards.

Storage:
  data/study/{pid}/flashcards.json
  data/study/{pid}/notes.json
  data/study/{pid}/quizzes.json
"""
from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path
from typing import Any

from . import knowledge, llm, profiles, srs

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "study"


def _safe_pid(pid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "", str(pid))[:40]


def _user_study_dir(pid: str) -> Path:
    p = DATA_DIR / _safe_pid(pid)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _read_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return default
    return default


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════════════
# 1. FLASHCARDS (with SM-2 Spaced Repetition)
# ══════════════════════════════════════════════════════════════════════════════

def list_decks(pid: str) -> list[dict]:
    p = _user_study_dir(pid) / "flashcards.json"
    data = _read_json(p, [])
    return data


def get_deck(pid: str, deck_id: str) -> dict | None:
    for deck in list_decks(pid):
        if deck.get("id") == deck_id:
            return deck
    return None


def generate_deck(pid: str, subject: str, topic: str, count: int = 5,
                  difficulty: str = "medium") -> dict:
    profile = profiles.get_profile(pid) or {}
    grade = profile.get("grade", 4)
    subject = subject.strip() or "general"
    topic = topic.strip() or "General Study"
    count = max(1, min(15, int(count or 5)))

    # Fetch curriculum excerpt
    excerpt = knowledge.extract_relevant(subject, grade, topic)
    cards = []

    # Attempt LLM generation if configured
    if llm.is_configured():
        prompt = (
            f"Generate exactly {count} curriculum flashcards for grade {grade} {subject} on topic '{topic}'. "
            f"Difficulty: {difficulty}.\n"
            + (f"CURRICULUM EXCERPT:\n{excerpt[:2000]}\n" if excerpt else "")
            + "Return ONLY a valid JSON array of objects with keys 'question' and 'answer'. "
            "Example: [{\"question\": \"...\", \"answer\": \"...\"}]"
        )
        text, err = llm.quick(prompt, max_tokens=1200, temperature=0.2)
        if text:
            try:
                # Find JSON array
                start = text.find("[")
                end = text.rfind("]")
                if start != -1 and end != -1:
                    parsed = json.loads(text[start:end+1])
                    if isinstance(parsed, list):
                        for i, item in enumerate(parsed[:count]):
                            if "question" in item and "answer" in item:
                                cards.append({
                                    "id": f"card_{i+1:03d}",
                                    "question": str(item["question"]),
                                    "answer": str(item["answer"]),
                                    "reps": 0,
                                    "ef": 2.5,
                                    "interval": 1,
                                    "due": time.time(),
                                    "last_quality": -1,
                                })
            except Exception:
                pass

    # Deterministic fallback when LLM is unavailable or in offline tests
    if not cards:
        sections = knowledge.load_file(str(knowledge.knowledge_path(subject, grade) or ""))
        items = []
        for title, body in sections:
            if title.lower() not in ("overview", "table of contents", "introduction") and body:
                first_sent = body.split(". ")[0].strip() + "."
                items.append((title, first_sent))
        if not items:
            items = [
                (f"What is {topic}?", f"{topic} is an essential concept in {subject}."),
                (f"Key rule of {topic}", f"Understanding {topic} helps solve core problems in {subject}."),
                (f"Application of {topic}", f"{topic} is applied in practical exercises and questions."),
            ]
        for i in range(min(count, max(3, len(items)))):
            t_item, a_item = items[i % len(items)]
            cards.append({
                "id": f"card_{i+1:03d}",
                "question": f"Explain: {t_item}" if not t_item.startswith("What") else t_item,
                "answer": a_item,
                "reps": 0,
                "ef": 2.5,
                "interval": 1,
                "due": time.time(),
                "last_quality": -1,
            })

    deck_id = f"deck_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    deck = {
        "id": deck_id,
        "subject": subject,
        "topic": topic,
        "grade": grade,
        "difficulty": difficulty,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "cards": cards,
    }

    decks = list_decks(pid)
    decks.insert(0, deck)
    _write_json(_user_study_dir(pid) / "flashcards.json", decks[:30])
    return deck


def review_card(pid: str, deck_id: str, card_id: str, quality: int) -> dict:
    """Review card with quality (0=again, 1=hard, 2=good, 3=easy)."""
    quality = max(0, min(5, int(quality)))
    decks = list_decks(pid)
    target_card = None

    for deck in decks:
        if deck.get("id") == deck_id:
            for card in deck.get("cards", []):
                if card.get("id") == card_id:
                    # Update card with SM-2
                    srs_card = {
                        "ef": card.get("ef", 2.5),
                        "interval": card.get("interval", 1),
                        "reps": card.get("reps", 0),
                    }
                    updated = srs._sm2(srs_card, quality)
                    card["ef"] = updated["ef"]
                    card["interval"] = updated["interval"]
                    card["reps"] = updated["reps"]
                    card["due"] = updated["due"]
                    card["last_quality"] = quality
                    card["last_reviewed"] = time.time()
                    target_card = card
                    break

    if target_card:
        _write_json(_user_study_dir(pid) / "flashcards.json", decks)
        # Award stars and points for reviewing
        stars_awarded = 1 if quality >= 3 else 0
        profiles.record_activity(pid, "flashcards", deck_id, stars=stars_awarded)
        raw = profiles._raw(pid)
        if raw:
            raw["points"] = raw.get("points", 0) + (2 if quality >= 3 else 1)
            profiles._write_raw(pid, raw)

    return {"ok": bool(target_card), "card": target_card}


# ══════════════════════════════════════════════════════════════════════════════
# 2. NOTES NOTEBOOK
# ══════════════════════════════════════════════════════════════════════════════

def list_notes(pid: str, subject: str | None = None) -> list[dict]:
    p = _user_study_dir(pid) / "notes.json"
    notes = _read_json(p, [])
    if subject:
        sub = subject.lower().strip()
        return [n for n in notes if n.get("subject", "").lower() == sub]
    return notes


def get_note(pid: str, note_id: str) -> dict | None:
    for n in list_notes(pid):
        if n.get("id") == note_id:
            return n
    return None


def save_note(pid: str, title: str, subject: str, content: str,
              note_id: str | None = None) -> dict:
    notes = list_notes(pid)
    now = time.strftime("%Y-%m-%dT%H:%M:%S")

    if note_id:
        for n in notes:
            if n.get("id") == note_id:
                n["title"] = title.strip()[:100]
                n["subject"] = subject.strip()[:40]
                n["content"] = content.strip()[:20000]
                n["updated_at"] = now
                _write_json(_user_study_dir(pid) / "notes.json", notes)
                return n

    nid = f"note_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    entry = {
        "id": nid,
        "title": (title or "Untitled Note").strip()[:100],
        "subject": (subject or "general").strip()[:40],
        "content": content.strip()[:20000],
        "created_at": now,
        "updated_at": now,
    }
    notes.insert(0, entry)
    _write_json(_user_study_dir(pid) / "notes.json", notes[:100])
    return entry


def delete_note(pid: str, note_id: str) -> bool:
    notes = list_notes(pid)
    rem = [n for n in notes if n.get("id") != note_id]
    if len(rem) < len(notes):
        _write_json(_user_study_dir(pid) / "notes.json", rem)
        return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# 3. INTERACTIVE QUIZ ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def list_quizzes(pid: str) -> list[dict]:
    p = _user_study_dir(pid) / "quizzes.json"
    return _read_json(p, [])


def generate_quiz(pid: str, subject: str, topic: str, count: int = 5,
                  difficulty: str = "medium") -> dict:
    profile = profiles.get_profile(pid) or {}
    grade = profile.get("grade", 4)
    subject = subject.strip() or "general"
    topic = topic.strip() or "General Science"
    count = max(2, min(10, int(count or 5)))

    excerpt = knowledge.extract_relevant(subject, grade, topic)
    questions = []

    if llm.is_configured():
        prompt = (
            f"Generate a {count}-question multiple-choice quiz for grade {grade} {subject} on topic '{topic}'. "
            f"Difficulty: {difficulty}.\n"
            + (f"CURRICULUM EXCERPT:\n{excerpt[:2000]}\n" if excerpt else "")
            + "Format: Return ONLY a valid JSON array of objects. Each object MUST have:\n"
            "- 'id': string (e.g. 'q1')\n"
            "- 'question': clear question string\n"
            "- 'options': list of exactly 4 string options\n"
            "- 'answer': integer index (0, 1, 2, or 3) of the correct option\n"
            "- 'explanation': 1 friendly sentence explaining why this answer is right\n"
        )
        text, err = llm.quick(prompt, max_tokens=1500, temperature=0.2)
        if text:
            try:
                start = text.find("[")
                end = text.rfind("]")
                if start != -1 and end != -1:
                    parsed = json.loads(text[start:end+1])
                    if isinstance(parsed, list):
                        for i, q in enumerate(parsed[:count]):
                            if ("question" in q and isinstance(q.get("options"), list)
                                    and len(q["options"]) == 4 and "answer" in q):
                                questions.append({
                                    "id": f"q_{i+1}",
                                    "question": str(q["question"]),
                                    "options": [str(opt) for opt in q["options"]],
                                    "answer": int(q["answer"]) % 4,
                                    "explanation": str(q.get("explanation", "Great job!")),
                                })
            except Exception:
                pass

    if not questions:
        # Deterministic fallback quiz
        questions = [
            {
                "id": "q_1",
                "question": f"Which statement best describes {topic}?",
                "options": [
                    f"It is a core foundational topic in {subject}.",
                    "It has no connection to school science or math.",
                    "It was invented yesterday.",
                    "It cannot be studied.",
                ],
                "answer": 0,
                "explanation": f"{topic} is an essential part of the {subject} syllabus.",
            },
            {
                "id": "q_2",
                "question": f"Why is studying {topic} important?",
                "options": [
                    "To build problem-solving ability and reasoning.",
                    "To forget previous lessons.",
                    "It has no practical use.",
                    "Only for exams, not understanding.",
                ],
                "answer": 0,
                "explanation": "Studying concepts builds problem-solving skills and long-term retention.",
            },
            {
                "id": "q_3",
                "question": f"When practicing questions on {topic}, what is the best first step?",
                "options": [
                    "Read the question carefully and identify key facts.",
                    "Guess immediately without reading.",
                    "Skip to the end without checking.",
                    "Close the book.",
                ],
                "answer": 0,
                "explanation": "Reading carefully and identifying facts is the best strategy.",
            },
        ]

    quiz_id = f"quiz_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    quiz = {
        "id": quiz_id,
        "subject": subject,
        "topic": topic,
        "grade": grade,
        "difficulty": difficulty,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "questions": questions,
        "submitted": False,
        "score": None,
    }

    quizzes = list_quizzes(pid)
    quizzes.insert(0, quiz)
    _write_json(_user_study_dir(pid) / "quizzes.json", quizzes[:30])
    return quiz


def submit_quiz(pid: str, quiz_id: str, answers: dict[str, int]) -> dict:
    """Submit quiz answers, award stars/points, update streak and return report."""
    quizzes = list_quizzes(pid)
    quiz = None
    for q in quizzes:
        if q.get("id") == quiz_id:
            quiz = q
            break

    if not quiz:
        return {"ok": False, "reason": "quiz not found"}

    correct_count = 0
    total = len(quiz.get("questions", []))
    review_details = []

    for q in quiz.get("questions", []):
        qid = q["id"]
        chosen = int(answers.get(qid, -1))
        expected = int(q["answer"])
        is_correct = (chosen == expected)
        if is_correct:
            correct_count += 1
        review_details.append({
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "chosen": chosen,
            "expected": expected,
            "correct": is_correct,
            "explanation": q.get("explanation", ""),
        })

    pct = round((correct_count / max(1, total)) * 100)
    stars = correct_count + (5 if correct_count == total and total >= 3 else 0)

    quiz["submitted"] = True
    quiz["score"] = pct
    quiz["correct"] = correct_count
    quiz["total"] = total
    quiz["review"] = review_details
    _write_json(_user_study_dir(pid) / "quizzes.json", quizzes)

    # Award progress to student profile
    profiles.log_practice(pid, subject=quiz.get("subject", "general"),
                          correct=correct_count, total=total, source="quiz")
    profiles.record_activity(pid, "quiz:" + quiz.get("topic", "general"),
                             quiz.get("topic", "quiz"), stars=stars)

    # Update weak/strong areas
    raw = profiles._raw(pid)
    if raw:
        topic = quiz.get("topic", "general")
        if pct < 60:
            weak = raw.setdefault("weak_areas", {})
            weak[topic] = weak.get(topic, 0) + 1
        else:
            strong = raw.setdefault("strong_areas", {})
            strong[topic] = strong.get(topic, 0) + 1
            if topic in raw.get("weak_areas", {}):
                raw["weak_areas"].pop(topic, None)
        profiles._write_raw(pid, raw)

    return {
        "ok": True,
        "quiz_id": quiz_id,
        "score": pct,
        "correct": correct_count,
        "total": total,
        "stars_earned": stars,
        "review": review_details,
    }
