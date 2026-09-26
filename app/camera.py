"""Camera homework helper (Stage 3).

The child photographs a sum or homework page (camera or gallery) and the
buddy READS the problem, then GUIDES the solution step by step — never a
bare answer dump (Khanmigo rule). Photos are kept in an in-app Homework
Album so the work is never lost.

Storage:  data/homework/{pid}/{hid}.jpg   (data/ is gitignored)
Index:    data/homework/{pid}/album.json  (records, newest first)

Endpoints (wired in main.py):
  POST /api/homework/{pid}            {image_b64, mime} -> guidance
  GET  /api/homework/{pid}            album list
  GET  /api/homework/{pid}/{hid}      one record
  GET  /api/homework-photo/{pid}/{fn} the saved image (traversal-safe)

Vision: provider must accept image parts. glm-5.3-flash verified; the
model is overridable via EDUSPHERE_VISION_MODEL.
"""
from __future__ import annotations

import base64
import binascii
import json
import re
import time
from pathlib import Path

from . import characters, language, llm

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "homework"
MAX_PHOTO_BYTES = 6 * 1024 * 1024
ALLOWED_MIME = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MIME_BY_MAGIC = {b"\xff\xd8\xff": "image/jpeg", b"\x89PNG\r\n": "image/png"}

_VISION_MODELS = ["glm-5.3-flash", "glm-4.6v"]


def _album_path(pid: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", str(pid))[:40]
    return DATA_DIR / safe / "album.json"


def _load_album(pid: str) -> list[dict]:
    p = _album_path(pid)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return []


def _save_album(pid: str, records: list[dict]) -> None:
    p = _album_path(pid)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(records[-100:], ensure_ascii=False, indent=1),
                 encoding="utf-8")


def decode_image(image_b64: str, mime: str | None) -> tuple[bytes, str]:
    """Validate + decode an uploaded photo. Raises ValueError on bad input."""
    raw = base64.b64decode(
        re.sub(r"^data:[^;]+;base64,", "", image_b64 or "").strip(),
        validate=False)
    if not raw:
        raise ValueError("empty image")
    if len(raw) > MAX_PHOTO_BYTES:
        raise OverflowError("photo too large")
    # magic bytes win over the declared mime (kids' galleries lie)
    real = None
    for magic, m in MIME_BY_MAGIC.items():
        if raw.startswith(magic):
            real = m
            break
    if real is None and raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
        real = "image/webp"
    if real is None:
        if (mime or "") in ALLOWED_MIME:
            real = mime
        else:
            raise ValueError("not a photo we can read (jpeg/png/webp only)")
    return raw, real


def save_photo(pid: str, raw: bytes, mime: str, note: str = "") -> dict:
    hid = time.strftime("%Y%m%d-%H%M%S") + "-" + str(int(time.time() * 1000))[-4:]
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", str(pid))[:40]
    folder = DATA_DIR / safe
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{hid}{ALLOWED_MIME[mime]}").write_bytes(raw)
    rec = {"id": hid, "ts": time.strftime("%Y-%m-%d %H:%M"),
           "file": f"{hid}{ALLOWED_MIME[mime]}", "mime": mime,
           "note": (note or "")[:200], "answer": ""}
    album = _load_album(pid)
    album.append(rec)
    _save_album(pid, album)
    return rec


def update_answer(pid: str, hid: str, answer: str) -> None:
    album = _load_album(pid)
    for r in album:
        if r["id"] == hid:
            r["answer"] = (answer or "")[:8000]
            break
    _save_album(pid, album)


def _vision_prompt(grade: int, name: str, note: str) -> str:
    band = language.band_for(grade)
    return (
        "You are EduSphere AI, a warm tutor for a child. "
        f"The child is {name}, grade {grade}. "
        "They photographed their homework or sums. "
        "Do this, in order:\n"
        "1. Say what you can read from the photo (read the question aloud "
        "so they know you see it). If the photo is blurry, dark, or cut "
        "off, say that kindly and ask for a closer one.\n"
        "2. Guide the FIRST step only, with a tiny question that helps "
        "them do it themselves. NEVER give the final answer to a sum or "
        "exercise — guide step by step over the conversation.\n"
        "3. Praise them for doing their homework.\n"
        + language.language_directive(grade)
        + ("Everyday words, one idea per sentence, no markdown.\n"
           if band in ("kinder", "little", "young") else
           "Plain text only, no markdown headings.\n")
        + (f"The child adds this note: {note[:200]}\n" if note else "")
    )


def vision_guide(pid: str, grade: int, name: str, character: str,
                 image_b64: str, mime: str | None = None,
                 note: str = "") -> tuple[str, dict]:
    """One homework-photo turn. Returns (guidance_text, meta).

    Never raises: failures come back as kid-friendly text + meta.ok=False.
    """
    meta: dict = {"ok": False, "id": None}
    try:
        raw, real_mime = decode_image(image_b64, mime)
    except OverflowError:
        return ("That photo is very big! Please try a smaller one — "
                "I am sure it is a great sum!"), meta
    except (ValueError, binascii.Error):
        return ("Hmm, I could not open that photo. Try taking it again "
                "with good light, all the way close to the page!"), meta

    rec = save_photo(pid, raw, real_mime, note)
    meta["id"] = rec["id"]
    meta["file"] = rec["file"]

    data_url = f"data:{real_mime};base64," + base64.b64encode(raw).decode()
    message = {"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": data_url}},
        {"type": "text", "text": _vision_prompt(grade, name, note)},
    ]}
    last_err = None
    for model in _VISION_MODELS:
        text, err = llm.complete(
            [message], max_tokens=1200, temperature=0.3, timeout=120.0,
            extra={"model": model})
        if text:
            meta.update({"ok": True, "model": model})
            update_answer(pid, rec["id"], text)
            return text, meta
        last_err = err
    return ("My eyes got sleepy looking at that one — please try again "
            "in a moment! (vision down: " + str(last_err) + ")"), meta


def album(pid: str) -> list[dict]:
    """Newest-first album list (full records; answers included)."""
    return list(reversed(_load_album(pid)))


def photo_path(pid: str, filename: str) -> Path | None:
    """Traversal-safe photo lookup."""
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", str(pid))[:40]
    fname = Path(filename).name
    if not re.fullmatch(r"[A-Za-z0-9._-]+\.(jpg|png|webp)", fname):
        return None
    p = DATA_DIR / safe / fname
    return p if p.exists() else None
