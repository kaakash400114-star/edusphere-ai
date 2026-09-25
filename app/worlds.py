"""The Four Worlds — Part 2 of EduSphere AI.

One app, four lands. Growing up = traveling to a new land.
- Sunny Meadow: ages 1-3 (pre-grade, tap-joy, no failure)
- Rainbow Kindergarten: ages 4-5 (pre-grade, letters/numbers through play)
- Explorer Village: grades 1-2 (first reading, shop math, nature walks)
- Champion Mountains: grades 3-5 (multiplication climbs, fraction pizzas,
  grammar quests, science labs, tournaments)

Each world changes how the buddy talks, which activities are offered, and
what the curriculum excerpt focuses on. Single source of truth for the API,
the tutor engine, and the frontend world map.
"""
from __future__ import annotations

WORLDS: dict[str, dict] = {}

_PUBLIC_FIELDS = ("id", "name", "emoji", "tagline", "ages", "grades",
                  "color", "greeting", "mood", "activities", "host_ids")


def _register(**kw) -> None:
    wid = kw["id"]
    assert wid not in WORLDS, f"duplicate world id {wid}"
    WORLDS[wid] = kw


_register(
    id="meadow",
    name="Sunny Meadow",
    emoji="🌻",
    tagline="Tap, giggle, surprise! A land of quacks and pop-up colors.",
    ages="Ages 1–3",
    grades=(0, 0),  # pre-grade, age <= 3
    color="#fbbf24",
    greeting=("Welcome to Sunny Meadow! Tap the duck — QUACK! "
              "What shall we play?"),
    mood=("Pure cause-and-effect joy. Everything the child mentions pops, "
          "quacks, or giggles. SUPER short sentences (max 8 words). "
          "Celebrate every tap. Nothing is ever wrong."),
    activities=[
        {"emoji": "🦆", "label": "Animal sounds", "prompt": "Duck says quack! What do other animals say?"},
        {"emoji": "🎈", "label": "Pop the colors", "prompt": "Balloons pop with colors! Red! Blue! Show me more!"},
        {"emoji": "⭐", "label": "Shapes hide & seek", "prompt": "Circle and star are playing hide and seek!"},
        {"emoji": "🐻", "label": "Peek-a-boo", "prompt": "Peek-a-boo! Where is the bear?"},
        {"emoji": "1️⃣", "label": "Count 1 to 5", "prompt": "Let's count little ducks: 1, 2, 3, 4, 5!"},
        {"emoji": "🎵", "label": "Sing a rhyme", "prompt": "Sing a tiny song about a happy duck!"},
    ],
    host_ids=["pip", "miko"],
)

_register(
    id="kindergarten",
    name="Rainbow Kindergarten",
    emoji="🌈",
    tagline="Letters sing, numbers play, magic sand traces A-B-C.",
    ages="Ages 4–5",
    grades=(0, 0),  # pre-grade, age 4-5
    color="#f472b6",
    greeting=("Welcome to Rainbow Kindergarten! Toko has a new song — "
              "and magic sand for tracing letters!"),
    mood=("Playful teacher. Letters and numbers arrive through songs, "
          "mangoes, stars, and stories. Very short sentences, lots of "
          "sound-out words (c-a-t!). Every small win gets a sticker moment. "
          "Nothing is ever wrong — 'almost! try again with me'."),
    activities=[
        {"emoji": "🔤", "label": "Letter of the day", "prompt": "Teach me the letter A with a song!"},
        {"emoji": "🐱", "label": "c-a-t sounds", "prompt": "Sound out a new word with me: c-a-t!"},
        {"emoji": "🥭", "label": "Count to 20", "prompt": "Count mangoes with me up to 20!"},
        {"emoji": "✏️", "label": "Magic sand tracing", "prompt": "How do I write the letter S in magic sand?"},
        {"emoji": "🎶", "label": "Rhyme time", "prompt": "Sing a rhyme and I will sing along!"},
        {"emoji": "🔷", "label": "Shapes & colors", "prompt": "What shape is a ball? Teach me shapes!"},
    ],
    host_ids=["toko", "pip"],
)

