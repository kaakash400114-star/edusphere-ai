#!/usr/bin/env python3
"""
EduSphere AI — Study Helper Script
Manages flashcards, quizzes, notes, and student progress tracking.

Usage:
    python study_helper.py flashcards --subject <subject> --topic <topic> [--source <file_or_text>] [--count 10]
    python study_helper.py quiz --subject <subject> --topic <topic> [--count 5] [--difficulty easy|medium|hard]
    python study_helper.py progress --add-topic <topic> --score <0-100> --notes <notes>
    python study_helper.py profile [--subject <subject>]
    python study_helper.py notes --subject <subject> --topic <topic> --content <markdown_content>
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Resolve workspace root
# Script is at: <workspace>/skills/study-helper/scripts/study_helper.py
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FLASHCARDS_DIR = WORKSPACE / "flashcards"
QUIZZES_DIR = WORKSPACE / "quizzes"
NOTES_DIR = WORKSPACE / "notes"
PROFILE_DIR = WORKSPACE / "profile"

STUDENT_FILE = PROFILE_DIR / "student.json"
TOPICS_FILE = PROFILE_DIR / "topics_covered.json"
WEAK_AREAS_FILE = PROFILE_DIR / "weak_areas.json"
STRENGTHS_FILE = PROFILE_DIR / "strengths.json"


def ensure_dirs():
    """Create all required directories if they don't exist."""
    for d in [FLASHCARDS_DIR, QUIZZES_DIR, NOTES_DIR, PROFILE_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default=None):
    """Read JSON file, return default if missing."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def write_json(path: Path, data):
    """Write data to JSON file."""
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# FLASHCARDS
# ─────────────────────────────────────────────

def cmd_flashcards(args):
    """Generate a flashcard deck from a topic or file."""
    ensure_dirs()
    subject_dir = FLASHCARDS_DIR / args.subject.lower().replace(" ", "_")
    subject_dir.mkdir(parents=True, exist_ok=True)

    deck_id = f"{args.topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    deck_file = subject_dir / f"{deck_id}.json"

    # If source is a file, read it
    source_text = ""
    if args.source:
        source_path = Path(args.source)
        if source_path.exists():
            source_text = source_path.read_text(encoding="utf-8")
        else:
            source_text = args.source

    # Create flashcard template deck
    # In production, the AI agent fills in the actual Q&A content.
    # This creates the structure and prompt guidance.
    flashcards = []
    for i in range(args.count):
        flashcards.append({
            "id": f"card_{i+1:03d}",
            "question": f"[AI-GENERATED] Question {i+1} about '{args.topic}' — fill via agent",
            "answer": f"[AI-GENERATED] Answer {i+1} — fill via agent",
            "difficulty": args.difficulty,
            "retrieved_count": 0,
            "correct_count": 0,
            "last_reviewed": None,
        })

    deck = {
        "id": deck_id,
        "subject": args.subject,
        "topic": args.topic,
        "created": datetime.now().isoformat(),
        "card_count": len(flashcards),
        "source_file": str(Path(args.source).resolve()) if args.source and Path(args.source).exists() else None,
        "flashcards": flashcards,
    }

    write_json(deck_file, deck)
    print(json.dumps({
        "status": "success",
        "action": "flashcards_generated",
        "deck_id": deck_id,
        "subject": args.subject,
        "topic": args.topic,
        "card_count": len(flashcards),
        "file": str(deck_file),
        "hint": "The agent should now populate the flashcard Q&A fields using the study-helper skill."
    }, indent=2))


# ─────────────────────────────────────────────
# QUIZ
# ─────────────────────────────────────────────

def cmd_quiz(args):
    """Record or generate quiz results."""
    ensure_dirs()
    subject_dir = QUIZZES_DIR / args.subject.lower().replace(" ", "_")
    subject_dir.mkdir(parents=True, exist_ok=True)

    result_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = subject_dir / f"quiz_{result_id}.json"

    result = {
        "id": result_id,
        "subject": args.subject,
        "topic": args.topic,
        "difficulty": args.difficulty,
        "question_count": args.count,
        "timestamp": datetime.now().isoformat(),
        "score": None,       # Agent fills this in after running the quiz
        "correct": 0,
        "incorrect": 0,
        "questions": [],      # Agent fills in question details
        "answers": [],        # Agent records student answers
        "explanations": [],   # Agent provides explanations for wrong answers
    }

    write_json(result_file, result)
    print(json.dumps({
        "status": "success",
        "action": "quiz_session_created",
        "quiz_id": result_id,
        "subject": args.subject,
        "topic": args.topic,
        "difficulty": args.difficulty,
        "hint": "Agent should generate questions, run the quiz interactively, then update this file with results."
    }, indent=2))


# ─────────────────────────────────────────────
# PROGRESS TRACKING
# ─────────────────────────────────────────────

def cmd_progress(args):
    """Update student learning profile with session results."""
    ensure_dirs()
    now = datetime.now().isoformat()

    # Update topics covered
    topics = read_json(TOPICS_FILE, [])
    entry = {
        "topic": args.add_topic,
        "score": args.score,
        "notes": args.notes,
        "timestamp": now,
    }
    topics.append(entry)
    write_json(TOPICS_FILE, topics)

    # Update weak areas (score < 60)
    weak_areas = read_json(WEAK_AREAS_FILE, {})
    if args.score < 60:
        weak_areas[args.add_topic] = {
            "last_score": args.score,
            "attempts": weak_areas.get(args.add_topic, {}).get("attempts", 0) + 1,
            "last_attempt": now,
        }
        write_json(WEAK_AREAS_FILE, weak_areas)
    elif args.add_topic in weak_areas:
        # Student mastered a weak area — remove it
        del weak_areas[args.add_topic]
        write_json(WEAK_AREAS_FILE, weak_areas)

    # Update strengths (score >= 80)
    strengths = read_json(STRENGTHS_FILE, {})
    if args.score >= 80:
        strengths[args.add_topic] = {
            "best_score": args.score,
            "last_attempt": now,
        }
        write_json(STRENGTHS_FILE, strengths)

    print(json.dumps({
        "status": "success",
        "action": "progress_updated",
        "topic": args.add_topic,
        "score": args.score,
        "total_topics_covered": len(topics),
        "current_weak_areas": list(weak_areas.keys()),
        "current_strengths": list(strengths.keys()),
    }, indent=2))


# ─────────────────────────────────────────────
# STUDENT PROFILE
# ─────────────────────────────────────────────

def cmd_profile(args):
    """View the current student profile."""
    student = read_json(STUDENT_FILE, {})
    topics = read_json(TOPICS_FILE, [])
    weak = read_json(WEAK_AREAS_FILE, {})
    strengths = read_json(STRENGTHS_FILE, {})

    # Filter by subject if specified
    if args.subject:
        topics = [t for t in topics if t.get("subject", "").lower() == args.subject.lower()]
        weak = {k: v for k, v in weak.items() if args.subject.lower() in k.lower()}
        strengths = {k: v for k, v in strengths.items() if args.subject.lower() in k.lower()}

    # Calculate stats
    scores = [t["score"] for t in topics if t.get("score") is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    total_sessions = len(topics)

    # Sort weak areas by attempts (most struggled = first)
    weak_sorted = sorted(weak.items(), key=lambda x: x[1].get("attempts", 0), reverse=True)

    profile = {
        "student": student,
        "statistics": {
            "total_sessions": total_sessions,
            "average_score": round(avg_score, 1),
            "topics_covered": len(set(t["topic"] for t in topics)),
        },
        "strengths": strengths,
        "weak_areas": weak_sorted,
        "recommended_review": [k for k, v in weak_sorted[:3]],  # Top 3 weak areas
        "recent_topics": [t["topic"] for t in topics[-5:]],       # Last 5 topics
    }

    print(json.dumps(profile, indent=2, ensure_ascii=False))


# ─────────────────────────────────────────────
# NOTES
# ─────────────────────────────────────────────

def cmd_notes(args):
    """Create or append structured study notes."""
    ensure_dirs()
    subject_dir = NOTES_DIR / args.subject.lower().replace(" ", "_")
    subject_dir.mkdir(parents=True, exist_ok=True)

    topic_file = subject_dir / f"{args.topic.lower().replace(' ', '_')}.md"

    note = {
        "metadata": {
            "subject": args.subject,
            "topic": args.topic,
            "created": datetime.now().isoformat(),
        },
        "content": args.content,
    }

    # Write as markdown with frontmatter
    header = f"""---
