"""Stage 4 — generate knowledge trees for the new world boards.

For every board that has no own files yet (15 boards x 3 subjects x 12
grades = 540 files) this script writes COMPLETE files in one LLM call per
file: header + >= 6 sections with 60-160-word bodies, localized to the
country's curriculum naming and examples.

Robustness (lessons from the Sep 26 backfill):
  - WORKERS = 3 (parallel LLM batches above that trip GLM 429s)
  - 429/err backoff with retry, resumable via data/worldgen_progress.json
  - validation identical to knowledge_fresh rules (>=5 '## ' sections,
    thin = < MIN_WORDS words); failed files are retried then reported
  - atomic tmp+replace writes; data/ stays gitignored

Run:  EDUSPHERE_NO_AUTOFRESH=1 python scripts/generate_world_boards.py
"""
from __future__ import annotations

import json
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import boards as boards_mod, knowledge as knowledge_mod  # noqa: E402
from app import llm  # noqa: E402
from app.knowledge_fresh import MIN_WORDS, audit_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "knowledge" / "boards"
PROGRESS = ROOT / "data" / "worldgen_progress.json"
WORKERS = 3
FILE_RETRIES = 3

SUBJECTS = (("mathematics", "math", "Mathematics"),
            ("science", "science", "Science"),
            ("english", "english", "English Language Arts"))

# per-country flavour so files are genuinely localized, not renamed CBSE
COUNTRY_FLAVOUR = {
    "cambridge_igcse": "Cambridge International assessment style; 'Stage' naming is NOT used — say Grade; Cambridge IGCSE framing for older grades; international examples",
    "ap": "US College Board AP course framing for grades 9-12 with AP exam terminology; elementary grades follow US Common Core; American examples",
    "ib": "IB PYP/MYP/DP framing: inquiry questions, key concepts, 'learners investigate'; international-mindedness; global examples",
    "australian": "ACARA achievement standards, Australian English spelling (colour, realise), Australian examples (AUD, footy, outback, Great Barrier Reef)",
    "singapore": "Singapore MOE syllabus with Concrete-Pictorial-Abstract approach, model/bar method for word problems, PSLE streaming language for grade 6; Singapore examples (hawker food, MRT, HDB)",
    "canadian": "Provincial Canadian curriculum expectations, Canadian spelling mixing UK/US, Canadian examples (loonies, hockey, provinces, maple, CN Tower)",
    "uae": "UAE Ministry of Education curriculum, British-based English, Gulf-region examples (dirhams, desert climate, souks, Sheikh Zayed Grand Mosque)",
    "south_africa": "South African CAPS curriculum with 'learners are able to' outcome phrasing, South African examples (rand, Proteas, Table Mountain, braai)",
    "nigeria": "Nigerian NERDC curriculum, Nigerian English conventions, Nigerian examples (naira, jollof rice, kola nuts, Lagos, harmattan)",
    "german": "German state curriculum (Lehrplan) taught in English, structured and systematic progression, German examples (euros, Autobahn, Christmas markets, Bundesliga)",
    "french": "French national curriculum (programmes de l'école) taught in English with French terms noted, French examples (euros, boulangerie, Tour de France, métro)",
    "japanese": "Japanese MEXT Course of Study taught in English, precision and mastery emphasis, Japanese examples (yen, bento, shinkansen, hanami)",
    "korean": "South Korean national curriculum taught in English with CSAT awareness for senior grades, Korean examples (won, kimchi, Seoul, hanbok)",
    "finnish": "Finnish FNBE phenomenon-based and transversal-competence framing, Finnish examples (euros, sauna, Northern Lights, Moomins)",
    "new_zealand": "New Zealand Curriculum with NZC levels mentioned alongside the grade, te reo Māori terms welcomed where natural, NZ examples (kiwi, haka, All Blacks, piupiu)",
    "kenya": "Kenyan CBC with competency-based 'the learner is guided to' phrasing, Kenyan examples (shillings, ugali, Nairobi National Park, boda boda)",
}

_lock = threading.Lock()
_progress = {"done": [], "failed": [], "total": 0}


