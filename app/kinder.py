"""Kinder Corner — little-learner activities for grades 1-2 (ages 5-7).

Phonics (letter sounds), counting (1-20), shapes, colors and rhymes.
Every activity is a tap-game: the server generates a task, the child taps
the answer, wrong taps just dim (no failure), and a finished round logs one
honest practice event (+2 points for the first correct round of the day,
same honest counting as practice topics).

Also feeds the tutor: kinder_context() turns a little kid's question about
letters/numbers/shapes/colors/rhymes into a compact curriculum excerpt so
the buddy teaches kindergarten foundations even though graded files start
at grade 1.
"""
from __future__ import annotations

import random
import re

KINDS: dict[str, dict] = {
    "phonics": {"emoji": "🔤", "name": "Phonics Fun"},
    "counting": {"emoji": "🍎", "name": "Counting Safari"},
    "shapes": {"emoji": "🔺", "name": "Shape Hunt"},
    "colors": {"emoji": "🌈", "name": "Color Splash"},
    "rhymes": {"emoji": "🎵", "name": "Rhyme Time"},
}

POINTS_PER_ROUND = 2

# letter -> three easy words; exactly one is the "answer" word shown with
# its emoji (the other two are the wrong options)
_LETTER_WORDS: dict[str, tuple[str, str, str, str, str]] = {
    # letter, right word, right emoji, wrong1, wrong2
    "A": ("Apple", "🍎", "Sun", "Ball"),
    "B": ("Ball", "⚽", "Cat", "Fish"),
    "C": ("Cat", "🐱", "Dog", "Sun"),
    "D": ("Dog", "🐶", "Egg", "Moon"),
    "E": ("Egg", "🥚", "Ant", "Kite"),
    "F": ("Fish", "🐟", "Hen", "Star"),
    "G": ("Goat", "🐐", "Duck", "Shoe"),
    "H": ("Hat", "🎩", "Cup", "Bee"),
    "I": ("Ice cream", "🍦", "Rain", "Tree"),
    "J": ("Jam", "🍯", "Fan", "Cow"),
    "K": ("Kite", "🪁", "Pen", "Owl"),
    "L": ("Lion", "🦁", "Net", "Car"),
    "M": ("Mango", "🥭", "Sock", "Hen"),
    "N": ("Nest", "🪹", "Map", "Cake"),
    "O": ("Orange", "🍊", "Grapes", "Chair"),
    "P": ("Parrot", "🦜", "Zebra", "Ring"),
    "Q": ("Queen", "👑", "Farmer", "Baby"),
    "R": ("Rain", "🌧️", "Sand", "Milk"),
    "S": ("Sun", "☀️", "Moon", "Bag"),
    "T": ("Tiger", "🐯", "Goat", "Shirt"),
    "U": ("Umbrella", "☂️", "Window", "Spoon"),
    "V": ("Van", "🚐", "Rocket", "Apple"),
    "W": ("Watch", "⌚", "Lamp", "Drum"),
    "X": ("X-ray", "🩻", "Sun", "Map"),
    "Y": ("Yo-yo", "🪀", "Book", "Cup"),
    "Z": ("Zebra", "🦓", "Tiger", "Duck"),
}

_FRUITS = [("Apples", "🍎"), ("Bananas", "🍌"), ("Mangoes", "🥭"),
           ("Stars", "⭐"), ("Balloons", "🎈"), ("Ducks", "🦆"),
           ("Flowers", "🌼"), ("Fish", "🐟")]

_SHAPES = [
    ("Triangle", "🔺", 3, "A triangle has 3 sides."),
    ("Square", "🟦", 4, "A square has 4 equal sides."),
    ("Circle", "⭕", 0, "A circle is perfectly round — no corners!"),
    ("Star", "⭐", 5, "A star has 5 points."),
    ("Heart", "💗", 0, "A heart shape has two round bumps."),
    ("Diamond", "🔷", 4, "A diamond leans on its corner."),
]

_COLOR_THINGS = [
    ("Red", "🍎", ["Banana", "Leaf", "Cloud"]),
    ("Yellow", "🍌", ["Apple", "Frog", "Grape"]),
    ("Green", " leaf", ["Sun", "Crow", "Strawberry"]),
    ("Blue", "🫐", ["Tomato", "Sun", "Banana"]),
    ("Orange", "🍊", ["Sky", "Milk", "Frog"]),
]

