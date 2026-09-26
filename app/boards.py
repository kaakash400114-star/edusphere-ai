"""Board / curriculum system — World Edition.

EduSphere supports curricula from around the world. Each board:
  1. Sets the ENGLISH standard (spelling, terms, exam framing) injected into the tutor prompt.
  2. Selects the knowledge files: knowledge/boards/<board>/... when present,
     falling back to the global base curriculum otherwise.

Boards ship knowledge files progressively — the self-updating engine heals
any thin sections automatically. Until a board has its own files it uses
the global CBSE-aligned base plus its own English/regional standard.
"""
from __future__ import annotations

from . import knowledge

# board id → display info + English standard + region flag
BOARDS: dict[str, dict] = {
    # ── India ──────────────────────────────────────────────────────────────
    "cbse": {
        "name": "CBSE", "region": "India (NCERT)", "country": "India",
        "english": "indian", "emoji": "🇮🇳",
        "description": "Central Board of Secondary Education — NCERT textbooks.",
    },
    "icse": {
        "name": "ICSE", "region": "India (CISCE)", "country": "India",
        "english": "british_india", "emoji": "🇮🇳",
        "description": "Indian Certificate of Secondary Education — CISCE board.",
    },
    "matriculation": {
        "name": "Matriculation", "region": "India", "country": "India",
        "english": "indian", "emoji": "🇮🇳",
        "description": "State Matriculation boards across India.",
    },
    "tn_state": {
        "name": "Tamil Nadu State Board", "region": "India (Tamil Nadu)", "country": "India",
        "english": "indian", "emoji": "🇮🇳",
        "description": "Tamil Nadu State Board of School Examination.",
    },
    # ── UK & International British ──────────────────────────────────────────
    "british": {
        "name": "British (GCSE / A-Level)", "region": "UK", "country": "United Kingdom",
        "english": "british", "emoji": "🇬🇧",
        "description": "UK national curriculum — GCSE and A-Level examinations.",
    },
    "cambridge_igcse": {
        "name": "Cambridge IGCSE", "region": "International", "country": "International",
        "english": "british", "emoji": "🌐",
        "description": "Cambridge Assessment International Education — IGCSE and A-Level.",
    },
    # ── USA ────────────────────────────────────────────────────────────────
    "american": {
        "name": "American (Common Core)", "region": "USA", "country": "United States",
        "english": "american", "emoji": "🇺🇸",
        "description": "US Common Core State Standards (CCSS) curriculum.",
    },
    "ap": {
        "name": "Advanced Placement (AP)", "region": "USA", "country": "United States",
        "english": "american", "emoji": "🇺🇸",
        "description": "College Board Advanced Placement courses for high school.",
    },
    # ── International Baccalaureate ────────────────────────────────────────
    "ib": {
        "name": "International Baccalaureate (IB)", "region": "International", "country": "International",
        "english": "british", "emoji": "🌐",
        "description": "IB Primary Years, Middle Years, and Diploma programmes.",
    },
    # ── Australia ──────────────────────────────────────────────────────────
    "australian": {
        "name": "Australian Curriculum (ACARA)", "region": "Australia", "country": "Australia",
        "english": "australian", "emoji": "🇦🇺",
        "description": "Australian Curriculum, Assessment and Reporting Authority.",
    },
    # ── Singapore ──────────────────────────────────────────────────────────
    "singapore": {
        "name": "Singapore Curriculum (MOE)", "region": "Singapore", "country": "Singapore",
        "english": "british", "emoji": "🇸🇬",
        "description": "Singapore Ministry of Education PSLE/O-Level/A-Level curriculum.",
    },
    # ── Canada ─────────────────────────────────────────────────────────────
    "canadian": {
        "name": "Canadian Curriculum", "region": "Canada", "country": "Canada",
        "english": "canadian", "emoji": "🇨🇦",
        "description": "Provincial curricula across Canada (Ontario, BC, Alberta, etc.).",
    },
    # ── UAE / Gulf ─────────────────────────────────────────────────────────
    "uae": {
        "name": "UAE Curriculum (MOE)", "region": "UAE", "country": "United Arab Emirates",
        "english": "british", "emoji": "🇦🇪",
        "description": "UAE Ministry of Education national curriculum.",
    },
    # ── South Africa ───────────────────────────────────────────────────────
    "south_africa": {
        "name": "South African (CAPS)", "region": "South Africa", "country": "South Africa",
        "english": "british", "emoji": "🇿🇦",
        "description": "Curriculum and Assessment Policy Statement (CAPS).",
    },
    # ── Nigeria ────────────────────────────────────────────────────────────
    "nigeria": {
        "name": "Nigerian (NERDC)", "region": "Nigeria", "country": "Nigeria",
        "english": "british", "emoji": "🇳🇬",
        "description": "Nigerian Educational Research and Development Council curriculum.",
    },
    # ── Germany ────────────────────────────────────────────────────────────
    "german": {
        "name": "German (Lehrplan)", "region": "Germany", "country": "Germany",
        "english": "british", "emoji": "🇩🇪",
        "description": "German state curricula (Lehrplan) — Grundschule to Gymnasium.",
    },
    # ── France ─────────────────────────────────────────────────────────────
    "french": {
        "name": "French (Éducation nationale)", "region": "France", "country": "France",
        "english": "british", "emoji": "🇫🇷",
        "description": "French national curriculum — Maternelle to Terminale/Bac.",
    },
    # ── Japan ──────────────────────────────────────────────────────────────
    "japanese": {
        "name": "Japanese (MEXT)", "region": "Japan", "country": "Japan",
        "english": "american", "emoji": "🇯🇵",
        "description": "Japanese Ministry of Education, Culture, Sports, Science and Technology.",
    },
    # ── South Korea ────────────────────────────────────────────────────────
    "korean": {
        "name": "South Korean (NCCE)", "region": "South Korea", "country": "South Korea",
        "english": "american", "emoji": "🇰🇷",
        "description": "Korean National Curriculum — Grade 1-12 with CSAT focus.",
    },
    # ── Finland ────────────────────────────────────────────────────────────
    "finnish": {
        "name": "Finnish (FNBE)", "region": "Finland", "country": "Finland",
        "english": "british", "emoji": "🇫🇮",
        "description": "Finnish National Board of Education — phenomenon-based curriculum.",
    },
    # ── New Zealand ────────────────────────────────────────────────────────
    "new_zealand": {
        "name": "New Zealand Curriculum (NZC)", "region": "New Zealand", "country": "New Zealand",
        "english": "british", "emoji": "🇳🇿",
        "description": "New Zealand Ministry of Education — NZC with NCEA assessments.",
    },
    # ── Kenya ──────────────────────────────────────────────────────────────
    "kenya": {
        "name": "Kenyan CBC", "region": "Kenya", "country": "Kenya",
        "english": "british", "emoji": "🇰🇪",
        "description": "Kenya Competency Based Curriculum (CBC) — KICD framework.",
    },
}

