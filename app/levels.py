"""The Level Engine — Stage B of the final spec.

Seven levels per grade, grades 1-12. Level 1 is free; every next level is
bought with points earned from tasks. Each level has a name, a set of tasks
(curriculum-fed in stage C), and a completion reward.

Points economy (one currency: points; stars remain the wardrobe currency):
- Task completed            -> score points (defined per task)
- Level completed (all tasks)-> level bonus points
- Next level price          -> 30 + 15 * (level-1)  => L2:45 .. L7:120
Progress is per (grade, level) and stored on the kid profile.
"""
from __future__ import annotations

LEVELS_PER_GRADE = 7

# Price in points to UNLOCK level n (n = 2..7). Level 1 is free.
def level_price(level: int) -> int:
    if level <= 1:
        return 0
    return 30 + 15 * (level - 1)


# Points awarded for completing a level's full task set.
LEVEL_BONUS = 20

LEVEL_NAMES = [
    "First Steps",      # 1
    "Trailblazer",      # 2
    "Pathfinder",       # 3
    "High Climber",     # 4
    "Star Chaser",      # 5
    "Champion",         # 6
    "Legend",           # 7
]


def level_theme(grade: int, level: int) -> dict:
    """Name + description for one level of one grade."""
    level = max(1, min(LEVELS_PER_GRADE, int(level)))
    return {
        "level": level,
        "name": LEVEL_NAMES[level - 1],
        "price": level_price(level),
        "bonus": LEVEL_BONUS,
    }


def level_map(grade: int) -> list[dict]:
    """The 7 levels of a grade, with locked/unlocked state shape (no kid)."""
    grade = max(1, min(12, int(grade or 1)))
    return [level_theme(grade, n) for n in range(1, LEVELS_PER_GRADE + 1)]


# ---- kid-side state helpers (operate on the raw profile dict) ----

def _levels_state(raw: dict, grade: int) -> dict:
    """{level(str): {'unlocked': bool, 'tasks_done': [id], 'completed': bool}}"""
    key = f"grade_{int(grade)}"
    state = raw.setdefault("levels", {})
    entry = state.setdefault(key, {})
    if "1" not in entry:
        entry["1"] = {"unlocked": True, "tasks_done": [], "completed": False}
    return entry


def view_levels(raw: dict, grade: int) -> dict:
    """Full level map with this kid's progress (public view for frontend)."""
    grade = max(1, min(12, int(grade or 1)))
    entry = _levels_state(raw, grade)
    out = []
    for n in range(1, LEVELS_PER_GRADE + 1):
        theme = level_theme(grade, n)
        st = entry.get(str(n), {})
        out.append({
            **theme,
            "grade": grade,
            "unlocked": bool(st.get("unlocked", n == 1)),
            "completed": bool(st.get("completed", False)),
            "tasks_done": list(st.get("tasks_done", [])),
        })
    return {"grade": grade, "points": raw.get("points", 0), "levels": out}


def unlock_level(raw: dict, grade: int, level: int) -> tuple[dict, bool]:
    """Buy the next level with points.

    Returns (new_state_dict, ok). Rules:
    - level must be exactly one above the highest unlocked/completed one
    - costs level_price(level) points; level 1 is always free/unlocked
    """
    grade = max(1, min(12, int(grade)))
    level = int(level)
    entry = _levels_state(raw, grade)
    prev = entry.get(str(level - 1), {}) if level > 1 else {"completed": True}
    if level < 1 or level > LEVELS_PER_GRADE:
        return {"error": "bad level"}, False
    if level == 1:
        return {"error": "level 1 is always unlocked"}, False
    cur = entry.setdefault(str(level), {"unlocked": False, "tasks_done": [], "completed": False})
    if cur.get("unlocked"):
        return {"error": "already unlocked"}, False
    if not prev.get("unlocked") and not prev.get("completed"):
        return {"error": "previous level is locked"}, False
    price = level_price(level)
    if raw.get("points", 0) < price:
        return {"error": "not enough points"}, False
    raw["points"] = raw.get("points", 0) - price
    cur["unlocked"] = True
    return {"level": level, "spent": price}, True


def complete_task(raw: dict, grade: int, level: int, task_id: str,
                  score: int) -> tuple[dict, bool, str]:
    """Record one task done inside a level; award its score as points.

    Finishing the last task of the level completes it and pays the bonus.
    Returns (payload, ok, message).
    """
    grade = max(1, min(12, int(grade)))
    level = int(level)
    entry = _levels_state(raw, grade)
    st = entry.setdefault(str(level), {"unlocked": False, "tasks_done": [], "completed": False})
    if not st.get("unlocked"):
        return {"error": "level is locked"}, False, "That level is still locked."
    if st.get("completed"):
        return {"error": "level already completed"}, False, "Level already completed."
    task_id = str(task_id)[:60]
    score = max(0, min(200, int(score)))
    if task_id in st["tasks_done"]:
        return {"error": "task already done"}, False, "Task already done."
    st["tasks_done"].append(task_id)
    raw["points"] = raw.get("points", 0) + score
    msg = f"Task complete! +{score} points."
    from . import curriculum_feed  # task set size comes from the feed
    total = curriculum_feed.task_count(grade, level)
    if total and len(st["tasks_done"]) >= total:
        st["completed"] = True
        raw["points"] = raw.get("points", 0) + LEVEL_BONUS
        msg = f"LEVEL COMPLETE! +{score} points, +{LEVEL_BONUS} bonus."
    return {"level": level, "task": task_id, "score": score,
            "completed": st.get("completed", False)}, True, msg
