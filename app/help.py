"""Help & feedback (launch feature): parents/kids report problems or ask
questions about the app. Stored as JSON records under data/help/ — no
external service, no personal data beyond the profile name."""

from __future__ import annotations
import json, re, time
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "help"

def _safe(pid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "", str(pid))[:40]

def submit(pid: str, name: str, message: str, kind: str = "question") -> dict:
    msg = (message or "").strip()[:2000]
    if len(msg) < 3:
        return {"ok": False, "reason": "Please write a little more."}
    kind = kind if kind in ("question", "complaint", "suggestion") else "question"
    DATA.mkdir(parents=True, exist_ok=True)
    rec = {"id": time.strftime("%Y%m%d-%H%M%S") + "-" + str(int(time.time()*1000))[-4:],
           "pid": _safe(pid), "name": (name or "friend")[:30],
           "kind": kind, "message": msg,
           "ts": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "open"}
    (DATA / (rec["id"] + ".json")).write_text(
        json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"ok": True, "id": rec["id"]}

def list_all(limit: int = 100) -> list[dict]:
    if not DATA.exists():
        return []
    out = []
    for f in sorted(DATA.glob("*.json"), reverse=True)[:limit]:
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass
    return out
