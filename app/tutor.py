"""Tutor engine: talks to GLM with grade-aware, curriculum-locked prompts.

The buddy persona comes from app.characters (the Character Universe).
"""
from __future__ import annotations

import os
import time

import httpx

from . import characters, conversation, knowledge, worlds

BASE_URL = os.environ.get(
    "GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4").rstrip("/")
MODEL = os.environ.get("EDUSPHERE_MODEL", "glm-4.5-flash")
MAX_HISTORY = 8

def _system_prompt(name: str, grade: int, buddy_id: str,
                   weak_areas: list[str], world_id: str | None = None,
                   memories: list[str] | None = None) -> str:
    weak = ", ".join(weak_areas[:5]) if weak_areas else "none yet"
    world = worlds.resolve_world(grade)
    if world_id and world_id in worlds.WORLDS:
        world = worlds.WORLDS[world_id]
    spoken = world_id in ("meadow", "kindergarten")  # pre-grade worlds no longer exist
    return (
        "You are EduSphere AI, a tutor app for children. You fully play one "
        "character:\n"
        + characters.persona_prompt(buddy_id)
        + worlds.world_prompt(world)
        + conversation.HUMAN_RULES
        + conversation.memory_directive(memories or [])
        + conversation.language_directive()
        + (f"\nSTUDENT: {name}, grade {grade} (about age {5 + grade}).\n")
        + f"WEAK AREAS to gently revisit: {weak}.\n\n"
        "RULES:\n"
        "- Teach ONLY the topic asked, using the CURRICULUM EXCERPT when given. "
        "If the excerpt covers it, follow its definitions and methods.\n"
        "- Never mention that you were given an excerpt or any file.\n"
        "- Stay in character at all times; the persona's style decides your "
        "tone, sentence length, and catchphrases.\n"
        "- The WORLD STYLE decides how playful, how short, and how gentle "
        "your replies are — follow it strictly.\n"
        "- Age-appropriate language for the grade. Warm, patient, encouraging.\n"
        "- Keep answers under 180 words unless asked to go deeper.\n"
        "- End with ONE small question to check understanding.\n"
        "- If asked about anything not school-related (violence, adult content, "
        "strangers, personal info), kindly steer back to learning.\n"
        "- Never ask for personal details beyond the first name.\n"
        "- Format: " + ("short spoken sentences only, no lists or tables "
         "(your words are read aloud)." if spoken else
         "short paragraphs, bullet points for steps, "
         "markdown tables for comparisons. Use simple math notation.")
    )


def _extract_content(data: dict) -> str:
    try:
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or ""
        return content.strip() or (reasoning[:1500] if reasoning else "")
    except (KeyError, IndexError, TypeError):
        return ""


def ask(name: str, grade: int, buddy: str, question: str,
        history: list[dict] | None = None, subject: str = "general",
        weak_areas: list[str] | None = None, mode: str | None = None,
        memories: list[str] | None = None) -> str:
    """One tutor turn: buddy persona + world style + human speech -> answer."""
    grade = max(1, min(12, int(grade or 1)))
    buddy = characters.character_for(grade, buddy)["id"]
    world = worlds.resolve_world(grade)
    subject_hint = worlds.knowledge_subject_hint(world["id"], subject)
    excerpt = knowledge.extract_relevant(subject_hint, grade, question)
    system = _system_prompt(name, grade, buddy, weak_areas or [],
                            memories=memories)
    mode_def = characters.MODES.get(buddy)
    if mode and mode_def and mode_def["trigger"] == mode:
        system += "\n" + mode_def["instructions"] + "\n"
    if mode == "story":
        system += "\n" + conversation.STORY_RULES + "\n"
    if excerpt:
        system += ("\n\nCURRICULUM EXCERPT (authoritative for this grade):\n"
                   + excerpt)
    messages = [{"role": "system", "content": system}]
    for h in (history or [])[-MAX_HISTORY:]:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": h["content"][:2000]})
    messages.append({"role": "user", "content": question[:2000]})

    api_key = os.environ.get("GLM_API_KEY", "")
    if not api_key:
        return "Setup needed: the GLM_API_KEY environment variable is missing."
    body = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 3000,
        "temperature": 0.4,
        "thinking": {"type": "disabled"},
    }
    last_err = None
    for attempt in range(2):
        try:
            r = httpx.post(
                f"{BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=body, timeout=90.0)
            data = r.json()
            text = _extract_content(data)
            if text:
                return text
            last_err = data.get("error") or data
        except (httpx.HTTPError, ValueError) as exc:
            last_err = str(exc)
        time.sleep(1.5 * (attempt + 1))
    return ("Hmm, my brain took a nap \U0001f605. Try again in a moment! "
            f"(error: {last_err})")


def detect_subject(question: str, grade: int) -> str:
    q = question.lower()
    if any(w in q for w in ("add", "subtract", "multiply", "divide", "fraction",
                            "number", "sum", "plus", "minus", "times", "math",
                            "geometry", "decimal", "percent", "algebra")):
        return "math"
    if any(w in q for w in ("plant", "animal", "body", "space", "water",
                            "science", "energy", "light", "sound", "earth",
                            "sky", "blue", "rain", "star", "sun", "moon",
                            "weather", "solar", "seed", "bird", "fish")):
        return "science"
    if any(w in q for w in ("grammar", "noun", "verb", "sentence", "spelling",
                            "english", "tense", "punctuation")):
        return "english"
    avail = knowledge.list_available(grade)
    return "math" if "math" in avail else (avail[0] if avail else "general")
