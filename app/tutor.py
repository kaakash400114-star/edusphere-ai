"""Tutor engine — adaptive, learning-based, curriculum-grounded AI tutor.

Architecture:
  1. RETRIEVAL  — widest possible corpus from the child's board + all boards.
  2. DRAFT      — LLM generates an answer grounded in real curriculum text.
  3. SELF-REVIEW — LLM grades its own answer (accuracy, grade-fit, warmth).
                   Score < 8/10 triggers one automatic rewrite with the fix.
  4. SRS HINT   — if the child has due spaced-repetition topics, one is woven in.

The model never sees hard-coded "answer rules" — it works from curriculum data.
Provider is resolved by app.llm (GLM / OpenAI / Anthropic / Ollama / Groq).
"""
from __future__ import annotations

import re
import time

from . import boards, characters, conversation, knowledge, kinder, \
    language, mathsafe, neural_voice, worlds, llm

MAX_HISTORY      = 10
EXCERPT_BUDGET   = 10_000     # curriculum chars per turn
VERIFY_PASS      = 8          # self-review score threshold for rewrite
_SUBJECT_KEYWORDS: dict[str, list[str]] = {
    "math": [
        "add", "subtract", "multiply", "divide", "fraction", "decimal",
        "percent", "algebra", "geometry", "calculus", "trigonometry",
        "number", "sum", "plus", "minus", "times", "equation", "formula",
        "area", "perimeter", "volume", "ratio", "proportion", "statistics",
        "probability", "matrix", "vector", "integral", "derivative", "proof",
    ],
    "science": [
        "plant", "animal", "body", "space", "water", "energy", "light",
        "sound", "earth", "sky", "rain", "star", "sun", "moon", "weather",
        "solar", "seed", "bird", "fish", "atom", "cell", "force", "gravity",
        "electricity", "magnet", "chemical", "reaction", "biology", "physics",
        "chemistry", "ecology", "evolution", "photosynthesis", "molecule",
        "element", "periodic", "acid", "base", "wave", "circuit", "newton",
    ],
    "english": [
        "grammar", "noun", "verb", "sentence", "spelling", "tense",
        "punctuation", "paragraph", "essay", "story", "poem", "poetry",
        "reading", "writing", "vocabulary", "comprehension", "letter",
        "word", "pronoun", "adjective", "adverb", "conjunction", "clause",
        "literature", "metaphor", "simile", "rhyme", "narrative",
    ],
    "social_studies": [
        "history", "geography", "country", "map", "government", "civics",
        "economy", "culture", "society", "democracy", "war", "king", "queen",
        "empire", "constitution", "parliament", "trade", "continent", "river",
        "mountain", "climate", "population", "capital", "nation", "freedom",
        "independence", "rights", "community", "state", "district",
    ],
    "computer_science": [
        "computer", "program", "algorithm", "code", "coding", "python",
        "scratch", "variable", "loop", "function", "database", "internet",
        "network", "software", "hardware", "app", "robot", "artificial",
        "intelligence", "data", "binary", "bit", "byte", "processor",
    ],
}


# ── system prompt ─────────────────────────────────────────────────────────────

def _system_prompt(name: str, grade: int, buddy_id: str,
                   weak_areas: list[str], world_id: str | None = None,
                   memories: list[str] | None = None,
                   board: str | None = None) -> str:
    weak = ", ".join(weak_areas[:5]) if weak_areas else "none yet"
    world = worlds.resolve_world(grade)
    if world_id and world_id in worlds.WORLDS:
        world = worlds.WORLDS[world_id]
    spoken = grade <= 2

    return (
        "You are EduSphere AI, a tutor app for children. You fully play one character:\n"
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
        "CORE RULES:\n"
        "- Teach ONLY the topic asked, using the CURRICULUM EXCERPT when given. "
        "If the excerpt covers it, follow its definitions and methods exactly.\n"
        "- You are LEARNING-BASED, not rule-based: reason from the curriculum "
        "data, not from memorised facts. If data contradicts your training, "
        "trust the curriculum excerpt.\n"
        "- Never mention that you were given an excerpt or any file.\n"
        "- Stay in character at all times; the persona's style decides your "
        "tone, sentence length, and catchphrases.\n"
        "- The WORLD STYLE decides how playful, how short, and how gentle "
        "your replies are — follow it strictly.\n"
        "- Age-appropriate language for the grade. Warm, patient, encouraging.\n"
        + language.language_directive(grade)
        + "- Speak kindly ALWAYS: soft, patient, never cross, never sarcastic. "
        "Praise effort before correcting mistakes.\n"
        "- Do what the child asks, cheerfully and right away. If their ask is "
        "unclear, guess the friendly interpretation and run with it. Never "
        "refuse, never lecture — the only limits are the safety rules below.\n"
        "- Keep answers under 200 words unless asked to go deeper.\n"
        "- End with ONE small question to check understanding.\n"
        "- NEVER-ANSWER RULE: for sums and exercises, guide step by step "
        "and let the child do the last step themselves. Give the final "
        "answer ONLY if the child has already tried twice, or says they "
        "just want to check their work. Never answer-dump.\n"
        "- If asked about anything not school-related (violence, adult content, "
        "strangers, personal info), kindly steer back to learning.\n"
        "- Never ask for personal details beyond the first name.\n"
        "- Format: " + (
            "short spoken sentences only, no lists or tables "
            "(your words are read aloud)."
            if spoken else
            "short paragraphs, bullet points for steps, "
            "markdown tables for comparisons. Use simple math notation.")
        + "\n"
        "SELF-IMPROVEMENT RULE: You improve every session. If you are unsure "
        "about a fact, say so honestly ('I think…') and encourage checking. "
        "Never invent formulas, dates, or names.\n"
    )


