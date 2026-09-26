"""Tutor engine: talks to GLM with grade-aware, curriculum-locked prompts.

The buddy persona comes from app.characters (the Character Universe).
Every answer is LEARNING-BASED and SELF-CHECKING:

- retrieval gathers the widest relevant corpus (the child's board file
  first, then the same subject across ALL boards) — the model thinks from
  real curriculum data, not from hard-coded rules;
- after drafting, the model REVIEWS ITS OWN ANSWER (accuracy, grade-fit,
  tone, did it actually answer the question). Below 8/10 it rewrites once
  with the criticism injected. No fixed templates anywhere.
"""
from __future__ import annotations

import os
import time

import httpx

from . import boards, characters, conversation, knowledge, kinder, \
    neural_voice, worlds

BASE_URL = os.environ.get(
    "GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4").rstrip("/")
MODEL = os.environ.get("EDUSPHERE_MODEL", "glm-4.5-flash")
MAX_HISTORY = 8
EXCERPT_BUDGET = 9000          # total curriculum chars fed per turn
VERIFY_PASS = 8                # self-review score below this forces a rewrite

def _system_prompt(name: str, grade: int, buddy_id: str,
                   weak_areas: list[str], world_id: str | None = None,
                   memories: list[str] | None = None,
                   board: str | None = None) -> str:
    weak = ", ".join(weak_areas[:5]) if weak_areas else "none yet"
    world = worlds.resolve_world(grade)
    if world_id and world_id in worlds.WORLDS:
        world = worlds.WORLDS[world_id]
    spoken = grade <= 2  # little learners: pure spoken play, no lists
    return (
        "You are EduSphere AI, a tutor app for children. You fully play one "
        "character:\n"
        + characters.persona_prompt(buddy_id)
        + worlds.world_prompt(world)
        + conversation.HUMAN_RULES
        + conversation.memory_directive(memories or [])
        + conversation.language_directive()
        + boards.english_directive(board)
        + (f"\nSTUDENT: {name}, "
           + (f"age about {4 + grade}, in kindergarten (play-based learning)"
              if grade <= 0 else f"grade {grade} (about age {5 + grade}).") + "\n")
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
        "- Speak kindly ALWAYS: soft, patient, never cross, never sarcastic. "
        "Praise effort before correcting mistakes.\n"
        "- Do what the child asks, cheerfully and right away. If their ask is "
        "unclear, guess the friendly interpretation and run with it. Never "
        "refuse, never lecture — the only limits are the safety rules below.\n"
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


def _llm(body: dict, timeout: float = 90.0) -> tuple[str, object]:
    """One raw completion call. Returns (content, error)."""
    api_key = os.environ.get("GLM_API_KEY", "")
    if not api_key:
        return "", "no GLM_API_KEY"
    try:
        r = httpx.post(f"{BASE_URL}/chat/completions",
                       headers={"Authorization": f"Bearer {api_key}"},
                       json=body, timeout=timeout)
        if r.status_code == 429:
            return "", "rate-limited"
        return _extract_content(r.json()), None
    except (httpx.HTTPError, ValueError) as exc:
        return "", exc


def _gather_corpus(subject_hint: str, grade: int, question: str,
                   board: str | None) -> str:
    """Widest retrieval: the child's board first, then ALL boards' files
    for the same subject/grade (deduped), keyword-scored, budget-capped.
    This is what makes answers learning-based — real data, not rules."""
    parts: list[str] = []
    seen_paths: set = set()

    def _add(path) -> None:
        if not path or path in seen_paths:
            return
        seen_paths.add(path)
        text = knowledge.extract_relevant(subject_hint, grade, question,
                                          path=path)
        if text:
            parts.append(text)

    _add(boards.knowledge_path_for(board, subject_hint, grade))
    for other_board in _boards_all():
        if other_board == board:
            continue
        _add(boards.knowledge_path_for(other_board, subject_hint, grade))
    out, used = [], 0
    for p in parts:
        if used + len(p) > EXCERPT_BUDGET:
            continue
        out.append(p)
        used += len(p)
    return "\n\n".join(out)


def _boards_all() -> list[str]:
    try:
        return list(boards.BOARDS.keys())
    except AttributeError:                         # pragma: no cover
        return ["cbse"]


def _review(answer: str, question: str, grade: int,
            name: str) -> tuple[int, str]:
    """The model judges its own draft. Returns (score/10, criticism)."""
    body = {
        "model": MODEL,
        "max_tokens": 300,
        "temperature": 0.0,
        "thinking": {"type": "disabled"},
        "messages": [{"role": "user", "content": (
            "You are a strict examiner reviewing a tutor's reply to a "
            f"child (grade {grade}). Question: \"{question[:500]}\"\n\n"
            f"TUTOR'S REPLY:\n{answer[:2500]}\n\n"
            "Score 1-10 where 10 = factually correct, answers exactly what "
            "was asked, vocabulary fits the grade, warm and encouraging "
            "tone. Deduct for: any factual error, ignoring the question, "
            "too-hard words, cold or sarcastic tone, invented facts. "
            "Reply in EXACTLY this shape:\n"
            "SCORE: <number>\n"
            "FIX: <one short sentence of the biggest problem, or 'none'>")}],
    }
    text, err = _llm(body, timeout=45.0)
    if err or not text:
        return 10, ""                    # reviewer down: trust the draft
    import re
    ms = re.search(r"SCORE:\s*(\d+)", text)
    mf = re.search(r"FIX:\s*(.+)", text)
    score = int(ms.group(1)) if ms else 10
    return min(10, max(1, score)), (mf.group(1).strip() if mf else "")


def ask(name: str, grade: int, buddy: str, question: str,
        history: list[dict] | None = None, subject: str = "general",
        weak_areas: list[str] | None = None, mode: str | None = None,
        memories: list[str] | None = None, board: str | None = None) -> str:
    """One tutor turn: wide retrieval -> draft -> SELF-REVIEW -> answer."""
    grade = max(0, min(12, int(grade or 0)))
    buddy = characters.character_for(grade, buddy)["id"]
    world = worlds.resolve_world(grade)
    subject_hint = worlds.knowledge_subject_hint(world["id"], subject)
    excerpt = ""
    if grade >= 1:
        excerpt = _gather_corpus(subject_hint, grade, question, board)
    else:
        # KG: kindergarten foundations (letters, counting, shapes, colors)
        kc = kinder.kinder_context(question)
        if kc:
            excerpt = kc
    system = _system_prompt(name, grade, buddy, weak_areas or [],
                            memories=memories, board=board)
    # little learners get the play-based tone directive
    system += kinder.kinder_tone(grade)
    mode_def = characters.MODES.get(buddy)
    if mode and mode_def and mode_def["trigger"] == mode:
        system += "\n" + mode_def["instructions"] + "\n"
    if mode == "story":
        system += "\n" + conversation.STORY_RULES + "\n"
    # Stage 3: the buddy's WORDS mature with the child's grade —
    # sentence length, vocabulary and pronunciation precision scale up.
    system += "\n" + neural_voice.grade_style_directive(grade) + "\n"
    if excerpt:
        system += ("\n\nCURRICULUM KNOWLEDGE (real data from every board's "
                   "grade file — authoritative, use it as ground truth):\n"
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
    answer, last_err = "", None
    for attempt in range(2):
        text, err = _llm(body)
        if text:
            answer = text
            break
        last_err = err
        time.sleep(1.5 * (attempt + 1))
    if not answer:
        return ("Hmm, my brain took a nap \U0001f605. Try again in a moment! "
                f"(error: {last_err})")

    # ---- learning-based self-check: the model reviews its own words ----
    try:
        score, fix = _review(answer, question, grade, name)
        if score < VERIFY_PASS and fix and fix.lower() != "none":
            body["messages"] = messages[:-1] + [
                {"role": "user", "content": question[:2000]},
                {"role": "assistant", "content": answer},
                {"role": "user", "content":
                    "Rewrite your reply, fixing this criticism: "
                    f"{fix}. Keep your character and warmth."}]
            better, err2 = _llm(body)
            if better:
                answer = better
    except Exception:
        pass                              # reviewer must never break chat
    return answer


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
