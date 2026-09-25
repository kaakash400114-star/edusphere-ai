"""Kid profiles with parent consent, stars, streaks, weak areas.

Minimal data by design (COPPA/GDPR-K mindset): first name, grade,
consent flag + timestamp. Everything else is learning progress only.
Storage: one JSON file per kid under data/profiles/.
"""
from __future__ import annotations

import json
import secrets
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROFILES_DIR = DATA_DIR / "profiles"

MAX_NAME_LEN = 20


def _safe_pid(pid: str) -> str:
    ok = all(c.isalnum() or c == "-" for c in pid) and len(pid) <= 40
    if not ok:
        raise ValueError("bad profile id")
    return pid


def _path(pid: str) -> Path:
    return PROFILES_DIR / f"{_safe_pid(pid)}.json"


def create_profile(name: str, grade: int, parent_pin: str,
                   character: str = "auto") -> dict:
    name = name.strip()[:MAX_NAME_LEN]
    grade = int(grade or 1)
    if not name or not (1 <= grade <= 12):
        raise ValueError("need a name and grade 1-12")
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    pid = f"{name.lower()}-{secrets.token_hex(3)}"
    profile = {
        "pid": pid,
        "name": name,
        "grade": grade,
        "character": character,
        "parent_pin_hash": _hash_pin(parent_pin),
        "parent_consent": True,
        "consent_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stars": 0,
        "streak": {"count": 0, "last_day": ""},
        "weak_areas": {},   # topic -> miss count
        "strong_areas": {},  # topic -> hit count
        "topics_covered": [],
        "memories": [],      # stage 2: life details the buddy remembers
        "stickers": {},      # stage 6: sticker album  sticker-id -> count
        "log": [],           # last N activity entries (capped)
    }
    _path(pid).write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return _public(profile)


def get_profile(pid: str) -> dict | None:
    p = _path(pid)
    if not p.exists():
        return None
    return _public(json.loads(p.read_text(encoding="utf-8")))


def check_pin(pid: str, pin: str) -> bool:
    p = _path(pid)
    if not p.exists():
        return False
    raw = json.loads(p.read_text(encoding="utf-8"))
    return secrets.compare_digest(raw.get("parent_pin_hash", ""), _hash_pin(pin))


def update_profile(pid: str, **changes) -> dict | None:
    p = _path(pid)
    if not p.exists():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    for key in ("grade", "character"):
        if key in changes and changes[key] is not None:
            raw[key] = changes[key]
    if "accessory" in changes and changes["accessory"] is not None:
        item = changes["accessory"]
        if item and item not in raw.get("wardrobe", []):
            raise ValueError("accessory not owned")
        raw["accessory"] = item
    raw["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    p.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return _public(raw)


def buy_item(pid: str, item: str, cost: int) -> dict:
    """Buy a wardrobe item with stars. Raises ValueError on bad buys."""
    p = _path(pid)
    if not p.exists():
        raise ValueError("profile not found")
    raw = json.loads(p.read_text(encoding="utf-8"))
    wardrobe = raw.setdefault("wardrobe", [])
    if item in wardrobe:
        raise ValueError("already owned")
    if raw.get("stars", 0) < cost:
        raise ValueError("not enough stars")
    raw["stars"] -= cost
    wardrobe.append(item)
    p.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return _public(raw)


def remember(pid: str, text: str) -> dict | None:
    """Stage 2: the buddy remembers a life detail across days."""
    p = _path(pid)
    if not p.exists():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    text = (text or "").strip()[:120]
    if not text:
        return _public(raw)
    mem = raw.setdefault("memories", [])
    if text not in mem:
        mem.append(text)
        raw["memories"] = mem[-10:]  # keep the last 10
    p.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return _public(raw)


def award_sticker(pid: str, sticker_id: str) -> dict | None:
    """Stage 6: drop a sticker into the child's album."""
    p = _path(pid)
    if not p.exists():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    stickers = raw.setdefault("stickers", {})
    stickers[sticker_id] = stickers.get(sticker_id, 0) + 1
    p.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return _public(raw)


def record_activity(pid: str, kind: str, topic: str = "", correct: bool | None = None,
                    stars: int = 0) -> dict | None:
    """Log one learning event: chat topic, quiz answer, game result."""
    p = _path(pid)
    if not p.exists():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    topic = (topic or "").strip()[:80]
    if topic and topic not in raw["topics_covered"]:
        raw["topics_covered"].append(topic)
        raw["topics_covered"] = raw["topics_covered"][-100:]
    if topic and correct is True:
        raw["strong_areas"][topic] = raw["strong_areas"].get(topic, 0) + 1
    if topic and correct is False:
        raw["weak_areas"][topic] = raw["weak_areas"].get(topic, 0) + 1
    raw["stars"] = raw.get("stars", 0) + max(0, int(stars))
    today = time.strftime("%Y-%m-%d")
    streak = raw.get("streak", {"count": 0, "last_day": ""})
    if streak.get("last_day") != today:
        yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
        streak["count"] = streak.get("count", 0) + 1 if streak.get("last_day") == yesterday else 1
        streak["last_day"] = today
        raw["streak"] = streak
    raw["log"].append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "kind": kind, "topic": topic})
    raw["log"] = raw["log"][-200:]
    p.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return _public(raw)


def parent_report(pid: str) -> dict | None:
    raw = _raw(pid)
    if raw is None:
        return None
    weak = sorted(raw.get("weak_areas", {}).items(), key=lambda kv: -kv[1])[:8]
    strong = sorted(raw.get("strong_areas", {}).items(), key=lambda kv: -kv[1])[:8]
    import collections
    per_day = collections.Counter(
        e["t"][:10] for e in raw.get("log", []) if e.get("t"))
    days = sorted(per_day.items())[-7:]  # last 7 active days
    return {
        "name": raw["name"], "grade": raw["grade"], "stars": raw["stars"],
        "streak": raw.get("streak", {}), "weak_areas": weak,
        "strong_areas": strong,
        "recent_activity": [e for e in raw.get("log", [])[-30:]],
        "topics_covered": raw.get("topics_covered", [])[-20:],
        "stickers": raw.get("stickers", {}),
        "week": {"days": days, "activities": sum(v for _, v in days)},
    }


def _raw(pid: str) -> dict | None:
    p = _path(pid)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _public(raw: dict) -> dict:
    return {k: v for k, v in raw.items() if k != "parent_pin_hash"}


def _hash_pin(pin: str) -> str:
    import hashlib
    return hashlib.sha256(("edusphere:" + str(pin)).encode()).hexdigest()
