"""Human-like neural voices (edge-tts / Microsoft neural TTS) — Stage 3.

Every buddy has a DISTINCT natural human speaker. Stage 3 adds the human
texture:
- GRADE-SCALED DELIVERY: the same buddy speaks slower with more breath
  pauses for a grade-1 child and at full adult pace with crisp precision
  for a grade-10 child (pace is baked into the synthesized mp3).
- SPOKEN-FORM PREPROCESSING: markdown noise, symbols and abbreviations
  are converted to what a human would actually SAY ("e.g." -> "for
  example", "*" emphasis -> real spoken pauses around the word).
- PAUSE PROFILE per grade band: little kids get gentle... slow... phrasing;
  seniors get flowing, dense speech.

BROWSER FALLBACK: if edge-tts is unavailable or fails (offline), the
frontend keeps its built-in Web Speech synthesis — the app never loses
its voice.
"""
from __future__ import annotations

import asyncio
import hashlib
import os
import re
import tempfile

try:
    import edge_tts
    _HAS_EDGE = True
except ImportError:
    _HAS_EDGE = False

# buddy id -> (neural voice, rate %, pitch adjustment)
# rate/pitch tuned per personality; edge-tts syntax: "+10%", "-20Hz"
BUDDY_VOICES: dict[str, dict] = {
    "leo":    {"voice": "en-US-ChristopherNeural", "rate": "-4%",  "pitch": "-8Hz"},   # warm, brave, steady
    "miko":   {"voice": "en-US-AriaNeural",        "rate": "-12%", "pitch": "-2Hz"},   # soft, dreamy, slow
    "pip":    {"voice": "en-US-AnaNeural",         "rate": "+8%",  "pitch": "+15Hz"},  # bouncy child, giggly
    "chintu": {"voice": "en-US-GuyNeural",         "rate": "-8%",  "pitch": "-15Hz"},  # deep and wise
    "zara":   {"voice": "en-US-JennyNeural",       "rate": "+6%",  "pitch": "+5Hz"},   # quick, teasing
    "toko":   {"voice": "en-GB-SoniaNeural",       "rate": "+4%",  "pitch": "+8Hz"},   # sing-song, chatty
    "kiko":   {"voice": "en-AU-NatashaNeural",     "rate": "0%",   "pitch": "+2Hz"},   # curious, flowing
    "bip":    {"voice": "en-US-EricNeural",        "rate": "-2%",  "pitch": "-4Hz"},   # calm, matter-of-fact
    "dodo":   {"voice": "en-US-AndrewNeural",      "rate": "+10%", "pitch": "+10Hz"},  # loud, goofy energy
    "nova":   {"voice": "en-IN-NeerjaNeural",      "rate": "-4%",  "pitch": "+0Hz"},   # calm, precise
}

# ---- grade-band delivery profiles (Stage 3) -------------------------
# pace multiplies the buddy's base rate (lower = slower, more immature);
# pause inserts breath breaks into the spoken text at this grade band.
GRADE_STYLE: dict[str, dict] = {
    "little":  {"grades": (1, 2),   "pace": 0.80, "max_words_per_breath": 7,
                "style": (
                    "SPEAKING STYLE: tiny sentences (max 8 words). Simplest "
                    "everyday words only. One idea per sentence. Sound happy "
                    "and surprised like a fun grown-up friend. Repeat key "
                    "words once with delight. Pronounce everything clearly "
                    "and slowly.")},
    "young":   {"grades": (3, 5),   "pace": 0.90, "max_words_per_breath": 9,
                "style": (
                    "SPEAKING STYLE: short sentences. Simple words, but the "
                    "real school term is always named and then explained in "
                    "one line. Warm and lively. Pronounce new words slowly "
                    "and clearly, syllable by syllable the first time.")},
    "middle":  {"grades": (6, 8),   "pace": 1.00, "max_words_per_breath": 12,
                "style": (
                    "SPEAKING STYLE: normal flowing sentences. Use the "
                    "correct academic terms with a quick plain-words gloss "
                    "when a term is new. Confident, friendly, never babyish. "
                    "Precise pronunciation of technical words.")},
    "senior":  {"grades": (9, 12),  "pace": 1.08, "max_words_per_breath": 16,
                "style": (
                    "SPEAKING STYLE: mature, precise, exam-aware English. "
                    "Full technical vocabulary, definitions stated exactly, "
                    "no simplification unless asked. Calm, respectful, "
                    "straight to the point — talk like a sharp senior tutor.")},
}


def grade_style(grade: int | None) -> dict:
    g = max(1, min(12, int(grade or 1)))
    for style in GRADE_STYLE.values():
        lo, hi = style["grades"]
        if lo <= g <= hi:
            return style
    return GRADE_STYLE["middle"]


def grade_style_directive(grade: int | None) -> str:
    """Prompt block that matures the buddy's WORDS with the child's grade."""
    return grade_style(grade)["style"] + "\n"


# ---- spoken-form preprocessing --------------------------------------