subject: {args.subject}
topic: {args.topic}
created: {datetime.now().isoformat()}
---

# {args.subject} — {args.topic}

{args.content}
"""
    topic_file.write_text(header, encoding="utf-8")

    print(json.dumps({
        "status": "success",
        "action": "notes_saved",
        "subject": args.subject,
        "topic": args.topic,
        "file": str(topic_file),
    }, indent=2))


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="EduSphere AI Study Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # flashcards
    p_fc = subparsers.add_parser("flashcards", help="Generate flashcard deck")
    p_fc.add_argument("--subject", required=True, help="Subject name")
    p_fc.add_argument("--topic", required=True, help="Topic name")
    p_fc.add_argument("--source", default=None, help="Source file or text")
    p_fc.add_argument("--count", type=int, default=10, help="Number of cards")
    p_fc.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"])

    # quiz
    p_qz = subparsers.add_parser("quiz", help="Create quiz session")
    p_qz.add_argument("--subject", required=True, help="Subject name")
    p_qz.add_argument("--topic", required=True, help="Topic name")
    p_qz.add_argument("--count", type=int, default=5, help="Number of questions")
    p_qz.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"])

    # progress
    p_pg = subparsers.add_parser("progress", help="Update progress tracking")
    p_pg.add_argument("--add-topic", required=True, help="Topic studied")
    p_pg.add_argument("--score", type=int, required=True, help="Score 0-100")
    p_pg.add_argument("--notes", default="", help="Session notes")

    # profile
    p_pf = subparsers.add_parser("profile", help="View student profile")
    p_pf.add_argument("--subject", default=None, help="Filter by subject")

    # notes
    p_nt = subparsers.add_parser("notes", help="Create study notes")
    p_nt.add_argument("--subject", required=True, help="Subject name")
    p_nt.add_argument("--topic", required=True, help="Topic name")
    p_nt.add_argument("--content", required=True, help="Markdown content")

    args = parser.parse_args()

    if args.command == "flashcards":
        cmd_flashcards(args)
    elif args.command == "quiz":
        cmd_quiz(args)
    elif args.command == "progress":
        cmd_progress(args)
    elif args.command == "profile":
        cmd_profile(args)
    elif args.command == "notes":
        cmd_notes(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
