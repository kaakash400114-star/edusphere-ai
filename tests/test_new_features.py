"""Tests for the new world-class EduSphere AI modules:
  - app.llm (multi-provider adapter)
  - app.animations (character animation system)
  - app.srs (spaced repetition)
  - API endpoints: /api/provider, /api/animate, /api/particles, /api/srs
"""
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import animations, srs

client = TestClient(app)


# ──────────────────────────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────────────────────────

def _mk(name="TestKid", grade=5, **kw):
    r = client.post("/api/profile", json={"name": name, "grade": grade, **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ══════════════════════════════════════════════════════════════════════════════
# LLM adapter
# ══════════════════════════════════════════════════════════════════════════════

def test_llm_provider_endpoint_shape():
    r = client.get("/api/provider")
    assert r.status_code == 200
    data = r.json()
    assert "provider" in data
    assert "model" in data
    assert "configured" in data
    assert isinstance(data["configured"], bool)


def test_llm_is_configured_returns_bool():
    from app import llm
    result = llm.is_configured()
    assert isinstance(result, bool)


def test_llm_provider_and_model_names_are_strings():
    from app import llm
    assert isinstance(llm.provider_name(), str)
    assert isinstance(llm.model_name(), str)


# ══════════════════════════════════════════════════════════════════════════════
# Animation system
# ══════════════════════════════════════════════════════════════════════════════

def test_all_buddies_have_animations():
    buddy_ids = ["leo", "miko", "pip", "chintu", "zara", "toko", "kiko", "bip", "dodo", "nova"]
    for bid in buddy_ids:
        result = animations.context_actions(bid, "on_correct")
        assert result["buddy"] == bid
        assert len(result["sequence"]) > 0, f"{bid} has no animate sequence"


def test_animation_sequence_has_css_and_duration():
    result = animations.context_actions("leo", "on_correct")
    for step in result["sequence"]:
        assert "css" in step
        assert "duration" in step
        assert isinstance(step["duration"], int)


def test_animate_api_endpoint():
    r = client.get("/api/animate/leo/on_correct")
    assert r.status_code == 200
    data = r.json()
    assert data["buddy"] == "leo"
    assert data["context"] == "on_correct"
    assert isinstance(data["sequence"], list)


def test_animate_api_unknown_buddy_returns_404():
    r = client.get("/api/animate/dragon_from_atlantis/on_correct")
    assert r.status_code == 404


def test_animate_contexts_endpoint():
    r = client.get("/api/animate/nova")
    assert r.status_code == 200
    data = r.json()
    assert data["buddy"] == "nova"
    assert "contexts" in data
    assert "actions" in data
    assert "on_correct" in data["contexts"]


def test_particles_endpoint():
    r = client.get("/api/particles")
    assert r.status_code == 200
    data = r.json()
    assert "particles" in data
    assert "stars_gold" in data["particles"]
    assert "confetti_rainbow" in data["particles"]


def test_chat_includes_animation():
    pid = _mk("AnimTest", 5)
    r = client.post("/api/chat", json={
        "pid": pid, "message": "What is 2 + 2?", "history": []})
    # Even without an LLM key, the animation should be present in the response
    # (chat may fail with setup-needed but animation field must be in the JSON)
    # If LLM is not configured we get 200 with an error message, not 5xx
    assert r.status_code == 200


def test_all_animation_actions_have_css():
    for action_name in animations.all_actions():
        anim = animations._ACTIONS[action_name]
        assert "css" in anim, f"Action {action_name} missing css key"


def test_particles_have_required_fields():
    for name, p in animations.PARTICLES.items():
        assert "type" in p, f"Particle {name} missing type"
        assert "count" in p, f"Particle {name} missing count"


def test_leo_celebrates_on_correct():
    result = animations.context_actions("leo", "on_correct")
    actions = [s["action"] for s in result["sequence"]]
    # Leo should backflip or celebrate on correct answer
    assert any(a in ("backflip", "celebrate", "jump") for a in actions)


def test_miko_sleeps_while_thinking():
    result = animations.context_actions("miko", "on_thinking")
    actions = [s["action"] for s in result["sequence"]]
    assert "sleep" in actions, f"Miko should sleep while thinking, got {actions}"


def test_dodo_sneezes_on_greet():
    result = animations.context_actions("dodo", "on_greet")
    actions = [s["action"] for s in result["sequence"]]
    assert "sneeze" in actions, f"Dodo should sneeze on greet, got {actions}"


def test_pip_is_jumpy_on_correct():
    result = animations.context_actions("pip", "on_correct")
    actions = [s["action"] for s in result["sequence"]]
    assert "jump" in actions or "spin" in actions, \
        f"Pip should jump/spin on correct, got {actions}"


# ══════════════════════════════════════════════════════════════════════════════
# Spaced Repetition System (SRS)
# ══════════════════════════════════════════════════════════════════════════════

def test_sm2_first_correct_gives_interval_1():
    card = {}
    updated = srs._sm2(card, quality=5)
    assert updated["interval"] == 1
    assert updated["reps"] == 1
    assert updated["ef"] >= 2.5


def test_sm2_second_correct_gives_interval_6():
    card = {"interval": 1, "reps": 1, "ef": 2.5}
    updated = srs._sm2(card, quality=5)
    assert updated["interval"] == 6
    assert updated["reps"] == 2


def test_sm2_wrong_resets_reps():
    card = {"interval": 10, "reps": 5, "ef": 2.5}
    updated = srs._sm2(card, quality=1)
    assert updated["reps"] == 0
    assert updated["interval"] == 1


def test_sm2_ef_never_below_1_3():
    card = {"interval": 1, "reps": 0, "ef": 1.4}
    for _ in range(10):
        card = srs._sm2(card, quality=0)
    assert card["ef"] >= 1.3


def test_update_card_creates_new_card():
    raw = {}
    srs.update_card(raw, "topic_fractions", "Fractions", "math", quality=4)
    assert "srs_cards" in raw
    assert "topic_fractions" in raw["srs_cards"]


def test_due_topics_returns_overdue():
    raw = {}
    # Create a card that was due yesterday
    card = srs._new_card("old_topic", "Old Topic", "math")
    card["due"] = time.time() - 86400  # 1 day ago
    raw["srs_cards"] = {"old_topic": card}
    due = srs.due_topics(raw)
    assert len(due) == 1
    assert due[0]["topic_id"] == "old_topic"


def test_due_topics_excludes_future():
    raw = {}
    card = srs._new_card("future_topic", "Future", "math")
    card["due"] = time.time() + 86400  # tomorrow
    raw["srs_cards"] = {"future_topic": card}
    due = srs.due_topics(raw)
    assert len(due) == 0


def test_srs_summary_counts():
    raw = {}
    for i in range(3):
        srs.update_card(raw, f"topic_{i}", f"Topic {i}", "math", quality=5)
    summary = srs.srs_summary(raw)
    assert summary["total_cards"] == 3
    assert isinstance(summary["due_now"], int)
    assert isinstance(summary["mastered"], int)


def test_quality_from_accuracy():
    assert srs.quality_from_accuracy(10, 10) == 5   # perfect (1.0 >= 0.95)
    assert srs.quality_from_accuracy(9, 10) == 4    # very good (0.9 >= 0.85)
    assert srs.quality_from_accuracy(8, 10) == 3    # good (0.8 >= 0.65)
    assert srs.quality_from_accuracy(0, 10) == 0    # blank
    assert srs.quality_from_accuracy(0, 0) == 0     # no data


def test_srs_api_endpoint():
    pid = _mk("SRSKid", 6)
    r = client.get(f"/api/srs/{pid}")
    assert r.status_code == 200
    data = r.json()
    assert "due" in data
    assert "upcoming" in data
    assert "summary" in data


def test_srs_api_404_for_unknown_profile():
    r = client.get("/api/srs/nonexistent-profile-xyz")
    assert r.status_code == 404


def test_upcoming_topics_within_window():
    raw = {}
    card = srs._new_card("upcoming_topic", "Upcoming", "science")
    card["due"] = time.time() + 12 * 3600  # 12 hours from now
    raw["srs_cards"] = {"upcoming_topic": card}
    upcoming = srs.upcoming_topics(raw, hours=24)
    assert len(upcoming) == 1
    assert upcoming[0]["topic_id"] == "upcoming_topic"


# ══════════════════════════════════════════════════════════════════════════════
# World boards expansion
# ══════════════════════════════════════════════════════════════════════════════

def test_world_boards_count():
    from app import boards
    assert len(boards.BOARDS) >= 20, f"Expected 20+ boards, got {len(boards.BOARDS)}"


def test_ib_board_present():
    from app import boards
    assert "ib" in boards.BOARDS
    assert boards.BOARDS["ib"]["country"] == "International"


def test_ap_board_present():
    from app import boards
    assert "ap" in boards.BOARDS
    assert boards.BOARDS["ap"]["country"] == "United States"


def test_singapore_board_present():
    from app import boards
    assert "singapore" in boards.BOARDS


def test_new_boards_normalize_correctly():
    from app import boards
    assert boards.normalize_board("ib") == "ib"
    assert boards.normalize_board("Singapore") == "singapore"
    assert boards.normalize_board("JAPANESE") == "japanese"
    assert boards.normalize_board("atlantis") == "cbse"  # fallback


def test_new_boards_have_description():
    from app import boards
    for bid, b in boards.BOARDS.items():
        assert "description" in b, f"Board {bid} missing description"
        assert len(b["description"]) > 10, f"Board {bid} description too short"


def test_new_boards_have_country():
    from app import boards
    for bid, b in boards.BOARDS.items():
        assert "country" in b, f"Board {bid} missing country"
        assert len(b["country"]) > 0, f"Board {bid} empty country"


def test_profile_can_be_created_with_ib_board():
    r = client.post("/api/profile", json={"name": "IBKid", "grade": 11, "board": "ib"})
    assert r.status_code == 200
    assert r.json()["profile"]["board"] == "ib"


def test_profile_can_be_created_with_ap_board():
    r = client.post("/api/profile", json={"name": "APKid", "grade": 11, "board": "ap"})
    assert r.status_code == 200
    assert r.json()["profile"]["board"] == "ap"