_register(
    id="village",
    name="Explorer Village",
    emoji="🏘️",
    tagline="Stories where YOU are the hero, shop math, nature walks.",
    ages="Grades 1–2",
    grades=(1, 2),
    color="#34d399",
    greeting=("Welcome to Explorer Village, hero! The village shop needs "
              "your math — and Kiko found something on the nature trail!"),
    mood=("Adventure guide. The child is the hero of village stories. "
          "Math happens at the village shop (buying fruits, paying coins). "
          "Science is a nature walk with Kiko. Reading is a story about "
          "the child. First stars and streaks — celebrate them warmly."),
    activities=[
        {"emoji": "🏪", "label": "Village shop math", "prompt": "I am at the village shop — help me buy fruits and pay!"},
        {"emoji": "📖", "label": "My hero story", "prompt": "Tell me a story where I am the hero and I learn to read!"},
        {"emoji": "🌿", "label": "Nature walk", "prompt": "Take me on a nature walk — why does it rain?"},
        {"emoji": "➕", "label": "Add & subtract", "prompt": "Teach me adding and taking away with mangoes!"},
        {"emoji": "🔤", "label": "Read a sentence", "prompt": "Help me read a full sentence all by myself!"},
        {"emoji": "🐢", "label": "Animal friends", "prompt": "Which animals live in the village pond? Teach me about them!"},
    ],
    host_ids=["chintu", "kiko"],
)

_register(
    id="mountains",
    name="Champion Mountains",
    emoji="⛰️",
    tagline="Multiplication climbs, fraction pizzas, quests and tournaments.",
    ages="Grades 3–5",
    grades=(3, 5),
    color="#818cf8",
    greeting=("Welcome to Champion Mountains, challenger! Today's climb: "
              "harder multiplication, pizza fractions, and the Friday "
              "tournament. Ready?"),
    mood=("Big-kid coach. Real challenges with clear steps, friendly "
          "competition against your own best score. Multiplication is a "
          "climbing wall, fractions are pizza slices at the mountain cafe, "
          "grammar is a quest, science is a lab. Track progress proudly."),
    activities=[
        {"emoji": "🧗", "label": "Multiplication climb", "prompt": "Help me climb the multiplication wall — times tables!"},
        {"emoji": "🍕", "label": "Fraction pizzas", "prompt": "Teach me fractions using pizza slices!"},
        {"emoji": "⚔️", "label": "Grammar quest", "prompt": "Give me a grammar quest — nouns, verbs, and tenses!"},
        {"emoji": "🔬", "label": "Science lab", "prompt": "Do a science lab with me — why is the sky blue?"},
        {"emoji": "🏆", "label": "Weekly challenge", "prompt": "Give me a 5-question weekly challenge quiz!"},
        {"emoji": "🌍", "label": "World explorer", "prompt": "Tell me amazing facts about countries of the world!"},
    ],
    host_ids=["zara", "nova", "dodo"],
)


def resolve_world(grade: int | None = None, age: int | None = None) -> dict:
    """Pick the right world from grade.

    Grades 1-2 -> Explorer Village, 3-5 -> Champion Mountains, 6+ stays in
    Champion Mountains (it is the top land). Grade-only routing (final spec):
    no preschool, no age-based lands.
    """
    g = int(grade or 1)
    for w in WORLDS.values():
        lo, hi = w["grades"]
        if lo and lo <= g <= hi:
            return w
    return WORLDS["mountains"]  # grade 6+ tops out in the Mountains (for now)


def public(wid: str) -> dict:
    w = WORLDS.get(wid) or WORLDS["village"]
    return {k: w.get(k) for k in _PUBLIC_FIELDS}


def roster() -> list[dict]:
    return [public(w) for w in ("meadow", "kindergarten", "village", "mountains")]


def world_for_profile(profile: dict) -> dict:
    return resolve_world(profile.get("grade"), profile.get("age"))


def world_prompt(world: dict) -> str:
    """System-prompt fragment that puts the buddy inside this world."""
    acts = "; ".join(a["label"] for a in world["activities"])
    return (
        f"WORLD: {world['name']} {world['emoji']} ({world['ages']}). "
        f"{world['tagline']}\n"
        f"WORLD STYLE: {world['mood']}\n"
        f"WORLD ACTIVITIES you can offer: {acts}.\n"
    )


def knowledge_subject_hint(world_id: str, subject: str) -> str:
    """Pre-grade worlds teach play-scripts, not graded curriculum files."""
    if world_id == "meadow":
        return "meadow"
    if world_id == "kindergarten":
        return "kindergarten"
    return subject if subject in ("math", "science", "english") else "general"