def _load_progress() -> None:
    if PROGRESS.exists():
        try:
            _progress.update(json.loads(PROGRESS.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass


def _save_progress() -> None:
    tmp = PROGRESS.with_suffix(".tmp")
    tmp.write_text(json.dumps(
        {"done": _progress["done"], "failed": _progress["failed"],
         "total": _progress["total"],
         "updated": time.strftime("%Y-%m-%dT%H:%M:%S")}),
        encoding="utf-8")
    tmp.replace(PROGRESS)


def _file_path(board: str, subject: str, grade: int) -> Path:
    pattern = knowledge_mod.FILE_MAP[subject]
    return LIB / board / pattern.format(grade=grade)


def _needs_file(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        audit = audit_text(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return True
    return audit["sections"] < 5 or audit["thin"] > 0


def _prompt(board: str, subject: str, grade: int) -> str:
    info = boards_mod.BOARDS[board]
    flavour = COUNTRY_FLAVOUR.get(board, "")
    if grade <= 0:
        return ""
    band = ("early years, play-based and concrete"
            if grade <= 2 else
            "primary level, concrete with pictures of ideas"
            if grade <= 5 else
            "middle school, more formal definitions appear"
            if grade <= 8 else
            "senior secondary, exam-oriented depth")
    return (
        f"You write school curriculum reference files for EduSphere AI. "
        f"Board: {info['name']} ({info.get('country', '')}). "
        f"Subject: {subject}. Grade: {grade} ({band}).\n"
        f"Country flavour to honour: {flavour}.\n\n"
        f"Write the COMPLETE curriculum file. EXACT format:\n"
        f"Line 1: '# {info['name']} Grade {grade} {subject.title()}'\n"
        f"Then SIX sections. Each section:\n"
        f"'## ' + a topic title actually taught at this grade in this "
        f"curriculum, then a NEW LINE, then 60-130 words of pure factual "
        f"teaching content (what children learn: rules, methods, formulas, "
        f"examples with real numbers or words). Use the country's "
        f"terminology and examples. No meta talk ('this chapter', 'in "
        f"this section'), no markdown besides the # and ## markers.\n"
    )


def _valid_file(text: str) -> bool:
    if not text or not text.lstrip().startswith("#"):
        return False
    audit = audit_text(text)
    return audit["sections"] >= 5 and audit["thin"] == 0


def _write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def generate_one(job: tuple[str, str, int, Path]) -> tuple[str, bool, str]:
    board, subject, grade, path = job
    prompt = _prompt(board, subject, grade)
    if not prompt:
        return (str(path), False, "bad grade")
    for attempt in range(FILE_RETRIES):
        text, err = llm.quick(prompt, max_tokens=1600, temperature=0.3,
                              timeout=120.0)
        if text:
            # strip an accidental fence
            text = re.sub(r"^```[a-z]*\n?|```$", "", text.strip(), flags=re.M)
            if _valid_file(text):
                _write_file(path, text + "\n")
                return (str(path), True, "")
        time.sleep(2.0 * (attempt + 1))          # 429 / invalid backoff
    return (str(path), False, str(err or "invalid output"))


def main() -> None:
    if not llm.is_configured():
        print("No LLM key configured — aborting.", flush=True)
        return
    _load_progress()
    done_set = set(_progress["done"])

    jobs: list[tuple[str, str, int, Path]] = []
    for board in boards_mod.BOARDS:
        if boards_mod.has_own_content(board):
            continue                              # 6 original boards done
        for subject, _, _s in SUBJECTS:
            for grade in range(1, 13):
                path = _file_path(board, subject, grade)
                if str(path) in done_set or not _needs_file(path):
                    continue
                jobs.append((board, subject, grade, path))
    _progress["total"] = len(jobs)
    print(f"{len(jobs)} files to generate across "
          f"{len([b for b in boards_mod.BOARDS if not boards_mod.has_own_content(b)])} boards",
          flush=True)
    if not jobs:
        return

    t0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, (path_str, success, err) in enumerate(
                ex.map(generate_one, jobs), 1):
            with _lock:
                if success:
                    ok += 1
                    _progress["done"].append(path_str)
                    _progress["failed"] = [f for f in _progress["failed"]
                                           if not f.startswith(path_str)]
                else:
                    _progress["failed"].append(f"{path_str} :: {err}")
            if i % 10 == 0 or i == len(jobs):
                _save_progress()
                print(f"[{i}/{len(jobs)}] ok={ok} "
                      f"({(time.time() - t0) / 60:.1f} min)", flush=True)
    _save_progress()
    print(f"DONE: {ok}/{len(jobs)} files generated, "
          f"{len(_progress['failed'])} failed "
          f"in {(time.time() - t0) / 60:.1f} min", flush=True)
    if _progress["failed"]:
        print("FAILED:", *_progress["failed"][:20], sep="\n  ", flush=True)


if __name__ == "__main__":
    main()