_RHYMES = [
    ("cat", ["hat", "bat", "mat"], ["sun", "dog", "car"]),
    ("dog", ["log", "fog", "frog"], ["cup", "bee", "star"]),
    ("sun", ["fun", "run", "bun"], ["pen", "map", "cow"]),
    ("cake", ["lake", "make", "sake"], ["milk", "shoe", "tree"]),
    ("star", ["car", "far", "jar"], ["dog", "pen", "bird"]),
    ("bee", ["tree", "see", "three"], ["cat", "box", "hat"]),
    ("ring", ["sing", "king", "wing"], ["cup", "sun", "dog"]),
    ("box", ["fox", "rocks", "socks"], ["ball", "tree", "cake"]),
]

_LETTER_LINE = (" ".join(f"{ch} for {w}" for ch, (w, *_rest) in
                         sorted(_LETTER_WORDS.items())))


def _opt_slide(text: str) -> dict:
    return {"id": text.lower()[:1] + str(abs(hash(text)) % 9999), "text": text}


def _mk_options(right: str, wrongs: list[str]) -> list[dict]:
    opts = [_opt_slide(right)] + [_opt_slide(w) for w in wrongs]
    random.shuffle(opts)
    return opts


def make_task(kind: str) -> dict | None:
    """One little-learner tap task (with the answer, for instant feedback)."""
    kind = (kind or "").strip().lower()
    if kind == "phonics":
        letter = random.choice(list(_LETTER_WORDS))
        word, emoji, w1, w2 = _LETTER_WORDS[letter]
        return {
            "kind": "phonics", "emoji": "🔤",
            "prompt": f"Which one starts with the letter {letter}?",
            "display": letter, "options": _mk_options(word, [w1, w2]),
            "answer": _opt_slide(word)["id"],
            "say": (f"{letter}. {letter} says buh or bah. "
                    f"{word} starts with {letter}."),
        }
    if kind == "counting":
        name, emoji = random.choice(_FRUITS)
        n = random.randint(1, 10)
        wrongs = {n + 1, max(1, n - 1), n + 2}
        wrongs.discard(n)
        opts = _mk_options(str(n), [str(w) for w in sorted(wrongs)][:2])
        return {
            "kind": "counting", "emoji": "🔢",
            "prompt": f"Count the {name.lower()}! How many do you see?",
            "display": emoji * n, "options": opts,
            "answer": _opt_slide(str(n))["id"],
            "say": f"Count with me. {n}! There are {n} {name.lower()}.",
        }
    if kind == "shapes":
        name, emoji, sides, fact = random.choice(_SHAPES)
        if random.random() < 0.5:
            others = [s for s, *_ in _SHAPES if s != name]
            return {
                "kind": "shapes", "emoji": "🔶", "prompt": f"Tap the {name}!",
                "display": "", "options": _mk_options(emoji, others[:2]),
                "answer": _opt_slide(emoji)["id"],
                "say": f"Find the {name}. {fact}",
            }
        wrongs = {sides + 1, max(1, sides - 1), sides + 2}
        wrongs.discard(sides)
        return {
            "kind": "shapes", "emoji": "🔶",
            "prompt": f"How many sides does a {name.lower()} have?",
            "display": emoji, "options": _mk_options(
                str(sides), [str(w) for w in sorted(wrongs)][:2]),
            "answer": _opt_slide(str(sides))["id"],
            "say": f"Look carefully. {fact}",
        }
    if kind == "colors":
        color, emoji, wrongs = random.choice(_COLOR_THINGS)
        return {
            "kind": "colors", "emoji": "🌈",
            "prompt": f"Tap the {color} one!",
            "display": "", "options": _mk_options(emoji, wrongs[:2]),
            "answer": _opt_slide(emoji)["id"],
            "say": f"Which one is {color}? Yes! The {color} one!",
        }
    if kind == "rhymes":
        word, rhymes, non = random.choice(_RHYMES)
        right = random.choice(rhymes)
        return {
            "kind": "rhymes", "emoji": "🎵",
            "prompt": f"Which word rhymes with '{word}'?",
            "display": f"🎵 {word}", "options": _mk_options(right, non[:2]),
            "answer": _opt_slide(right)["id"],
            "say": (f"{word}, {word}. Which word sounds the same at the end? "
                    f"{right} rhymes with {word}!"),
        }
    return None


