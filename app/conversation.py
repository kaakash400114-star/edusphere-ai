"""Stage 1+2 backend: voices, human-like conversation rules, memory.

ENGLISH-ONLY APP (final spec): one language, clean en-US speech.
"""
from __future__ import annotations

# Web Speech tuning per buddy: each buddy gets a DIFFERENT actual voice
# (voice_hints are matched against installed voice names, first hint wins)
# plus a human-range pitch tweak, so they sound like different people
# rather than one robot with pitch shifts.
# Voice pools: David (male, calm), Mark (male, deep), Zira (female, warm),
# Google US English (female, bright), Google UK Male, Google UK Female.
VOICES: dict[str, dict] = {
    # buddy      voice hints (in order)             rate  pitch  character
    "leo":    {"voice_hints": ["David", "Google UK Male"],   "rate": 0.95, "pitch": 1.0,  "act": "warm and brave male voice"},
    "miko":   {"voice_hints": ["UK English Male", "David"],   "rate": 0.8,  "pitch": 0.9,  "act": "soft, slow, sleepy male voice"},
    "pip":    {"voice_hints": ["Zira", "Google US English"], "rate": 1.2,  "pitch": 1.25, "act": "fast giggly young female voice"},
    "chintu": {"voice_hints": ["Mark", "David"],             "rate": 0.85, "pitch": 0.75, "act": "deep wise older male voice"},
    "zara":   {"voice_hints": ["Google US English", "Zira"], "rate": 1.1,  "pitch": 1.1,  "act": "quick teasing female voice"},
    "toko":   {"voice_hints": ["UK English Female", "Zira"],  "rate": 1.05, "pitch": 1.15, "act": "sing-song chatty British female voice"},
    "kiko":   {"voice_hints": ["Google US English", "Zira"], "rate": 1.0,  "pitch": 1.05, "act": "curious flowing female voice"},
    "bip":    {"voice_hints": ["David", "Mark"],             "rate": 1.0,  "pitch": 0.9,  "act": "flat precise robot-ish male voice"},
    "dodo":   {"voice_hints": ["Mark", "Google UK Male"],    "rate": 1.15, "pitch": 1.15, "act": "loud goofy dramatic male voice"},
    "nova":   {"voice_hints": ["Zira", "Google UK Female"],  "rate": 0.9,  "pitch": 1.0,  "act": "calm precise senior female voice"},
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
        "emoji": "🦁", "character": "Leo the lion cub",
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
        "emoji": "🐢", "character": "Tara the tortoise",
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
        "emoji": "🌧️", "character": "Miko the panda",
        "words": [
            "Pitter-patter on the roof!", "The rain danced all day long.",
            "Where do the drops go, Miko asked?", "Some sink into the happy soil.",
            "Some run down to the river.", "The river carries them to the sea.",
            "The sun lifts them up again.", "Up, up into a friendly cloud.",
            "Then the cloud grows heavy and grey.", "And the rain comes back to play!",
        ],
    },
}

