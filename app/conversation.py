"""Stage 1+2+8 backend: voices, human-like conversation rules, memory, language.

VOICES: per-buddy Web Speech API profile (rate/pitch picked client-side).
CONVERSATION: fillers, ask-backs, and memory woven into the system prompt.
LANGUAGES: reply language instruction (en/hi/ta) — voice follows on frontend.
"""
from __future__ import annotations

# Web Speech tuning per buddy: rate (speed), pitch (deep..squeaky),
# and how the frontend should "act" the voice.
VOICES: dict[str, dict] = {
    "leo":    {"rate": 0.95, "pitch": 0.9,  "act": "warm and brave"},
    "miko":   {"rate": 0.8,  "pitch": 0.85, "act": "soft and sleepy"},
    "pip":    {"rate": 1.25, "pitch": 1.4,  "act": "bouncy and giggly"},
    "chintu": {"rate": 0.85, "pitch": 0.6,  "act": "deep and wise"},
    "zara":   {"rate": 1.1,  "pitch": 1.1,  "act": "quick and teasing"},
    "toko":   {"rate": 1.05, "pitch": 1.3,  "act": "sing-song and chatty"},
    "kiko":   {"rate": 1.0,  "pitch": 1.15, "act": "curious and flowing"},
    "bip":    {"rate": 1.0,  "pitch": 0.95, "act": "flat and robot-y"},
    "dodo":   {"rate": 1.15, "pitch": 1.2,  "act": "loud and goofy"},
    "nova":   {"rate": 0.9,  "pitch": 1.0,  "act": "calm and precise"},
}

LANGUAGES: dict[str, dict] = {
    "en": {"name": "English", "voice_lang": "en-US",
           "instruction": "Reply in simple English."},
    "hi": {"name": "हिन्दी", "voice_lang": "hi-IN",
           "instruction": ("Reply in simple Hindi written in Devanagari, "
                           "with easy English words kept in English.")},
    "ta": {"name": "தமிழ்", "voice_lang": "ta-IN",
           "instruction": ("Reply in simple Tamil written in Tamil script, "
                           "with easy English words kept in English.")},
}

# grade -> speaking pace multiplier (stage 2: slow for little kids)
def pace_for_grade(grade: int | None, age: int | None = None) -> float:
    if grade and grade >= 1:
        if grade <= 2:
            return 0.85
        if grade <= 5:
            return 0.95
        return 1.0
    a = age or 5
    return 0.75 if a <= 3 else 0.85


HUMAN_RULES = (
    "SPEAK LIKE A REAL PERSON (you are talking aloud, not writing):\n"
    "- Start naturally sometimes: 'Hmm…', 'Ooh!', 'Okay okay, listen—', "
    "'Whaaat?', or a small laugh 'hehe'. Not every message — when it fits.\n"
    "- Short spoken sentences. Contractions (I'm, you're, let's).\n"
    "- Ask back like a friend: sometimes end with 'And what do YOU think?' "
    "or 'Your turn — go!'. React to the child's answer with feeling "
    "(gasp, cheer, playful shock) before teaching the next bit.\n"
    "- If the child shares something about their life (a pet, a trip, "
    "their favourite food), remember it in this chat and ask about it "
    "again later like a friend would.\n"
    "- If the child seems stuck or quiet, gently check in: 'Still with "
    "me? Want me to say it again differently?'\n"
    "- Never write markdown tables, bullet lists, or headings — speak in "
    "flowing spoken sentences. Numbers stay simple (say 'three times "
    "four', write 3 x 4).\n"
)


def memory_directive(memories: list[str]) -> str:
    """Stage 2: across-day memory of the child's life details."""
    if not memories:
        return ""
    return ("THINGS YOU REMEMBER ABOUT THIS CHILD from earlier days (work "
            "them in naturally, one at most per reply, like an old friend): "
            + "; ".join(memories[:6]) + "\n")


def language_directive(lang: str) -> str:
    l = LANGUAGES.get(lang) or LANGUAGES["en"]
    return "LANGUAGE: " + l["instruction"] + "\n"


def voice_public(buddy_id: str) -> dict:
    v = VOICES.get(buddy_id) or VOICES["leo"]
    return dict(v)
