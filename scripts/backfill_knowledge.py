"""One-shot parallel backfill of thin curriculum sections.

Heals every file whose sections are below knowledge_fresh.MIN_WORDS using
the same validate-and-write pipeline as the live self-updating engine.
Safe to re-run: already-good sections are skipped. Progress is written to
data/backfill_progress.json after every file.
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import knowledge_fresh as kf  # noqa: E402

PROGRESS = kf.ROOT / "data" / "backfill_progress.json"
WORKERS = 2


def save_progress(done: list[str]) -> None:
    tmp = PROGRESS.with_suffix(".tmp")
    tmp.write_text(json.dumps(
        {"done": done, "total": len(kf.library_files()),
         "updated": time.strftime("%Y-%m-%dT%H:%M:%S")}),
        encoding="utf-8")
    tmp.replace(PROGRESS)


def main() -> None:
    files = kf.library_files()
    todo = [p for p in files if kf.audit_file(p)["thin"]]
    print(f"{len(todo)} of {len(files)} files need healing", flush=True)
    done: list[str] = []
    fixed_total = 0
    lock_write = None  # GIL-protected list append is fine

    def run(p: Path):
        nonlocal fixed_total
        try:
            r = kf.heal_file(p, max_sections=60)
        except Exception as exc:            # keep going no matter what
            r = {"file": str(p), "fixed": 0, "left": 0, "error": str(exc)}
        done.append(r["file"])
        fixed_total += r.get("fixed", 0)
        if len(done) % 10 == 0 or len(done) == len(todo):
            save_progress(done)
            print(f"[{len(done)}/{len(todo)}] +{fixed_total} sections "
                  f"(last: {r['file']} +{r.get('fixed', 0)})", flush=True)
        return r

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(run, todo))
    save_progress(done)
    after = kf.audit_library()
    print(f"DONE in {(time.time() - t0) / 60:.1f} min — "
          f"library now: {json.dumps(after)}", flush=True)


if __name__ == "__main__":
    main()
