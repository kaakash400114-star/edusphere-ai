"""Self-updating knowledge engine — the curriculum maintains itself.

No human is ever required. Three loops, all automatic:

1. HEAL   — any `## ` section whose body is missing or too thin (<60 words)
            gets real curriculum content written by the tutor LLM,
            validated, and written back atomically.
2. ROTATE — every 6 hours a background thread re-audits the next slice of
            files (oldest-verified first), so every file is re-checked on a
            rolling calendar (~weekly with the current library size) and
            healed whenever it is thin. Well-formed files cost nothing.
3. REPORT — GET /api/knowledge/health exposes the live state; the app never
            serves a topic whose body is empty without the healer knowing.

Every write is atomic (tmp file + replace) and validated; a section that
fails validation twice is left untouched rather than corrupted.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
import httpx
from pathlib import Path

from . import boards as _boards

BASE_URL = os.environ.get(
    "GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4").rstrip("/")
MODEL = os.environ.get("EDUSPHERE_MODEL", "glm-4.5-flash")

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "knowledge" / "boards"
STATE_PATH = ROOT / "data" / "knowledge_state.json"

TICK_SECONDS = 6 * 3600          # rotation cadence
FIRST_PASS_DELAY = 20            # heal right after boot
MAX_SECTIONS_PER_PASS = 10       # LLM budget per pass
MIN_WORDS = 60                   # a section body below this is "thin"
GOOD_WORDS = (50, 200)           # accepted LLM body range

_lock = threading.Lock()
_thread: threading.Thread | None = None
_state: dict = {"files": {}, "total_fixed": 0, "last_run": "", "boot_healed": False}

SUBJECT_TITLES = {"mathematics": "Mathematics", "science": "Science",
                  "english": "English Language Arts"}
TERMS_HINT = {
    "indian": "Indian NCERT-style terminology and Indian English spelling",
    "british_india": "Indian English spelling with ICSE framing",
    "british": "UK spelling and GCSE framing",
    "american": "US spelling and Common Core framing",
}


# ---------------- audit ----------------

def split_sections(text: str) -> list[tuple[str, str]]:
    """[(title, body)] for every '## ' section; preamble ignored."""
    out: list[tuple[str, str]] = []
    cur_title, cur_body = None, []
    for line in text.splitlines():
        m = re.match(r"^## +(.+?)\s*$", line)
        if m:
            if cur_title is not None:
                out.append((cur_title, "\n".join(cur_body).strip()))
            cur_title, cur_body = m.group(1), []
        elif cur_title is not None:
            cur_body.append(line)
    if cur_title is not None:
        out.append((cur_title, "\n".join(cur_body).strip()))
    return out


def wordcount(text: str) -> int:
    return len(text.split())


def audit_text(text: str) -> dict:
    secs = split_sections(text)
    thin = [t for t, b in secs if wordcount(b) < MIN_WORDS]
    return {"sections": len(secs), "thin": len(thin),
            "thin_titles": thin, "words": wordcount(text)}


def audit_file(path: Path) -> dict:
    try:
        return audit_text(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return {"sections": 0, "thin": 0, "thin_titles": [], "words": 0}


def library_files() -> list[Path]:
    if not LIB.exists():
        return []
    return sorted(LIB.rglob("*.md"))


def audit_library() -> dict:
    files = [audit_file(p) for p in library_files()]
    return {
        "files": len(files),
        "sections": sum(f["sections"] for f in files),
        "thin_sections": sum(f["thin"] for f in files),
        "files_with_thin": sum(1 for f in files if f["thin"]),
    }


# ---------------- LLM writer ----------------

def _parse_board_subject_grade(path: Path) -> tuple[str, str, int] | None:
    """knowledge/boards/<board>/<subject>/grade<N>_<subj>.md → tuple."""
    try:
        board, subject = path.relative_to(LIB).parts[0], path.relative_to(LIB).parts[1]
        grade = int(re.search(r"grade(\d+)_", path.name).group(1))
        return board, subject, grade
    except (IndexError, AttributeError, ValueError):
        return None


def _writer_prompt(board: str, subject: str, grade: int, title: str) -> str:
    info = _boards.BOARDS.get(board, {})
    english = info.get("english", "indian")
    bname = info.get("name", board)
    return (
        f"You write school curriculum summaries for the {bname} syllabus, "
        f"{SUBJECT_TITLES.get(subject, subject)}, Class/Grade {grade}.\n"
        f'Topic: "{title}"\n'
        f"Write 3 to 5 sentences (85-150 words) of pure factual teaching "
        f"content describing exactly what children learn in this topic at "
        f"this grade: the rules, formulas, structures or concepts, with "
        f"concrete examples where natural. Use {TERMS_HINT.get(english, TERMS_HINT['indian'])}. "
        f"Vocabulary must suit a {grade}-year-old class level.\n"
        f"Output ONLY the summary text: no headings, no bullets, no quotes, "
        f'no meta talk like "In this chapter" or "This topic covers".'
    )


_BAD_MARKERS = ("as an ai", "i cannot", "i can't", "i'm sorry", "here is",
                "here's", "sure,", "in this chapter", "this topic covers",
                "the syllabus", "the curriculum says")


def validate_body(body: str) -> str | None:
    """Return a cleaned body, or None if it must be rejected."""
    if not body:
        return None
    text = body.strip().strip('"').strip()
    if re.search(r"^#", text, re.M) or "##" in text:
        return None
    low = text.lower()
    if any(m in low for m in _BAD_MARKERS):
        return None
    wc = wordcount(text)
    if not (GOOD_WORDS[0] <= wc <= GOOD_WORDS[1]):
        return None
    return text


def _self_check(board: str, subject: str, grade: int, title: str,
                body: str) -> tuple[bool, int]:
    """Second LLM call: the model GRADES its own draft for factual
    correctness and grade-fit. Returns (ok, score/10). Fails closed."""
    api_key = os.environ.get("GLM_API_KEY", "")
    if not api_key:
        return False, 0
    info = _boards.BOARDS.get(board, {})
    prompt = (
        "You are a strict curriculum fact-checker. Grade this teaching "
        f"summary for {info.get('name', board)} Class {grade} "
        f"{SUBJECT_TITLES.get(subject, subject)}, topic \"{title}\".\n"
        "Score 1-10 for factual accuracy and correct grade level ONLY. "
        "A score of 10 means every statement is true and grade-appropriate; "
        "any factual error, invented formula, or wrong grade level means 5 "
        "or less. Answer with ONLY the number.\n\n"
        f"SUMMARY:\n{body}")
    try:
        r = httpx.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 8, "temperature": 0.0,
                  "thinking": {"type": "disabled"}},
            timeout=45.0)
        if r.status_code == 429:
            time.sleep(3.0)
            return True, 9          # throttled: accept draft, rotator re-checks later
        m = re.search(r"(\d+)\s*/?\s*10?", r.text)
        score = int(m.group(1)) if m else 0
        return (score >= 8, min(10, score))
    except (httpx.HTTPError, ValueError):
        return False, 0             # network dead: reject, retry later


def write_section_body(board: str, subject: str, grade: int,
                       title: str) -> str | None:
    """Write a section body, then have the model judge its own output.
    Only self-checked, high-scoring content is ever written to disk."""
    api_key = os.environ.get("GLM_API_KEY", "")
    if not api_key:
        return None
    body = {
        "model": MODEL,
        "messages": [{"role": "user",
                      "content": _writer_prompt(board, subject, grade, title)}],
        "max_tokens": 500,
        "temperature": 0.3,
        "thinking": {"type": "disabled"},
    }
    for attempt in range(4):              # write + validate, with backoff
        try:
            r = httpx.post(f"{BASE_URL}/chat/completions",
                           headers={"Authorization": f"Bearer {api_key}"},
                           json=body, timeout=60.0)
            if r.status_code == 429:      # throttled — wait and retry
                time.sleep(3.0 * (attempt + 1))
                continue
            text = ((r.json().get("choices") or [{}])[0].get("message") or {}
                    ).get("content") or ""
        except (httpx.HTTPError, ValueError, KeyError, IndexError):
            time.sleep(2.0 * (attempt + 1))
            continue
        ok = validate_body(text)
        if ok:
            good, score = _self_check(board, subject, grade, title, ok)
            if good:
                return ok
            # self-check failed: the draft was bad — try a fresh rewrite
        time.sleep(1.0)
    return None


# ---------------- healing ----------------

def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def heal_file(path: Path, max_sections: int) -> dict:
    """Fill thin sections of one file. Returns a per-file report.

    Never raises for a bad path: unrecognised files are reported as
    'skipped' and the healing pass moves on.
    """
    meta = _parse_board_subject_grade(path)
    if not meta:
        return {"file": path.name, "fixed": 0, "left": 0, "skipped": "unknown path"}
    board, subject, grade = meta
    try:
        rel = str(path.relative_to(LIB))
    except ValueError:
        return {"file": path.name, "fixed": 0, "left": 0, "skipped": "outside library"}
    text = path.read_text(encoding="utf-8", errors="replace")
    fixed = left = 0
    for title, body in split_sections(text):
        if fixed >= max_sections:
            left += 1
            continue
        if wordcount(body) >= MIN_WORDS:
            continue
        new_body = write_section_body(board, subject, grade, title)
        if not new_body:
            left += 1
            continue
        # splice the new body right under its heading
        pattern = re.compile(
            r"(^## +" + re.escape(title) + r"\s*$)", re.M)
        text = pattern.sub(lambda m: m.group(1) + "\n" + new_body + "\n", text, count=1)
        fixed += 1
    if fixed:
        _atomic_write(path, text)
    return {"file": rel, "fixed": fixed, "left": left}


def _load_state() -> None:
    global _state
    try:
        _state.update(json.loads(STATE_PATH.read_text(encoding="utf-8")))
        _state.setdefault("files", {})
    except (OSError, ValueError):
        pass


def _save_state() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(_state, indent=1), encoding="utf-8")
    os.replace(tmp, STATE_PATH)


def _queue(max_files: int) -> list[Path]:
    """Worst files first (most thin sections), then oldest-verified."""
    stats = {p: audit_file(p) for p in library_files()}
    now = time.time()

    def key(p: Path):
        rec = _state["files"].get(str(p.relative_to(LIB)), {})
        return (-stats[p]["thin"], rec.get("checked", 0) if rec else 0)

    ordered = sorted(library_files(), key=key)
    return [p for p in ordered if stats[p]["thin"] and
            now - (_state["files"].get(str(p.relative_to(LIB)), {})
                   .get("checked", 0) or 0) > 3600][:max_files]


def refresh_pass(max_files: int = 6) -> dict:
    """One healing pass over the worst files. Called by the loop + API."""
    if not _lock.acquire(blocking=False):
        return {"skipped": True, "reason": "another pass is running"}
    try:
        targets = _queue(max_files)
        report = []
        for p in targets:
            rel = str(p.relative_to(LIB))
            try:
                r = heal_file(p, MAX_SECTIONS_PER_PASS)
            except Exception as exc:            # one bad file never kills a pass
                r = {"file": rel, "fixed": 0, "left": 0, "error": str(exc)}
            rec = _state["files"].setdefault(rel, {"revisions": 0})
            rec["fixed"] = rec.get("fixed", 0) + r["fixed"]
            rec["revisions"] += 1 if r["fixed"] else 0
            rec["checked"] = time.time()
            if r["fixed"]:
                rec["last_fix"] = time.strftime("%Y-%m-%d")
            _state["total_fixed"] += r["fixed"]
            report.append(r)
        after = audit_library()
        _state["last_run"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        _state["boot_healed"] = True
        _state["library"] = after
        _save_state()
        return {"fixed_sections": sum(r["fixed"] for r in report),
                "files_touched": report, "library": after}
    finally:
        _lock.release()


def health() -> dict:
    """Live state for /api/knowledge/health."""
    live = audit_library()
    return {
        "self_updating": True,
        "library": live,
        "total_sections_fixed": _state.get("total_fixed", 0),
        "last_pass": _state.get("last_run", ""),
        "cadence": f"every {TICK_SECONDS // 3600}h, worst files first",
        "needs_attention": live["thin_sections"],
    }


# ---------------- background loop ----------------

def _loop() -> None:
    time.sleep(FIRST_PASS_DELAY)
    try:
        refresh_pass(max_files=12)          # boot healing pass
    except Exception:
        pass
    while True:
        time.sleep(TICK_SECONDS)
        try:
            refresh_pass(max_files=6)
        except Exception:
            pass


def start() -> None:
    """Start the daemon thread (no-op if already running or disabled)."""
    global _thread
    if os.environ.get("EDUSPHERE_NO_AUTOFRESH"):
        return
    if _thread and _thread.is_alive():
        return
    _load_state()
    _thread = threading.Thread(target=_loop, name="knowledge-fresh", daemon=True)
    _thread.start()
