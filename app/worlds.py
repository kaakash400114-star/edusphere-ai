"""The Four Worlds — Part 2 of EduSphere AI.

One app, five lands. Growing up = traveling to a new land.
- Sunny Meadow: KG little learners (grade 0) — letters/numbers/shapes/colors/rhymes through play
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
    emoji="🌸",
    tagline="Letters, numbers, shapes and songs — learning through play.",
    ages="Little learners (KG)",
    grades=(0, 0),
    color="#f472b6",
    greeting=("Welcome to Sunny Meadow! Pick a flower, count the "
              "butterflies, and sing with your buddy!"),
    mood=("Play-group guide. The child is 5 or 6 and may not read yet. "
          "Speak in tiny spoken sentences of at most 8 words. Teach "
          "letters, counting, shapes, colors and rhymes through play. "
          "Cheer every try. Gentle, slow, magical, zero pressure."),
    activities=[
        {"emoji": "🔤", "label": "Letter sounds", "prompt": "Teach me the letter A sound!"},
        {"emoji": "🍎", "label": "Counting fun", "prompt": "Count apples with me!"},
        {"emoji": "🔺", "label": "Shape hunt", "prompt": "Show me shapes around us!"},
        {"emoji": "🌈", "label": "Color splash", "prompt": "What do red and yellow make?"},
        {"emoji": "🎵", "label": "Rhyme time", "prompt": "Sing a rhyme with me!"},
        {"emoji": "🎲", "label": "Play a game", "prompt": "Let's play a fun learning game!"},
    ],
    host_ids=["pip", "miko", "leo"],
)

_register(
    id="academy",
    name="Scholar Academy",
    emoji="🏛️",
    tagline="Experiments, equations and big ideas for serious minds.",
    ages="Grades 6–8",
    grades=(6, 8),
    color="#38bdf8",
    greeting=("Welcome to Scholar Academy! Labs, logic and level climbs — "
              "your knowledge gets sharper here."),
    mood=("Mentor-coach. Clear explanations with real examples, higher-order "
          "questions, exam-smart tips. Encourage independent thinking, keep "
          "answers structured but not childish."),
    activities=[
        {"emoji": "🔬", "label": "Lab explorer", "prompt": "Explain a science concept with a real-life experiment I can picture!"},
        {"emoji": "🧮", "label": "Math mastery", "prompt": "Teach me a new math chapter with solved examples!"},
        {"emoji": "📝", "label": "Grammar gym", "prompt": "Give me a grammar workout with corrections!"},
        {"emoji": "🗺️", "label": "World facts", "prompt": "Quiz me on social studies facts!"},
        {"emoji": "🏆", "label": "Level challenge", "prompt": "Give me a challenge from my current level!"},
        {"emoji": "💡", "label": "Why it matters", "prompt": "Where is today's topic used in real life?"},
    ],
    host_ids=["nova", "bip", "kiko"],
)

_register(
    id="tower",
    name="Wisdom Tower",
    emoji="🗼",
    tagline="The summit for senior learners — boards and beyond.",
    ages="Grades 9–12",
    grades=(9, 12),
    color="#f472b6",
    greeting=("Welcome to the Wisdom Tower. Deep concepts, board-level "
              "answers and every climb counts toward your future."),
    mood=("Senior tutor. Board-exam depth, precise definitions, worked "
          "answers, exam strategy; respects intelligence, no baby talk, "
          "still warm and encouraging."),
    activities=[
        {"emoji": "📚", "label": "Board prep", "prompt": "Teach me a board-exam chapter with important questions!"},
        {"emoji": "🧪", "label": "Physics-Chem-Bio drill", "prompt": "Give me a mixed science drill with solutions!"},
        {"emoji": "✍️", "label": "Answer writing", "prompt": "Show me how to write full-mark answers!"},
        {"emoji": "🧠", "label": "Concept deep dive", "prompt": "Explain the hardest concept of my grade simply!"},
        {"emoji": "📊", "label": "Weekly test", "prompt": "Take a 5-question test from my syllabus!"},
        {"emoji": "🎯", "label": "Doubt clinic", "prompt": "I have a doubt — explain step by step!"},
    ],
    host_ids=["nova", "zara"],
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

    Grade 0 (KG) -> Sunny Meadow, 1-2 -> Explorer Village,
    3-5 -> Champion Mountains, 6-8 -> Scholar Academy, 9-12 -> Wisdom Tower.
    `age` is ignored.
    """
    g = int(grade or 0)
    if g <= 0:
        return WORLDS["meadow"]
    for w in WORLDS.values():
        lo, hi = w["grades"]
        if lo and lo <= g <= hi:
            return w
    return WORLDS["tower"]  # safety net


def public(wid: str) -> dict:
    w = WORLDS.get(wid) or WORLDS["village"]
    return {k: w.get(k) for k in _PUBLIC_FIELDS}


def roster() -> list[dict]:
    return [public(w) for w in ("meadow", "village", "mountains", "academy", "tower")]


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
    """All four worlds teach the graded curriculum files."""
    return subject if subject in ("math", "science", "english") else "general"