_SUBS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"e\.g\.,?", re.I), "for example,"),
    (re.compile(r"i\.e\.,?", re.I), "that is,"),
    (re.compile(r"\betc\.?", re.I), "and so on"),
    (re.compile(r"\bvs\.?\b", re.I), "versus"),
    (re.compile(r"\bapprox\.?", re.I), "about"),
    (re.compile(r"&"), " and "),
    (re.compile(r"[*_#`>|]"), " "),          # markdown noise (except kept markers below)
    (re.compile(r"\s*—\s*"), "... "),        # dash -> breath pause
    (re.compile(r"\s*–\s*"), ", "),
    (re.compile(r"(\d+)\s*x\s*(\d+)", re.I), r"\1 times \2"),
    (re.compile(r"(\d+)\s*÷\s*(\d+)"), r"\1 divided by \2"),
    (re.compile(r"(\d+)\s*%\s*"), r"\1 percent "),
]

# *word* markers from the tutor -> real spoken emphasis: short pauses
# on both sides so the important word lands (kept OUT of _SUBS).
_EMPHASIS = re.compile(r"\*([^*\n]{1,24})\*")


def spoken_form(text: str, max_words_per_breath: int = 12) -> str:
    """Convert model text into what a human would actually SAY."""
    text = _EMPHASIS.sub(r" ... \1 ... ", text)      # spoken emphasis first
    for pattern, repl in _SUBS:
        text = pattern.sub(repl, text)
    # long unpunctuated runs get a breath so the reader sounds human
    out_parts = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words = sentence.split()
        if len(words) <= max_words_per_breath:
            out_parts.append(sentence)
            continue
        for i in range(0, len(words), max_words_per_breath):
            chunk = " ".join(words[i:i + max_words_per_breath])
            out_parts.append(chunk + ("," if i + max_words_per_breath < len(words) else ""))
    return re.sub(r"\s{2,}", " ", " ".join(out_parts)).strip()


# ---- rate/pitch math --------------------------------------------------

def _parse_pct(rate: str) -> float:
    try:
        return float(str(rate).replace("%", "").replace("+", ""))
    except ValueError:
        return 0.0


def _fmt_pct(value: float) -> str:
    return f"{value:+.0f}%"


def effective_rate(buddy_cfg: dict, pace: float = 1.0) -> str:
    """Buddy base rate scaled by the grade pace (baked into the mp3)."""
    base = _parse_pct(buddy_cfg["rate"])
    scaled = base + (pace - 1.0) * 100.0      # -20% pace = -20 percentage pts
    # keep inside edge-tts sane range
    return _fmt_pct(max(-50.0, min(50.0, scaled)))


_CACHE_DIR = os.path.join(tempfile.gettempdir(), "edusphere_tts")
os.makedirs(_CACHE_DIR, exist_ok=True)


def _cache_path(text: str, voice_cfg: dict) -> str:
    key = hashlib.sha1(
        (voice_cfg["voice"] + "|" + voice_cfg["rate"] + "|" + voice_cfg["pitch"]
         + "|" + text).encode("utf-8")).hexdigest() + ".mp3"
    return os.path.join(_CACHE_DIR, key)


def _generate(text: str, voice_cfg: dict, out_path: str) -> None:
    async def run():
        com = edge_tts.Communicate(
            text, voice_cfg["voice"],
            rate=voice_cfg["rate"], pitch=voice_cfg["pitch"])
        await com.save(out_path)
    asyncio.run(run())


def synth(buddy_id: str, text: str, pace: float = 1.0) -> str | None:
    """Return path to an mp3 for this text in this buddy's grade-scaled
    voice, or None if edge-tts is unavailable/failed (frontend then falls
    back to Web Speech)."""
    if not _HAS_EDGE or not text.strip():
        return None
    cfg = dict(BUDDY_VOICES.get(buddy_id) or BUDDY_VOICES["leo"])
    cfg["rate"] = effective_rate(cfg, pace)
    spoken = spoken_form(text[:900])
    if not spoken:
        return None
    out = _cache_path(spoken, cfg)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return out
    try:
        _generate(spoken, cfg, out)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            return out
    except Exception:
        pass
    return None


def voice_public(buddy_id: str) -> dict:
    """Neural voice descriptor for the frontend.

    The descriptor IS the neural voice profile (per-buddy Microsoft neural
    speaker + Stage 3 grade-scaled rate). `voice_hints` is kept alongside
    for the browser Web Speech fallback so each buddy still sounds like a
    different person when offline.
    """
    cfg = BUDDY_VOICES.get(buddy_id) or BUDDY_VOICES["leo"]
    return {"engine": "edge", "voice": cfg["voice"],
            "rate": cfg["rate"], "pitch": cfg["pitch"],
            "voice_hints": _browser_hints(buddy_id)}


# browser Web Speech fallback hints (used only when the mp3 can't play)
_BROWSER_HINTS: dict[str, list[str]] = {
    "leo": ["David", "Google UK Male"],
    "miko": ["UK English Male", "David"],
    "pip": ["Zira", "Google US English"],
    "chintu": ["Mark", "David"],
    "zara": ["Google US English", "Zira"],
    "toko": ["UK English Female", "Zira"],
    "kiko": ["Google US English", "Zira"],
    "bip": ["David", "Mark"],
    "dodo": ["Mark", "Google UK Male"],
    "nova": ["Zira", "Google UK Female"],
}


def _browser_hints(buddy_id: str) -> list[str]:
    return list(_BROWSER_HINTS.get(buddy_id, ["David", "Zira"]))
