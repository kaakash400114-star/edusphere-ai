"""Board / curriculum system (Stage 5 of the rework).

A child's profile carries a BOARD (cbse, icse, matriculation, tn_state,
american, british). The board:

1. sets the ENGLISH standard taught (spelling, terms, exam framing) via
   `english_directive()` — injected into the tutor prompt;
2. selects the knowledge files: `knowledge/<board>/...` overrides the
   default all-India files when they exist, so boards can be fed one at
   a time without touching the other boards.

CBSE ships fully (Stage 5); the remaining boards are fed in Stage 6 —
until a board has files it transparently falls back to the default
curriculum plus its own English standard.
"""
from __future__ import annotations

from . import knowledge

# board id -> display info
BOARDS: dict[str, dict] = {
    "cbse": {"name": "CBSE", "region": "India (NCERT)",
             "english": "indian", "emoji": "🇮🇳"},
    "icse": {"name": "ICSE", "region": "India (CISCE)",
             "english": "british_india", "emoji": "🇮🇳"},
    "matriculation": {"name": "Matriculation", "region": "India",
                      "english": "indian", "emoji": "🇮🇳"},
    "tn_state": {"name": "Tamil Nadu State Board", "region": "India",
                 "english": "indian", "emoji": "🇮🇳"},
    "american": {"name": "American (Common Core)", "region": "USA",
                 "english": "american", "emoji": "🇺🇸"},
    "british": {"name": "British (GCSE)", "region": "UK",
                "english": "british", "emoji": "🇬🇧"},
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
        "ENGLISH STANDARD (British GCSE): Use British spelling and grammar "
        "conventions (colour, organise, maths not math). Use UK examples "
        "(pounds, football, UK places) and GCSE/A-Level terminology and "
        "mark-scheme style phrasing."
    ),
    "american": (
        "ENGLISH STANDARD (American Common Core): Use American spelling and "
        "conventions (color, organize, math not maths). Use US examples "
        "(dollars, baseball, US states) and Common Core terminology and "
        "methods."
    ),
}


def normalize_board(board: str | None) -> str:
    b = (board or "").strip().lower().replace(" ", "_").replace("-", "_")
    return b if b in BOARDS else DEFAULT_BOARD


def board_public() -> list[dict]:
    """Roster for the frontend pickers."""
    return [{"id": bid, "name": b["name"], "region": b["region"],
             "emoji": b["emoji"]} for bid, b in BOARDS.items()]


def board_info(board: str | None) -> dict:
    bid = normalize_board(board)
    return {"id": bid, **BOARDS[bid]}


def english_directive(board: str | None) -> str:
    bid = normalize_board(board)
    return _ENGLISH_DIRECTIVES[BOARDS[bid]["english"]] + "\n"


def board_file_path(subject: str, grade: int) -> object | None:
    """Board-specific knowledge file for subject+grade, if one exists."""
    bid = normalize_board(subject.split("/", 1)[0]) if "/" in subject else None
    return None  # placeholder; real resolution lives in knowledge_path_for


def knowledge_path_for(board: str | None, subject: str, grade: int):
    """Board-aware knowledge file resolution.

    1. knowledge/<board>/<subject dir>/grade<N>_<subject>.md if present
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
