"""Knowledge base loader for EduSphere AI.

Loads curriculum markdown files from knowledge/ and extracts the most
relevant sections for a given grade + subject + question.
"""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

# subject -> filename pattern
FILE_MAP = {
    "math": "mathematics/grade{grade}_math.md",
    "maths": "mathematics/grade{grade}_math.md",
    "mathematics": "mathematics/grade{grade}_math.md",
    "science": "science/grade{grade}_science.md",
    "english": "english/grade{grade}_english.md",
    "grammar": "english/grade{grade}_english.md",
    "social": "general/social_studies.md",
    "social studies": "general/social_studies.md",
    "logic": "general/logical_thinking.md",
    "logical thinking": "general/logical_thinking.md",
    "general": "general/social_studies.md",
    # pre-grade worlds (Sunny Meadow / Rainbow Kindergarten)
    "meadow": "general/meadow_activities.md",
    "kindergarten": "general/kindergarten_activities.md",
}

GRADES_WITH_FILES = {
    "math": set(range(1, 13)) | {"foundation"},
    "science": set(range(1, 8)),
    "english": set(range(1, 7)),
}


def normalize_subject(subject: str) -> str:
    s = (subject or "").strip().lower()
    return s if s in FILE_MAP else "general"


def knowledge_path(subject: str, grade: int | str) -> Path | None:
    """Resolve the knowledge file for a subject+grade, falling back sensibly."""
    subject = normalize_subject(subject)
    pattern = FILE_MAP[subject]
    rel = pattern.format(grade=grade)
    path = KNOWLEDGE_DIR / rel
    if path.exists():
        return path
    # fallback: closest lower grade that exists
    if isinstance(grade, int):
        for g in range(grade - 1, 0, -1):
            cand = KNOWLEDGE_DIR / pattern.format(grade=g)
            if cand.exists():
                return cand
    # last resort: foundation / general file
    for cand in (
        KNOWLEDGE_DIR / "mathematics/arithmetic_foundation.md",
        KNOWLEDGE_DIR / "general/logical_thinking.md",
    ):
        if cand.exists():
            return cand
    return None


@lru_cache(maxsize=64)
def load_file(path_str: str) -> list[tuple[str, str]]:
    """Parse a knowledge file into (section_title, section_text) tuples.

    Sections are split on '## ' headers; content before the first header
    is kept under the file's title.
    """
    path = Path(path_str)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"\n(?=## )", text)
    sections: list[tuple[str, str]] = []
    for part in parts:
        lines = part.strip().splitlines()
        if not lines:
            continue
        title = lines[0].lstrip("# ").strip() or "Overview"
        body = "\n".join(lines[1:]).strip()
        sections.append((title, body if body else part.strip()))
    return sections


def _keywords(question: str) -> list[str]:
    stop = {
        "what", "why", "how", "the", "a", "an", "is", "are", "was", "were",
        "do", "does", "did", "can", "you", "me", "my", "i", "of", "in", "on",
        "for", "to", "and", "or", "it", "this", "that", "with", "explain",
        "tell", "about", "please", "help",
    }
    words = re.findall(r"[a-zA-Z][a-zA-Z\-']+", question.lower())
    return [w for w in words if w not in stop and len(w) > 2]


def extract_relevant(subject: str, grade: int | str, question: str,
                     max_chars: int = 6000) -> str:
    """Return the most question-relevant excerpt of the grade's knowledge file."""
    path = knowledge_path(subject, grade)
    if not path:
        return ""
    sections = load_file(str(path))
    if not sections:
        return ""
    kws = _keywords(question)
    scored: list[tuple[float, int, tuple[str, str]]] = []
    for idx, (title, body) in enumerate(sections):
        hay = (title + " " + body[:800]).lower()
        score = sum(2.0 if w in title.lower() else (0.4 if w in hay else 0.0)
                    for w in kws)
        scored.append((score, -idx, (title, body)))
    scored.sort(reverse=True)
    picked: list[str] = []
    used = 0
    for score, _, (title, body) in scored:
        if score <= 0 and picked:
            continue
        chunk = f"### {title}\n{body[:2600]}"
        if used + len(chunk) > max_chars:
            break
        picked.append(chunk)
        used += len(chunk)
        if len(picked) >= 4:
            break
    header = f"Curriculum reference file: {path.name}\n\n"
    return header + "\n\n---\n\n".join(picked)


def list_available(grade: int | str) -> list[str]:
    """Subjects that have a knowledge file for this grade."""
    out = []
    for subject in ("math", "science", "english", "social", "logic"):
        if knowledge_path(subject, grade):
            out.append(subject)
    return out