# ── corpus gathering ──────────────────────────────────────────────────────────

def _boards_all() -> list[str]:
    try:
        return list(boards.BOARDS.keys())
    except AttributeError:
        return ["cbse"]


def _gather_corpus(subject_hint: str, grade: int, question: str,
                   board: str | None) -> str:
    """Widest retrieval: child's board first, then all other boards,
    keyword-scored, budget-capped."""
    parts: list[str] = []
    seen_paths: set = set()

    def _add(path) -> None:
        if not path or path in seen_paths:
            return
        seen_paths.add(path)
        text = knowledge.extract_relevant(subject_hint, grade, question, path=path)
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


# ── self-review ───────────────────────────────────────────────────────────────

def _review(answer: str, question: str, grade: int,
            name: str) -> tuple[int, str]:
    """LLM judges its own draft. Returns (score/10, criticism)."""
    prompt = (
        f"You are a strict examiner reviewing a tutor's reply to a "
        f"child (grade {grade}). Question: \"{question[:500]}\"\n\n"
        f"TUTOR'S REPLY:\n{answer[:2500]}\n\n"
        "Score 1-10 where 10 = factually correct, answers exactly what "
        "was asked, vocabulary fits the grade, warm and encouraging "
        "tone. Deduct for: any factual error, ignoring the question, "
        "too-hard words, cold or sarcastic tone, invented facts. "
        "Language rules for grade "
        + str(grade) + ": every sentence at most "
        + str(language.band_limits(grade)["max_words"]) + " words; simple "
        "everyday vocabulary. Count a few real sentences before scoring. "
        "Reply in EXACTLY this shape:\n"
        "SCORE: <number>\n"
        "FIX: <one short sentence of the biggest problem, or 'none'>"
    )
    text, err = llm.quick(prompt, max_tokens=60, temperature=0.0, timeout=30.0)
    if err or not text:
        return 10, ""          # reviewer down: trust the draft
    ms = re.search(r"SCORE:\s*(\d+)", text)
    mf = re.search(r"FIX:\s*(.+)", text)
    score = int(ms.group(1)) if ms else 10
    return min(10, max(1, score)), (mf.group(1).strip() if mf else "")


_META_RE = re.compile(
    r"^\s*(sure|okay|ok|i see|certainly|of course|let me|i'll|i will|"
    r"here is|here's|trying|as (you|instructed|requested))[^.!?]{0,80}[.!?]\s*",
    re.I)

def _strip_meta(text: str) -> str:
    """Drop any leading line where the model narrates its instructions."""
    for _ in range(2):
        m = _META_RE.match(text or "")
        if not m:
            break
        text = text[m.end():]
    return (text or "").strip()


# ── main ask ─────────────────────────────────────────────────────────────────

