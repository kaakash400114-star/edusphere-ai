"""Tests for neural voice module (edge-tts human speakers)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import neural_voice as nv


def test_ten_distinct_voices():
    voices = {c["voice"] for c in nv.BUDDY_VOICES.values()}
    assert len(nv.BUDDY_VOICES) == 10
    assert len(voices) == 10, "every buddy needs a distinct speaker"


def test_voice_public_shape():
    v = nv.voice_public("chintu")
    assert v["engine"] == "edge"
    assert "Neural" in v["voice"]
    assert "rate" in v and "pitch" in v


def test_voice_public_fallback():
    v = nv.voice_public("nonexistent-buddy")
    assert v["voice"] == nv.BUDDY_VOICES["leo"]["voice"]


def test_known_neural_names():
    allowed_prefixes = ("en-US-", "en-GB-", "en-IN-", "en-AU-")
    for c in nv.BUDDY_VOICES.values():
        assert c["voice"].startswith(allowed_prefixes), c["voice"]
        assert c["voice"].endswith("Neural"), c["voice"]