def kinder_round_size() -> int:
    return 5


def make_round() -> list[dict]:
    """One round: a task of every kind, shuffled (5 taps of fun)."""
    tasks = [make_task(k) for k in KINDS]
    tasks = [t for t in tasks if t]
    import random as _r
    _r.shuffle(tasks)
    return tasks


def mark_round(raw: dict, kind: str, correct: int, total: int) -> dict:
    """Finish one kinder round: +points only for the FIRST correct round of
    the day per kind (honest counting, same spirit as practice topics)."""
    import time
    kind = (kind or "").strip().lower()[:20]
    if kind not in KINDS:
        return {"kind": kind, "points_awarded": 0, "points": raw.get("points", 0)}
    done = raw.setdefault("kinder_done", {})
    today = time.strftime("%Y-%m-%d")
    already_today = done.get(kind) == today
    awarded = 0
    if correct >= 1 and not already_today:
        awarded = POINTS_PER_ROUND
        raw["points"] = raw.get("points", 0) + awarded
        done[kind] = today
    return {"kind": kind, "correct": max(0, int(correct)),
            "total": max(0, int(total)), "already_today": already_today,
            "points_awarded": awarded, "points": raw.get("points", 0)}


# ---- tutor context: kindergarten foundations for little learners --------

def kinder_context(question: str) -> str:
    """A compact kinder curriculum excerpt when a little kid asks about
    letters, numbers, shapes, colors or rhymes. Empty for other topics."""
    q = (question or "").lower()

    def has(*words: str) -> bool:
        return any(re.search(r"\b" + re.escape(w) + r"\b", q) for w in words)

    parts: list[str] = []
    if has("letter", "letters", "alphabet", "phonic", "phonics", "sound",
           "sounds", "spell") or re.search(r"\b[a-z]\b", q):
        parts.append("KINDER PHONICS CHART (authoritative):\n" + _LETTER_LINE)
    if has("count", "counting", "number", "numbers", "add", "plus", "one",
           "two", "three", "four", "five", "six", "seven", "eight", "nine",
           "ten", "twenty", "how many"):
        parts.append(
            "KINDER COUNTING (authoritative): counting 1 to 20 — one, two, "
            "three, four, five, six, seven, eight, nine, ten, eleven, twelve, "
            "thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, "
            "nineteen, twenty. Count real things with the child (fingers, "
            "toys, fruits). Adding small numbers = counting on: 3 plus 2 "
            "means start at 3 and count two more: four, five.")
    if has("shape", "shapes", "triangle", "square", "circle", "star",
           "heart", "diamond", "round", "side", "sides", "corner", "corners"):
        parts.append("KINDER SHAPES (authoritative):\n" +
                     "\n".join(f"- {n}: {f}" for n, _e, _s, f in _SHAPES))
    if has("color", "colors", "colour", "colours", "red", "blue", "yellow",
           "green", "orange", "purple", "pink", "black", "white"):
        parts.append(
            "KINDER COLORS (authoritative): the primary colors are red, "
            "yellow and blue. Mix yellow and blue to make green, red and "
            "yellow to make orange, red and blue to make purple. Point at "
            "real things around the child in that color.")
    if has("rhyme", "rhymes", "rhyming", "poem", "poems", "song", "sing",
           "singing"):
        example = random.choice(_RHYMES)
        parts.append(
            f"KINDER RHYMES (authoritative): rhyming words end with the SAME "
            f"sound. Examples: {example[0]} rhymes with "
            f"{', '.join(example[1])}. Sing the pair twice so the child "
            f"hears the ending sound.")
    return "\n\n".join(parts)


def kinder_tone(grade: int) -> str:
    """Extra persona directive for the littlest learners (grades 1-2)."""
    if grade > 2:
        return ""
    return (
        "LITTLE LEARNER MODE (this child is 5 to 7 years old): use the "
        "child's name often and warmly. ONE idea per sentence, max 8 words "
        "per sentence. Everyday words only, spoken aloud clearly. Teach "
        "letters, numbers, shapes, colors and rhymes through play — count "
        "real things, sound out letters, cheer every single try. Repeat key "
        "words once with delight. Never rush, never lecture, no long "
        "explanations.\n")
