"""Stage 5: board system + CBSE knowledge files wired end-to-end."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import boards, knowledge
from app.main import app

client = TestClient(app)


def _mk(name="Boardy", grade=7, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- board roster and normalisation ----------
def test_six_boards_exposed():
    r = client.get("/api/boards")
    assert r.status_code == 200
    ids = {b["id"] for b in r.json()["boards"]}
    assert ids == {"cbse", "icse", "matriculation", "tn_state",
                   "american", "british"}


def test_board_normalisation_and_default():
    assert boards.normalize_board(None) == "cbse"
    assert boards.normalize_board("British") == "british"
    assert boards.normalize_board("TN State") == "tn_state"
    assert boards.normalize_board("nope") == "cbse"


# ---------- profile stores board; settings can change it ----------
def test_profile_stores_board_and_settings_change_it():
    pid = _mk("BoardSet", 8, board="british")
    p = client.get(f"/api/profile/{pid}").json()["profile"]
    assert p["board"] == "british"

    r = client.post(f"/api/settings/{pid}", json={"board": "american"})
    assert r.json()["profile"]["board"] == "american"

    # unknown board falls back to default, never crashes
    r = client.post(f"/api/settings/{pid}", json={"board": "atlantis"})
    assert r.json()["profile"]["board"] == "cbse"


def test_onboarding_defaults_to_cbse():
    pid = _mk("DefaultCBSE", 5)
    p = client.get(f"/api/profile/{pid}").json()["profile"]
    assert p["board"] == "cbse"


# ---------- CBSE knowledge files exist and are used ----------
def test_cbse_files_exist_for_every_grade_and_subject():
    for g in range(1, 13):
        for sub in ("mathematics", "science", "english"):
            fname = {"mathematics": "math", "science": "science",
                     "english": "english"}[sub]
            p = (knowledge.KNOWLEDGE_DIR / "boards" / "cbse" / sub /
                 f"grade{g}_{fname}.md")
            assert p.exists(), f"missing CBSE file {p}"
            text = p.read_text(encoding="utf-8")
            assert text.startswith("# CBSE"), f"{p} missing CBSE header"
            assert text.count("## ") >= 5, f"{p} has too few sections"


def test_cbse_resolution_prefers_board_files():
    path = boards.knowledge_path_for("cbse", "math", 10)
    assert path is not None
    assert "boards" in str(path) and "cbse" in str(path)
    # a board WITH its own files resolves to them
    path2 = boards.knowledge_path_for("icse", "math", 10)
    assert path2 is not None
    assert "icse" in str(path2)


def test_every_board_resolves_all_grades_and_subjects():
    # all six boards now have full coverage grades 1-12
    for board in ("cbse", "icse", "matriculation", "tn_state",
                  "american", "british"):
        for g in range(1, 13):
            for sub in ("math", "science", "english"):
                p = boards.knowledge_path_for(board, sub, g)
                assert p is not None, f"{board} {sub} {g}: no file"
                assert p.exists(), f"{board} {sub} {g}: file missing"


def test_extract_relevant_uses_resolver():
    text = knowledge.extract_relevant(
        "math", 10, "quadratic equations",
        path=boards.knowledge_path_for("cbse", "math", 10))
    assert "Quadratic" in text or "quadratic" in text


# ---------- English standard directive per board ----------
def test_english_directives_differ():
    d_cbse = boards.english_directive("cbse")
    d_us = boards.english_directive("american")
    d_uk = boards.english_directive("british")
    assert "NCERT" in d_cbse
    assert "Common Core" in d_us and "color" in d_us
    assert "GCSE" in d_uk and "colour" in d_uk
    assert d_cbse != d_us != d_uk


# ---------- live chat includes the board directive (unit-level) ----------
def test_tutor_system_prompt_contains_board_block():
    from app import tutor
    s = tutor._system_prompt("Kid", 10, "leo", [], board="american")
    assert "Common Core" in s
    s2 = tutor._system_prompt("Kid", 10, "leo", [], board="cbse")
    assert "NCERT" in s2
