"""Tests for all 4 major enhancements:
1. Multi-provider Gemini & Streaming LLM adapter
2. Dynamic Vision Model resolution & Multimodal handling
3. Streaming chat endpoint (/api/chat/stream)
4. Service worker offline CDN caching
5. Study Tools (Flashcards with SM-2, Notes Notebook, Quizzes Arena)
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

from app import camera, llm, study_tools
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_pid():
    res = client.post("/api/profile", json={"name": "EnhancedKid", "grade": 6, "character": "leo"})
    assert res.status_code == 200
    return res.json()["pid"]


# ══════════════════════════════════════════════════════════════════════════════
# 1. GEMINI & STREAMING LLM ADAPTER
# ══════════════════════════════════════════════════════════════════════════════

def test_gemini_provider_defaults():
    assert "gemini" in llm._PROVIDER_DEFAULTS
    gcfg = llm._PROVIDER_DEFAULTS["gemini"]
    assert "googleapis.com" in gcfg["base_url"]
    assert "gemini" in gcfg["model"]
    assert gcfg["key_env"] == "GEMINI_API_KEY"


def test_gemini_provider_autodetect(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key_12345")
    monkeypatch.delenv("EDUSPHERE_PROVIDER", raising=False)
    assert llm._resolve_provider() == "gemini"
    cfg = llm._cfg()
    assert cfg["provider"] == "gemini"
    assert cfg["api_key"] == "test_gemini_key_12345"


def test_complete_stream_no_key_warning(monkeypatch):
    monkeypatch.delenv("GLM_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setenv("EDUSPHERE_PROVIDER", "gemini")
    chunks = list(llm.complete_stream([{"role": "user", "content": "hi"}]))
    assert len(chunks) == 1
    assert "Setup needed" in chunks[0]


def test_anthropic_multimodal_turn_formatting():
    messages = [
        {"role": "system", "content": "system prompt"},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg=="}},
                {"type": "text", "text": "What is in this sum?"},
            ],
        },
    ]
    system, turns = llm._format_anthropic_turns(messages)
    assert system == "system prompt"
    assert len(turns) == 1
    adapted_content = turns[0]["content"]
    assert adapted_content[0]["type"] == "image"
    assert adapted_content[0]["source"]["type"] == "base64"
    assert adapted_content[0]["source"]["media_type"] == "image/png"
    assert adapted_content[1]["text"] == "What is in this sum?"


# ══════════════════════════════════════════════════════════════════════════════
# 2. DYNAMIC CAMERA VISION RESOLUTION
# ══════════════════════════════════════════════════════════════════════════════

def test_camera_vision_model_override(monkeypatch):
    monkeypatch.setenv("EDUSPHERE_VISION_MODEL", "custom-vision-pro-1.0")
    models = camera._resolve_vision_models()
    assert models == ["custom-vision-pro-1.0"]


def test_camera_vision_models_for_gemini(monkeypatch):
    monkeypatch.delenv("EDUSPHERE_VISION_MODEL", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini")
    monkeypatch.setenv("EDUSPHERE_PROVIDER", "gemini")
    models = camera._resolve_vision_models()
    assert any("gemini" in m for m in models)


# ══════════════════════════════════════════════════════════════════════════════
# 3. STREAMING CHAT SSE ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════

def test_chat_stream_endpoint(mock_pid, monkeypatch):
    # Mock ask_stream to yield predictable tokens
    from app import tutor

    def fake_stream(*a, **kw):
        yield "Photosynthesis "
        yield "is the "
        yield "solar kitchen! "

    monkeypatch.setattr(tutor, "ask_stream", fake_stream)

    res = client.post("/api/chat/stream", json={"pid": mock_pid, "message": "What is photosynthesis?"})
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]
    text = res.text
    assert "Photosynthesis" in text
    assert '"done": true' in text


# ══════════════════════════════════════════════════════════════════════════════
# 4. SERVICE WORKER OFFLINE CACHING
# ══════════════════════════════════════════════════════════════════════════════

def test_service_worker_caches_cdn():
    sw_path = Path(__file__).resolve().parent.parent / "static" / "sw.js"
    assert sw_path.exists()
    content = sw_path.read_text(encoding="utf-8")
    assert "jsdelivr.net" in content
    assert "edusphere-v15" in content


# ══════════════════════════════════════════════════════════════════════════════
# 5. STUDY TOOLS (FLASHCARDS, NOTES, QUIZZES)
# ══════════════════════════════════════════════════════════════════════════════

def test_study_flashcards_deck_flow(mock_pid):
    # Generate a deck
    res = client.post(f"/api/study/flashcards/{mock_pid}/generate", json={
        "subject": "science",
        "topic": "Gravity",
        "count": 4,
        "difficulty": "medium",
    })
    assert res.status_code == 200
    deck = res.json()["deck"]
    assert deck["topic"] == "Gravity"
    assert len(deck["cards"]) >= 3
    card_id = deck["cards"][0]["id"]

    # Review card with SM-2 quality 4 (good recall)
    rev_res = client.post(f"/api/study/flashcards/{mock_pid}/review", json={
        "deck_id": deck["id"],
        "card_id": card_id,
        "quality": 4,
    })
    assert rev_res.status_code == 200
    assert rev_res.json()["ok"] is True
    assert rev_res.json()["card"]["reps"] >= 1

    # List decks
    list_res = client.get(f"/api/study/flashcards/{mock_pid}")
    assert list_res.status_code == 200
    assert len(list_res.json()["decks"]) >= 1


def test_study_notes_crud_flow(mock_pid):
    # 1. Create a note
    res = client.post(f"/api/study/notes/{mock_pid}", json={
        "title": "Newton's Laws Summary",
        "subject": "physics",
        "content": "# Newton's 3 Laws\n1. Inertia\n2. F = ma\n3. Action & Reaction",
    })
    assert res.status_code == 200
    note = res.json()["note"]
    note_id = note["id"]
    assert note["title"] == "Newton's Laws Summary"

    # 2. List notes
    list_res = client.get(f"/api/study/notes/{mock_pid}?subject=physics")
    assert list_res.status_code == 200
    assert any(n["id"] == note_id for n in list_res.json()["notes"])

    # 3. Update note
    up_res = client.post(f"/api/study/notes/{mock_pid}", json={
        "note_id": note_id,
        "title": "Newton's Laws (Updated)",
        "subject": "physics",
        "content": "Expanded notes on gravity and friction.",
    })
    assert up_res.status_code == 200
    assert up_res.json()["note"]["title"] == "Newton's Laws (Updated)"

    # 4. Delete note
    del_res = client.delete(f"/api/study/notes/{mock_pid}/{note_id}")
    assert del_res.status_code == 200
    assert del_res.json()["ok"] is True

    # 5. Confirm deletion
    list_after = client.get(f"/api/study/notes/{mock_pid}").json()["notes"]
    assert not any(n["id"] == note_id for n in list_after)


def test_study_quiz_flow(mock_pid):
    # 1. Generate quiz
    gen_res = client.post(f"/api/study/quiz/{mock_pid}/generate", json={
        "subject": "science",
        "topic": "Solar System",
        "count": 3,
        "difficulty": "easy",
    })
    assert gen_res.status_code == 200
    quiz = gen_res.json()["quiz"]
    quiz_id = quiz["id"]
    assert len(quiz["questions"]) >= 2
    assert len(quiz["questions"][0]["options"]) == 4

    # 2. Submit quiz answers
    answers = {}
    for q in quiz["questions"]:
        answers[q["id"]] = q["answer"]  # all correct

    sub_res = client.post(f"/api/study/quiz/{mock_pid}/submit", json={
        "quiz_id": quiz_id,
        "answers": answers,
    })
    assert sub_res.status_code == 200
    result = sub_res.json()
    assert result["ok"] is True
    assert result["score"] == 100
    assert result["correct"] == len(quiz["questions"])
    assert result["stars_earned"] > 0

    # 3. List quizzes
    quizzes = client.get(f"/api/study/quizzes/{mock_pid}").json()["quizzes"]
    assert any(q["id"] == quiz_id and q["submitted"] for q in quizzes)
