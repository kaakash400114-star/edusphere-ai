"""Stage C feed: level task sets generated from the curriculum files.

Each (grade, level) gets a task set derived from the real knowledge files
('## ' sections). Deterministic: section i of the subject spread maps to
level (i % 7) + 1, so every level has 2 tasks (math + science OR english +
second subject) and every curriculum section reaches a level.

Subject spread per grade band:
- grades 1-5: math + science + english -> tasks pair math/science/english
  cycling; each level ends with 3 tasks where material exists.
- grades 6-12: math + science (english added in stage D when files exist).

Public API used by main.py / levels.py:
  task_count(grade, level) -> int
  level_tasks(grade, level) -> [{id, subject, title, prompt, points}]
"""
from __future__ import annotations

from pathlib import Path

from . import knowledge

PRACTICE_SPLIT = 6  # free practice: topics are NOT grouped into levels anymore

ROOT = Path(__file__).resolve().parent.parent

# section count per (subject, grade) discovered from the knowledge files
def _sections(subject: str, grade: int) -> list[str]:
    path = ROOT / "knowledge" / subject / f"grade{grade}_{subject}.md"
    if subject == "math":  # mathematics dir
        path = ROOT / "knowledge" / "mathematics" / f"grade{grade}_math.md"
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    out = []
    for line in text.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            if not title or title.startswith("#"):
                continue
            # skip navigational sections that make poor tasks
            if title.lower() in ("table of contents", "contents", "introduction",
                                 "conclusion", "summary", "index"):
                continue
            out.append(title)
    if len(out) < PRACTICE_SPLIT:
        # thin file: fall back to ### subsections so every grade still gets
        # a full task pool (grades 3-5 English store topics as ### headings)
        out = []
        for line in text.splitlines():
            if line.startswith("### "):
                title = line[4:].strip()
                if not title or title.startswith("#"):
                    continue
                if title.lower() in ("table of contents", "contents", "introduction",
                                     "conclusion", "summary", "index"):
                    continue
                if len(out) < 21:      # cap: 3 topics per level at most
                    out.append(title)
    return out


_SUBJECTS_BY_GRADE = {
    **{g: ["math", "science", "english"] for g in range(1, 13)},
}

PROMPTS = {
    "math": "Teach me {topic} with a small example, then quiz me on it!",
    "science": "Explain {topic} simply, then ask me two check questions!",
    "english": "Help me practice {topic}, then give me a mini exercise!",
}


def _subject_file_name(subject: str, grade: int) -> str:
    return {"math": "mathematics", "science": "science", "english": "english"}[subject]


def _grade_tasks(grade: int) -> list[dict]:
    """All free practice topics for a grade: one per curriculum section."""
    subs = _SUBJECTS_BY_GRADE.get(grade, ["math"])
    streams = []
    for s in subs:
        for i, title in enumerate(_sections(s, grade)):
            streams.append({
                "subject": s,
                "title": title,
                "file": _subject_file_name(s, grade),
            })
    if not streams:
        return []
    # deterministic order: round-robin subjects so the list gets variety
    streams.sort(key=lambda t: (t["subject"], ))
    tasks = []
    for idx, t in enumerate(streams):
        s = t["subject"]
        tasks.append({
            "id": f"{s}_{idx}_{t['file']}",
            "grade": grade,
            "subject": s,
            "title": t["title"][:80],
            "prompt": PROMPTS[s].format(topic=t["title"].lower())[:160],
            "points": 10,
            "mode": "chat",   # chat-based topic: buddy teaches + quizzes
        })
    return tasks


_CACHE: dict[int, list[dict]] = {}

def grade_tasks(grade: int) -> list[dict]:
    g = max(1, min(12, int(grade or 1)))
    if g not in _CACHE:
        _CACHE[g] = _grade_tasks(g)
    return _CACHE[g]


def kinder_grade() -> bool:
    """Grade 0 (KG) has no curriculum files — kinder corner serves it."""
    return True


def topic_by_id(grade: int, task_id: str) -> dict | None:
    for t in grade_tasks(grade):
        if t["id"] == task_id:
            return t
    return None