# Stage G: INTERACTIVE conversational stories — the animal talks WITH the
# child. Each story: 6 beats; each beat = setup + question. The child's
# reply shapes the next beat (the model continues using STORY_RULES).
INTERACTIVE_STORIES: dict[str, dict] = {
    "brave_mouse": {
        "title": "Chintu and the Brave Little Mouse",
        "emoji": "🐘", "character": "Chintu the elephant",
        "grade_band": (1, 3),
        "topic_hint": "courage and kindness, counting and sizes",
        "beats": [
            "One evening, Chintu the elephant hears a tiny squeak near the river. It is a little mouse stuck in a deep hole!",
            "The mouse looks up and asks for help. But the hole is narrow — Chintu's trunk is too big to fit! What do you think Chintu should do?",
            "A cool idea! Chintu tries it. The mouse climbs closer, but the hole is still too deep. Now the mouse is scared of the dark. How can Chintu help the mouse feel brave?",
            "What a kind thought! The mouse takes a deep breath and stops crying. But now the sky rumbles — rain is coming! The hole will fill with water soon! What should Chintu do fast?",
            "Clever! The rain stops just in time. The mouse jumps onto a big leaf Chintu dropped in, and up it floats! The mouse is free! What should the mouse say to Chintu?",
            "The mouse thanks Chintu and the two become best friends under the starry sky. The mouse learned that even the biggest friend can be gentle, and Chintu learned that small friends bring big ideas.",
        ],
        "moral": "Big or small, everyone needs help sometimes — and kindness finds a way.",
    },
    "lost_puppy": {
        "title": "Pip and the Lost Puppy",
        "emoji": "🐿️", "character": "Pip the squirrel",
        "grade_band": (1, 3),
        "topic_hint": "helping others, directions, animal homes",
        "beats": [
            "Pip the squirrel is collecting acorns when he hears whimpering — a little puppy is lost near the big banyan tree!",
            "The puppy cannot remember its way home. It only remembers a yellow gate and the smell of mangoes. Where do you think the puppy lives?",
            "Ooh, good guess! Pip and the puppy hop toward the mango trees. But oh no — the path splits into three! Which way should they go?",
            "Let's try it! The chosen path leads to a pond with ducks. The puppy wags its tail — it remembers swimming here! But the sun is setting. What should they do now?",
            "Quick thinking! On the other side of the pond shines a yellow gate, and someone is calling a puppy's name! The puppy runs — it's home! What do the puppy's family say to Pip?",
            "The family thanks Pip with the biggest mango from their tree. Pip shares it with the puppy — and they promise to play again tomorrow.",
        ],
        "moral": "Helping a lost friend home is the greatest adventure of all.",
    },
    "river_rescue": {
        "title": "Kiko and the Clogged River",
        "emoji": "🐬", "character": "Kiko the dolphin",
        "grade_band": (3, 6),
        "topic_hint": "environment, water pollution, teamwork, science of water flow",
        "beats": [
            "Kiko the dolphin swims up the river to visit her fish friends — but the water is barely moving, and it smells strange. Something is blocking the river!",
            "Kiko investigates: plastic bags, sticks and old bottles have tangled together near a narrow bend. The fish are gasping — clean water cannot flow through! Why is it a problem when a river gets blocked?",
            "Exactly right — no flow means no fresh oxygen, and fish cannot breathe! Kiko pushes a big branch aside, but the plastic is stuck between rocks. What could loosen it?",
            "Brilliant! The rain from upstream helps loosen the tangle, and the fish push from below. Teamwork! But one last plastic bag is stuck tight. How can the animals stop this from happening again?",
            "What a wise idea! Kiko suggests the village children keep the banks clean and use cloth bags instead of plastic. Slowly, the river runs clear again, and the fish leap happily.",
            "That evening the river sparkles. Kiko learned that water always finds a way — and people can help it stay free.",
        ],
        "moral": "Nature gives us everything — keeping rivers clean keeps life flowing.",
    },
    "star_math": {
        "title": "Bip and the Space Station Puzzle",
        "emoji": "🤖", "character": "Bip the robot",
        "grade_band": (3, 6),
        "topic_hint": "multiplication, patterns, logical thinking",
        "beats": [
            "BEEP! Bip the robot is fixing a space station far away. The door has a number lock — 3 blinking lights showing: 2, 4, 6. What number should come next to open the door?",
            "B-Z-Z-T! The door hums — almost! The lock now shows a new pattern: 5, 10, 15. What comes next this time?",
            "DOOR OPEN! Inside, a screen flashes: 'To power the station, charge 4 batteries. Each battery needs 5 units. How many units in total?'",
            "POWER SURGING! The lights blink on. But a meteor shower is coming — Bip must close the shield in 10 seconds! Count down with Bip: 10, 9, 8… what comes next all the way to 1?",
            "SHIELD SECURED! Phew! The station is safe. The computer asks Bip one final question: 'What did you learn today?' What should Bip say?",
            "Bip types the answer and adds a smiley — because even robots know that thinking together beats thinking alone. BEEP-BEEP! Mission complete!",
        ],
        "moral": "Patterns and calm thinking solve even the trickiest space puzzles.",
    },
}

STORY_RULES = (
    "INTERACTIVE STORY MODE: You ARE the story animal named above, talking "
    "WITH the child (not narrating at them). The story beats are fixed; the "
    "child's last reply shapes THIS beat:\n"
    "- Welcome the child's idea into the story naturally ('What a clever "
    "thought! Chintu tries exactly that...'). If the idea is impossible, "
    "gently bend the story around it anyway — never say 'wrong'.\n"
    "- Speak 2-4 short spoken sentences per beat, then end with a warm "
    "question only on beats that need it.\n"
    "- Keep the animal's personality (its persona phrases may appear once).\n"
    "- On the final beat, tell the moral softly and cheer.\n"
    "- Never break character, never mention 'beats' or 'the story'.\n"
)


def story_public(sid: str) -> dict:
    s = STORIES.get(sid) or (list(STORIES.values())[0] if STORIES else {})
    return dict(s) if s else {}


def stories_roster() -> list[dict]:
    return [{"id": sid, **{k: s[k] for k in ("title", "emoji", "character")}}
            for sid, s in STORIES.items()]


def quest_public() -> list[dict]:
    return [dict(q) for q in QUEST_POOL]
