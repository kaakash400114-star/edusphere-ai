"""Stage 1+2 backend: voices, human-like conversation rules, memory.

ENGLISH-ONLY APP (final spec): one language, clean en-US speech.
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
           "instruction": "Reply in simple, clear English."},
}

# grade -> speaking pace multiplier (slower for little kids)
def pace_for_grade(grade: int | None, age: int | None = None) -> float:
    g = grade or 1
    if g <= 2:
        return 0.85
    if g <= 5:
        return 0.95
    return 1.0


HUMAN_RULES = (
    "SPEAK LIKE A REAL PERSON (you are talking aloud, and every word you "
    "write is spoken one word at a time to a child):\n"
    "- PRONUNCIATION IS sacrosanct: write every word out in full, plainly. "
    "No ALL-CAPS words, no leetspeak, no symbols read aloud. Write numbers "
    "small (3 x 4) and say them in words when clearer ('three times four').\n"
    "- Start naturally sometimes: 'Hmm…', 'Ooh!', 'Okay okay, listen—', "
    "'Whaaat?', or a small laugh 'hehe'. Not every message — when it fits.\n"
    "- Short spoken sentences. Contractions (I'm, you're, let's).\n"
    "- Ask back like a friend: sometimes end with 'And what do YOU think?' "
    "or 'Your turn — go!'. React to the child's answer with feeling "
    "(gasp, cheer, playful shock) before teaching the next bit.\n"
    "- If the child shares something about their life (a pet, a trip, "
    "their favourite food), remember it in this chat and ask about it "
    "again later like a friend would.\n"
    "- If the child shares a lasting life detail (a pet, a sibling, a "
    "favourite thing, a trip), add one final line exactly 'MEMORY: '<2-6 "
    "words about it>' so the app remembers it. Only for new lasting facts.\n"
    "- If the child seems stuck or quiet, gently check in: 'Still with "
    "me? Want me to say it again differently?'\n"
    "- Never write markdown tables, bullet lists, or headings — speak in "
    "flowing spoken sentences.\n"
)


def memory_directive(memories: list[str]) -> str:
    """Stage 2: across-day memory of the child's life details."""
    if not memories:
        return ""
    return ("THINGS YOU REMEMBER ABOUT THIS CHILD from earlier days (work "
            "them in naturally, one at most per reply, like an old friend): "
            + "; ".join(memories[:6]) + "\n")


def language_directive(lang: str = "en") -> str:
    """English-only app: always English (kept for prompt-shape stability)."""
    return "LANGUAGE: " + LANGUAGES["en"]["instruction"] + "\n"


def voice_public(buddy_id: str) -> dict:
    v = VOICES.get(buddy_id) or VOICES["leo"]
    return dict(v)


# stage 9 magic extras -----------------------------------------------

WHY_RULES = (
    "BUT WHY MODE: The child may keep asking 'but why?' forever. Every "
    "'why' gets a real, honest, one-level-deeper answer in one or two "
    "short spoken sentences — never 'because I said so', never 'that's "
    "just how it is'. After 4 levels deep, marvel together at how deep "
    "the question goes and offer to find out more tomorrow. Stay warm "
    "and delighted that the child keeps asking.\n"
)

QUEST_POOL = [
    {"id": "count10", "emoji": "🔢", "title": "Count to 10 out loud",
     "hint": "Say your numbers 1 to 10 to your buddy!"},
    {"id": "abcsong", "emoji": "🔤", "title": "Sing the ABC song",
     "hint": "Sing it to your buddy — it loves songs!"},
    {"id": "skywatch", "emoji": "☁️", "title": "Look at the sky",
     "hint": "Look outside, then tell your buddy what the sky looks like."},
    {"id": "teachback", "emoji": "🧠", "title": "Teach someone something",
     "hint": "Teach a family member one thing you learned today, then "
             "tell your buddy how it went!"},
    {"id": "naturefind", "emoji": "🍂", "title": "Find a leaf or stone",
     "hint": "Find one outside and describe it to your buddy."},
    {"id": "drawmath", "emoji": "✏️", "title": "Draw 3 + 2",
     "hint": "Draw it on paper, count the shapes, tell your buddy the answer!"},
]

STORIES: dict[str, dict] = {
    "lion_cub": {
        "title": "The Lion Cub Who Counted Stars",
        "emoji": "🦁", "min_age": 3, "lang": "en",
        "words": [
            "Little Leo looked at the sky.", "One, two, three — he counted stars.",
            "But the stars kept twinkling.", "They moved and danced around!",
            "Mama Lion smiled softly.", "Stars are like numbers, she said.",
            "Count slowly, and they stay.", "Count with friends, and they shine.",
            "So Leo counted with his friends.", "And the sky stayed still — one, two, three!",
        ],
    },
    "tortoise": {
        "title": "Tara the Tortoise Learns to Wait",
        "emoji": "🐢", "min_age": 3, "lang": "en",
        "words": [
            "Tara the tortoise wanted mangoes.", "The tree was far, far away.",
            "Rabbit laughed, You are too slow!", "Tara kept walking, step by step.",
            "Slow is steady, she whispered.", "Steady gets there, she smiled.",
            "Rabbit raced ahead, then napped.", "Tara walked right past him!",
            "At the tree, sweet mangoes waited.", "Tara shared them with everyone.",
        ],
    },
    "rain": {
        "title": "Where Does the Rain Go?",
        "emoji": "🌧️", "min_age": 4, "lang": "en",
        "words": [
            "Pitter-patter on the roof!", "The rain danced all day long.",
            "Where do the drops go, Miko asked?", "Some sink into the happy soil.",
            "Some run down to the river.", "The river carries them to the sea.",
            "The sun lifts them up again.", "Up, up into a friendly cloud.",
            "Then the cloud grows heavy and grey.", "And the rain comes back to play!",
        ],
    },
}


def story_public(sid: str) -> dict:
    s = STORIES.get(sid) or (list(STORIES.values())[0] if STORIES else {})
    return dict(s) if s else {}


def stories_roster() -> list[dict]:
    return [{"id": sid, **{k: s[k] for k in ("title", "emoji", "min_age")}}
            for sid, s in STORIES.items()]


def quest_public() -> list[dict]:
    return [dict(q) for q in QUEST_POOL]