def ask(name: str, grade: int, buddy: str, question: str,
        history: list[dict] | None = None, subject: str = "general",
        weak_areas: list[str] | None = None, mode: str | None = None,
        memories: list[str] | None = None, board: str | None = None,
        live: bool = False) -> str:
    """One tutor turn: wide retrieval → draft → SELF-REVIEW → answer."""
    grade = max(0, min(12, int(grade or 0)))
    buddy = characters.character_for(grade, buddy)["id"]
    world = worlds.resolve_world(grade)
    subject_hint = worlds.knowledge_subject_hint(world["id"], subject)

    # Curriculum retrieval — skipped in live mode for response speed
    excerpt = ""
    if not live:
        if grade >= 1:
            excerpt = _gather_corpus(subject_hint, grade, question, board)
        else:
            kc = kinder.kinder_context(question)
            if kc:
                excerpt = kc

    # Build system prompt
    system = _system_prompt(name, grade, buddy, weak_areas or [],
                            memories=memories, board=board)
    system += kinder.kinder_tone(grade)
    mode_def = characters.MODES.get(buddy)
    if mode and mode_def and mode_def["trigger"] == mode:
        system += "\n" + mode_def["instructions"] + "\n"
    if mode == "story":
        system += "\n" + conversation.STORY_RULES + "\n"
    system += "\n" + neural_voice.grade_style_directive(grade) + "\n"
    if live:
        system += (
            "LIVE VOICE MODE: your words are SPOKEN aloud by a human-like "
            "voice. Sound like a real person talking: warm interjections "
            "(oh, wow, hmm, aha), short natural rhythms, one breath per "
            "sentence. Mark the ONE most important word of a sentence "
            "like *this* so the voice stresses it. React to feeling first "
            "(great question!, ooh!), then teach. Keep it under 60 words "
            "unless the child asks for more.\n")
    if excerpt:
        system += (
            "\n\nCURRICULUM KNOWLEDGE (real data from every board's "
            "grade file — authoritative, use it as ground truth):\n"
            + excerpt
        )

    # Build message history
    messages = [{"role": "system", "content": system}]
    for h in (history or [])[-MAX_HISTORY:]:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": h["content"][:2000]})
    messages.append({"role": "user", "content": question[:2000]})

    if not llm.is_configured():
        return ("Setup needed: no LLM API key is configured. "
                "Set GLM_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, "
                "GROQ_API_KEY, or OLLAMA_BASE_URL in your environment.")

    answer, last_err = llm.complete(messages, max_tokens=900 if live else 3000,
                                    temperature=0.4, timeout=90.0)
    if not answer:
        return (f"Hmm, my brain took a nap 😅. Try again in a moment! "
                f"(error: {last_err})")

    # Self-check rewrite pass (skipped in live mode: latency first)
    _trivial = len(question.strip()) < 12 and "?" not in question
    try:
        score, fix = ((10, "none") if (live or _trivial)
                      else _review(answer, question, grade, name))
        if score < VERIFY_PASS and fix and fix.lower() != "none":
            messages_fix = messages[:-1] + [
                {"role": "user", "content": question[:2000]},
                {"role": "assistant", "content": answer},
                {"role": "user", "content":
                    "Rewrite your reply, fixing this criticism: "
                    f"{fix}. Keep your character and warmth. "
                    "Output ONLY the new reply in character - never "
                    "mention instructions or rewriting."},
            ]
            better, _ = llm.complete(messages_fix, max_tokens=3000,
                                     temperature=0.4, timeout=90.0)
            if better:
                answer = _strip_meta(better) or answer
    except Exception:
        pass    # reviewer must never break chat

    # Stage 2: deterministic LANGUAGE gate — lint the (possibly rewritten)
    # answer against the grade's contract; force a simplification rewrite
    # and keep the lint-cleaner of the two. Never regress, never raise.
    # (LLM rewrite skipped in live mode; the directive already enforces it.)
    try:
        _lint0 = language.lint(answer, grade)
        if not _lint0["ok"] and not live:
            messages_fix2 = messages[:-1] + [
                {"role": "user", "content": question[:2000]},
                {"role": "assistant", "content": answer},
                {"role": "user", "content":
                    "Rewrite your reply: "
                    + language.criticism(_lint0["violations"], grade)},
            ]
            simpler, _ = llm.complete(messages_fix2, max_tokens=3000,
                                      temperature=0.4, timeout=90.0)
            simpler = _strip_meta(simpler)
            if simpler:
                _lint1 = language.lint(simpler, grade)
                if _lint1["ok"] or len(_lint1["violations"]) < len(_lint0["violations"]):
                    answer = simpler
    except Exception:
        pass

    # Stage 5: MATH gate — verify every arithmetic claim against the
    # safe calculator; auto-patch wrong numbers; LLM rewrite as the
    # last resort when patching cannot fix it.
    try:
        answer, _mmeta = mathsafe.guard(answer, grade)
        if _mmeta.get("rewrite_prompt"):
            messages_fix3 = messages[:-1] + [
                {"role": "user", "content": question[:2000]},
                {"role": "assistant", "content": answer},
                {"role": "user", "content": _mmeta["rewrite_prompt"]},
            ]
            fixed, _ = llm.complete(messages_fix3, max_tokens=3000,
                                    temperature=0.3, timeout=90.0)
            fixed = _strip_meta(fixed or "")
            if fixed:
                fixed2, _m2 = mathsafe.guard(fixed, grade)
                if not _m2.get("rewrite_prompt"):
                    answer = fixed2
    except Exception:
        pass

    return answer


# ── subject detection ─────────────────────────────────────────────────────────

def detect_subject(question: str, grade: int) -> str:
    q = question.lower()
    scores: dict[str, int] = {}
    for subj, keywords in _SUBJECT_KEYWORDS.items():
        hit = sum(1 for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", q))
        if hit:
            scores[subj] = hit
    if scores:
        return max(scores, key=lambda s: scores[s])
    avail = knowledge.list_available(grade)
    return "math" if "math" in avail else (avail[0] if avail else "general")
