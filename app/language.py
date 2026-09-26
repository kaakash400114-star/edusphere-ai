"""Grade-perfect language layer (Stage 2 of the world-class upgrade).

Every tutor answer is machine-checked against the child's grade band:
  - sentence-length caps   (hard for KG-8, advisory for exam bands)
  - long-word density      (approx syllables via vowel groups)
  - band vocabulary rules  (little kids: everyday words, terms glossed)

Pure functions, no LLM: deterministic, instant, fully test-covered.
  lint(answer, grade)          -> metrics + violations
  criticism(violations, grade) -> one rewrite instruction
  language_directive(grade)    -> hard rules for the system prompt
  band_limits(grade)           -> the numeric contract for a grade

The rewrite path keeps the BETTER of draft vs rewrite (never regress).
"""
from __future__ import annotations

import re

# band -> (lo, hi, limits)  — the numeric language contract per grade band
BANDS: dict[str, tuple[int, int, dict]] = {
    "kinder": (0, 0, {"max_words": 9,   "soft_words": 7,
                      "long_ratio": 0.10, "hard": True}),
    "little": (1, 2, {"max_words": 10,  "soft_words": 8,
                      "long_ratio": 0.12, "hard": True}),
    "young":  (3, 5, {"max_words": 16,  "soft_words": 12,
                      "long_ratio": 0.18, "hard": True}),
    "middle": (6, 8, {"max_words": 26,  "soft_words": 20,
                      "long_ratio": 0.28, "hard": False}),   # soft: >30% of sentences
    "senior": (9, 12, {"max_words": 40, "soft_words": 30,
                       "long_ratio": 0.40, "hard": False}),  # exam answers may run long
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z']+")
_VOWELS = "aeiouy"
# words kids know early even though they look "long" by syllable count
_KNOWN = {
    "alligator", "crocodile", "elephant", "butterfly", "sometimes",
    "birthday", "understand", "remember", "favorite", "favourite",
    "beautiful", "different", "alphabet", "children", "together",
    "yesterday", "everyday", "family", "animals", "another", "because",
}


def band_for(grade: int) -> str:
    g = max(0, min(12, int(grade or 0)))
    for name, (lo, hi, _lim) in BANDS.items():
        if lo <= g <= hi:
            return name
    return "middle"


def band_limits(grade: int) -> dict:
    g = max(0, min(12, int(grade or 0)))
    for _name, (lo, hi, lim) in BANDS.items():
        if lo <= g <= hi:
            return dict(lim)
    return dict(BANDS["middle"][2])


def _syllables(word: str) -> int:
    w = word.lower().strip("'")
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)


def sentences(text: str) -> list[list[str]]:
    """Sentences as word lists (markdown noise stripped, code skipped)."""
    clean = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    clean = re.sub(r"[#*_>|`]", " ", clean)
    out = []
    for s in _SENT_SPLIT.split(clean):
        words = _WORD.findall(s)
        if words:
            out.append(words)
    return out


def _long_word_ratio(all_words: list[str]) -> float:
    if not all_words:
        return 0.0
    long = sum(
        1 for w in all_words
        if w.lower() not in _KNOWN and not w.isdigit()
        and _syllables(w) >= 3
    )
    return long / len(all_words)


def lint(answer: str, grade: int) -> dict:
    """Machine-check one answer against the grade's language contract."""
    lim = band_limits(grade)
    sents = sentences(answer)
    lens = [len(s) for s in sents]
    ratio = _long_word_ratio([w for s in sents for w in s])
    metrics = {
        "sentences": len(sents),
        "avg_words": round(sum(lens) / len(lens), 1) if lens else 0.0,
        "max_words": max(lens) if lens else 0,
        "long_ratio": round(ratio, 3),
        "band": band_for(grade),
    }
    violations: list[str] = []

    over = [n for n in lens if n > lim["max_words"]]
    if lim["hard"]:
        if over:
            violations.append(
                f"{len(over)} sentence(s) exceed the {lim['max_words']}-word "
                f"cap (longest {max(over)} words)")
    else:
        frac = (len(over) / len(lens)) if lens else 0.0
        if frac > 0.30:
            violations.append(
                f"{int(frac * 100)}% of sentences exceed {lim['max_words']} "
                "words — too dense for this grade")

    if ratio > lim["long_ratio"]:
        violations.append(
            f"long-word density {metrics['long_ratio']} above the "
            f"{lim['long_ratio']} limit for grade {grade}")
    return {"ok": not violations, "violations": violations,
            "metrics": metrics}


def criticism(violations: list[str], grade: int) -> str:
    """One concrete rewrite instruction from the lint findings."""
    if not violations:
        return ""
    name = {"kinder": "5-year-old in kindergarten", "little": "6-7 year old",
            "young": "primary school child", "middle": "middle schooler",
            "senior": "senior student"}[band_for(grade)]
    return ("Language too hard for a " + name + " (grade "
            + str(grade) + "): " + "; ".join(violations[:2])
            + ". Rewrite with shorter sentences and simpler everyday "
              "words — keep the meaning, warmth, and character. "
              "Output ONLY the new reply in character: never mention "
              "these instructions, rewriting, or sentence rules.")


def language_directive(grade: int) -> str:
    """Hard language rules for the system prompt (band-specific)."""
    lim = band_limits(grade)
    band = band_for(grade)
    base = (f"LANGUAGE CONTRACT (checked by machine — violations force a "
            f"rewrite): every sentence MUST be {lim['max_words']} words or "
            f"fewer (aim for {lim['soft_words']}). ")
    if band in ("kinder", "little"):
        return (base
                + "Use ONLY everyday words a small child knows. Every school "
                  "word (like 'add' or 'rhyme') must be shown with a thing "
                  "they can see or touch. No clauses with 'however', "
                  "'therefore', or 'although'. One idea per sentence.\n")
    if band == "young":
        return (base
                + "Simple words; when a real school term appears, name it "
                  "then explain it in one short line. No long clauses.\n")
    if band == "middle":
        return (base
                + "Correct academic terms with a quick plain-words gloss on "
                  "first use. Keep sentences readable.\n")
    return ("LANGUAGE: precise, exam-aware English; define technical terms "
            "exactly. Long analytic sentences are fine when they carry "
            "reasoning.\n")