DEFAULT_BOARD = "cbse"

# English-standard prompt blocks per board family
_ENGLISH_DIRECTIVES: dict[str, str] = {
    "indian": (
        "ENGLISH STANDARD (Indian curriculum): Use Indian textbook spellings "
        "and conventions — British-based spelling (colour, realise, centre) "
        "with Indian curriculum terms (standard, marks, summative assessment). "
        "Use Indian-context examples (rupees, mangoes, monsoon, cricket) that "
        "fit the concept. Follow NCERT terminology and methods exactly when "
        "the excerpt comes from an NCERT-based file."
    ),
    "british_india": (
        "ENGLISH STANDARD (ICSE): Use British spelling (colour, realise, "
        "centre) and ICSE's slightly richer English register. Prefer ICSE "
        "terminology where it differs from NCERT, and India-context examples."
    ),
    "british": (
        "ENGLISH STANDARD (British): Use British spelling and grammar "
        "conventions (colour, organise, maths not math). Use UK/Commonwealth "
        "examples (pounds, football, local geography) and the board's "
        "mark-scheme terminology (e.g. GCSE, A-Level, IGCSE)."
    ),
    "american": (
        "ENGLISH STANDARD (American): Use American spelling and conventions "
        "(color, organize, math not maths). Use US examples (dollars, "
        "baseball, US states, Common Core or AP terminology and methods)."
    ),
    "australian": (
        "ENGLISH STANDARD (Australian): Use Australian English spelling "
        "(colour, organise, maths). Use Australian examples (AUD, cricket, "
        "AFL, Australian geography) and ACARA curriculum language."
    ),
    "canadian": (
        "ENGLISH STANDARD (Canadian): Use Canadian English spelling (colour, "
        "organise). Reference Canadian provinces, dollars, hockey, and "
        "provincial curriculum expectations. Mix American and British conventions "
        "naturally, as Canadians do."
    ),
}


def normalize_board(board: str | None) -> str:
    b = (board or "").strip().lower().replace(" ", "_").replace("-", "_")
    return b if b in BOARDS else DEFAULT_BOARD


def board_public() -> list[dict]:
    """Roster for the frontend pickers — grouped by country."""
    return [{"id": bid, "name": b["name"], "region": b["region"],
             "country": b.get("country", ""), "emoji": b["emoji"],
             "description": b.get("description", "")}
            for bid, b in BOARDS.items()]


def board_info(board: str | None) -> dict:
    bid = normalize_board(board)
    return {"id": bid, **BOARDS[bid]}


def english_directive(board: str | None) -> str:
    bid = normalize_board(board)
    english = BOARDS[bid]["english"]
    return _ENGLISH_DIRECTIVES.get(english, _ENGLISH_DIRECTIVES["indian"]) + "\n"


def board_file_path(subject: str, grade: int) -> object | None:
    """Board-specific knowledge file for subject+grade, if one exists."""
    bid = normalize_board(subject.split("/", 1)[0]) if "/" in subject else None
    return None  # placeholder; real resolution lives in knowledge_path_for


def knowledge_path_for(board: str | None, subject: str, grade: int):
    """Board-aware knowledge file resolution.

    1. knowledge/boards/<board>/<subject dir>/grade<N>_<subject>.md if present
    2. else the default file (all-India CBSE-aligned base content)
    """
    bid = normalize_board(board)
    subject = knowledge.normalize_subject(subject)
    pattern = knowledge.FILE_MAP[subject]
    board_path = knowledge.KNOWLEDGE_DIR / "boards" / bid / pattern.format(grade=grade)
    if board_path.exists():
        return board_path
    return knowledge.knowledge_path(subject, grade)


def has_own_content(board: str | None) -> bool:
    """True once a board has at least one of its own knowledge files."""
    bid = normalize_board(board)
    return (knowledge.KNOWLEDGE_DIR / "boards" / bid).exists()
