"""Sweeper: enrich every board-knowledge section under 70 words to 85-130
words using the self-checked writer (write -> validate). Resumable via
data/enrich_progress.json. WORKERS=2 (GLM account concurrency limit)."""
import json, re, sys, time, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

env = {}
env_file = Path(r"C:\Users\user\AppData\Local\hermes\.env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
if env.get("GLM_API_KEY"):
    os.environ["GLM_API_KEY"] = env["GLM_API_KEY"]
os.environ.setdefault("GLM_BASE_URL", env.get("GLM_BASE_URL", ""))

from app import knowledge_fresh as kf, llm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BOARDS = ROOT / "knowledge" / "boards"
PROGRESS = ROOT / "data" / "enrich_progress.json"
MIN_W = 70
WORKERS = 2

_state = {"done": []}


def _load():
    if PROGRESS.exists():
        try:
            _state.update(json.loads(PROGRESS.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass


def _save():
    tmp = PROGRESS.with_suffix(".tmp")
    tmp.write_text(json.dumps({"done": _state["done"][-5000:]}), encoding="utf-8")
    tmp.replace(PROGRESS)


def key(path: Path, title: str) -> str:
    return str(path.relative_to(BOARDS)) + "::" + title


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    header = text.split("## ")[0]
    secs = []
    for chunk in text.split("## ")[1:]:
        title = chunk.split("\n")[0].strip()
        body = chunk[len(title):].strip()
        secs.append([title, body])
    return header, secs


def board_subject_grade(path: Path):
    try:
        parts = path.relative_to(BOARDS).parts
        board, subject = parts[0], parts[1]
        grade = int(re.search(r"grade(\d+)_", path.name).group(1))
        return board, subject, grade
    except (IndexError, AttributeError, ValueError):
        return None


def enrich_one(args):
    path, title, body = args
    info = board_subject_grade(path)
    if not info:
        return (path, title, "skip-meta", False)
    board, subject, grade = info
    binfo = kf._boards.BOARDS.get(board, {})
    prompt = (
        f"You write school curriculum summaries for the {binfo.get('name', board)} "
        f"syllabus, {kf.SUBJECT_TITLES.get(subject, subject)}, Grade {grade}. "
        f'Topic: "{title}". The current summary is too short:\n{body}\n\n'
        f"Write an improved version of 4 to 6 sentences (90-140 words) of pure "
        f"factual teaching content: the rules, methods, formulas or concepts, "
        f"with concrete examples. Keep the same country/curriculum flavour. "
        f"Output ONLY the text: no headings, no bullets, no quotes, no meta talk."
    )
    for attempt in range(4):
        text, err = llm.quick(prompt, max_tokens=380, temperature=0.3, timeout=60.0)
        if text:
            cleaned = kf.validate_body(text)
            if cleaned and len(cleaned.split()) >= MIN_W - 5:
                return (path, title, cleaned, True)
        time.sleep(2.5 * (attempt + 1))
    return (path, title, "failed", False)


def main():
    if not llm.is_configured():
        print("no LLM key — abort", flush=True)
        return
    _load()
    done = set(_state["done"])

    jobs = []
    files = sorted(BOARDS.rglob("*.md"))
    for f in files:
        header, secs = parse(f)
        for title, body in secs:
            if len(body.split()) < MIN_W and key(f, title) not in done:
                jobs.append((f, title, body))
    print(f"{len(jobs)} weak sections to enrich", flush=True)
    if not jobs:
        return

    t0 = time.time()
    ok = fail = 0
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, (path, title, new_body, success) in enumerate(
                ex.map(enrich_one, jobs), 1):
            results.append((path, title, new_body, success))
            if success:
                ok += 1
                done.add(key(path, title))
            else:
                fail += 1
            if i % 10 == 0 or i == len(jobs):
                _state["done"] = list(done)
                _save()
                print(f"[{i}/{len(jobs)}] ok={ok} fail={fail} "
                      f"({(time.time()-t0)/60:.1f} min)", flush=True)

    # group new bodies per file and rewrite
    by_file = {}
    for path, title, new_body, success in results:
        if success:
            by_file.setdefault(path, {})[title] = new_body
    for path, new_titles in by_file.items():
        header, secs = parse(path)
        out = [header]
        for title, body in secs:
            body = new_titles.get(title, body)
            out.append(f"## {title}\n{body}\n")
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text("\n".join(out), encoding="utf-8")
        tmp.replace(path)
    print(f"rewrote {len(by_file)} files", flush=True)
    _save()
    print(f"ENRICH-DONE ok={ok} fail={fail}", flush=True)


if __name__ == "__main__":
    main()
