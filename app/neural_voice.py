"""Human-like neural voices (edge-tts / Microsoft neural TTS).

BROWSER FALLBACK: if edge-tts is unavailable or fails (offline), the
frontend keeps its built-in Web Speech synthesis with the buddy's
rate/pitch profile — the app never loses its voice.

Each of the 10 buddies gets a DISTINCT natural human speaker, chosen for
the buddy's personality. All are verified-available Microsoft neural
voices (en-US / en-GB / en-IN / en-AU).
"""
from __future__ import annotations

import asyncio
import hashlib
import os
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

_CACHE_DIR = os.path.join(tempfile.gettempdir(), "edusphere_tts")
os.makedirs(_CACHE_DIR, exist_ok=True)


def _cache_path(text: str, voice_cfg: dict) -> str:
    key = hashlib.sha1(
        (voice_cfg["voice"] + "|" + voice_cfg["rate"] + "|" + voice_cfg["pitch"] + "|" + text)
        .encode("utf-8")).hexdigest() + ".mp3"
    return os.path.join(_CACHE_DIR, key)


def _generate(text: str, voice_cfg: dict, out_path: str) -> None:
    async def run():
        com = edge_tts.Communicate(
            text, voice_cfg["voice"],
            rate=voice_cfg["rate"], pitch=voice_cfg["pitch"])
        await com.save(out_path)
    asyncio.run(run())


def synth(buddy_id: str, text: str) -> str | None:
    """Return path to an mp3 for this text in this buddy's voice, or None
    if edge-tts is unavailable/failed (frontend then falls back to Web Speech)."""
    if not _HAS_EDGE or not text.strip():
        return None
    cfg = BUDDY_VOICES.get(buddy_id) or BUDDY_VOICES["leo"]
    out = _cache_path(text, cfg)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return out
    try:
        _generate(text, cfg, out)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            return out
    except Exception:
        pass
    return None


def voice_public(buddy_id: str) -> dict:
    """Neural voice descriptor for the frontend; includes browser fallback."""
    cfg = BUDDY_VOICES.get(buddy_id) or BUDDY_VOICES["leo"]
    return {"engine": "edge", "voice": cfg["voice"],
            "rate": cfg["rate"], "pitch": cfg["pitch"]}
