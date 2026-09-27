"""Foundation files healer: expands thin sections of the 3 pre-KG files using
the same self-checked writer as knowledge_fresh (write -> validate -> score).
Safe to re-run: sections >= 60 words are skipped."""
import re, sys, time, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

env = {}
for line in Path(r"C:\Users\user\AppData\Local\hermes\.env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip()
os.environ["GLM_API_KEY"] = env["GLM_API_KEY"]
os.environ.setdefault("GLM_BASE_URL", env.get("GLM_BASE_URL", ""))

from app import knowledge_fresh as kf, llm  # noqa: E402

FILES = [
    ("Foundation Mathematics", "mathematics",
     Path(r"C:\Users\user\Documents\Programming\edusphere\knowledge\mathematics\gradefoundation_math.md")),
    ("Foundation Science", "science",
     Path(r"C:\Users\user\Documents\Programming\edusphere\knowledge\science\gradefoundation_science.md")),
    ("Foundation English", "english",
     Path(r"C:\Users\user\Documents\Programming\edusphere\knowledge\english\gradefoundation_english.md")),
]
MIN_W = 60


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    header = text.split("## ")[0]
    secs = []
    for chunk in text.split("## ")[1:]:
        title = chunk.split("\n")[0].strip()
        body = chunk[len(title):].strip()
        secs.append([title, body])
    return header, secs


def writer(title: str, subject: str) -> str:
    return (
        f"You write pre-kindergarten (age 3-5) teaching notes for {subject}. "
        f'Topic: "{title}". Write 4 to 6 simple sentences (85-130 words) '
        f"describing what tiny children learn and HOW a teacher plays it with "
        f"them: concrete objects, actions, songs, games. Very simple words. "
        f"Output ONLY the text: no headings, no bullets, no quotes."
    )


def process_one(args):
    path, subject, title, body = args
    if len(body.split()) >= MIN_W:
        return (path, title, "skip", 0)
    for attempt in range(4):
        text, err = llm.quick(writer(title, subject), max_tokens=350,
                              temperature=0.3, timeout=60.0)
        if text:
            cleaned = kf.validate_body(text)
            if cleaned:
                return (path, title, cleaned, 1)
        time.sleep(2.0 * (attempt + 1))
    return (path, title, "failed", 0)


def main():
    jobs = []
    for title, subject, path in FILES:
        header, secs = parse(path)
        for title2, body in secs:
            jobs.append((path, subject, title2, body))

    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        for res in ex.map(process_one, jobs):
            results.append(res)
            print(f"  {res[1][:36]:38s} {res[2] if isinstance(res[2], str) else 'ok'}",
                  flush=True)

    # rewrite files with new bodies
    by_file = {}
    for path, title, new_body, _ in results:
        by_file.setdefault(path, {})[title] = new_body
    for _title, _subject, path in FILES:
        if path not in by_file:
            continue
        header, secs = parse(path)
        out = [header]
        for title, body in secs:
            new = by_file[path].get(title, body)
            if isinstance(new, str) and new not in ("skip", "failed"):
                body = new
            out.append(f"## {title}\n{body}\n")
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text("\n".join(out), encoding="utf-8")
        tmp.replace(path)
        print(f"rewrote {path.name}", flush=True)
    print("FOUNDATION-HEAL-DONE", flush=True)


if __name__ == "__main__":
    main()
