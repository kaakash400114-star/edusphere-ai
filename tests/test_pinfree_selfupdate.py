"""Tests: optional parent PIN + self-updating knowledge engine (offline paths)."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# never let tests talk to the live LLM or start the background healer
os.environ.setdefault("EDUSPHERE_NO_AUTOFRESH", "1")

from fastapi.testclient import TestClient

from app import knowledge_fresh, profiles
from app.main import app

client = TestClient(app)

# offline: the writer never calls the API in tests
knowledge_fresh.write_section_body = lambda *a, **k: None


def _mk(name="Pinfree", grade=4, **kw):
    r = client.post("/api/profile", json={"name": name, "grade": grade, **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- optional PIN ----------

def test_signup_without_pin():
    pid = _mk(name="NoPinKid", grade=2)          # no parent_pin at all
    d = client.get(f"/api/profile/{pid}").json()["profile"]
    assert d["has_pin"] is False
    assert "parent_pin_hash" not in d


def test_report_without_pin_opens():
    pid = _mk(name="OpenReport", grade=5)
    r = client.post("/api/parent/report", json={"pid": pid, "pin": ""})
    assert r.status_code == 200, r.text
    assert r.json()["report"]["pin_protected"] is False


def test_settings_report_has_pin_flag():
    pid = _mk(name="FlagKid", grade=6, parent_pin="9988")
    d = client.get(f"/api/settings/{pid}").json()
    assert d["has_pin"] is True
    r = client.post("/api/parent/report", json={"pid": pid, "pin": "9988"})
    assert r.status_code == 200
    assert r.json()["report"]["pin_protected"] is True


def test_set_then_remove_pin_via_settings():
    pid = _mk(name="Cycle", grade=7)             # start with none
    # set one
    r = client.post(f"/api/settings/{pid}",
                    json={"new_pin": "4444"})
    assert r.status_code == 200
    assert client.get(f"/api/profile/{pid}").json()["profile"]["has_pin"] is True
    # wrong PIN cannot read the report now
    assert client.post("/api/parent/report",
                       json={"pid": pid, "pin": ""}).status_code == 403
    # right PIN reads it
    assert client.post("/api/parent/report",
                       json={"pid": pid, "pin": "4444"}).status_code == 200
    # remove it (empty new_pin)
    r = client.post(f"/api/settings/{pid}",
                    json={"current_pin": "4444", "new_pin": ""})
    assert r.status_code == 200
    assert client.get(f"/api/profile/{pid}").json()["profile"]["has_pin"] is False
    assert client.post("/api/parent/report",
                       json={"pid": pid, "pin": ""}).status_code == 200


def test_short_pin_still_rejected():
    r = client.post("/api/profile",
                    json={"name": "Shorty", "grade": 3, "parent_pin": "12"})
    assert r.status_code == 422                  # min_length=4 still enforced


# ---------- self-updating knowledge (offline parts) ----------

def test_audit_counts_thin_sections():
    text = "# T\n\n## One\n" + "word " * 70 + "\n\n## Two\nshort\n"
    a = knowledge_fresh.audit_text(text)
    assert a["sections"] == 2 and a["thin"] == 1
    assert a["thin_titles"] == ["Two"]


def test_validate_body_rules():
    assert knowledge_fresh.validate_body("Just a plain good body. " * 10)
    assert knowledge_fresh.validate_body("short") is None
    assert knowledge_fresh.validate_body("## has headings\n" + "x " * 80) is None
    assert knowledge_fresh.validate_body(
        "Here is a summary. " + "word " * 60) is None       # meta talk
    too_long = "word " * 300
    assert knowledge_fresh.validate_body(too_long) is None


def test_split_and_heal_roundtrip(tmp_path):
    f = tmp_path / "grade9_science.md"
    f.write_text("# G9\n\n## Gravity\n\n## Photosynthesis\n", encoding="utf-8")
    assert knowledge_fresh.audit_file(f)["thin"] == 2
    # offline heal: splice bodies by hand the same way heal_file does
    import re
    text = f.read_text(encoding="utf-8")
    body = "word " * 60
    for title in ("Gravity", "Photosynthesis"):
        text = re.sub(r"(^## +" + title + r"\s*$)", r"\1\n" + body,
                      text, count=1, flags=re.M)
    f.write_text(text, encoding="utf-8")
    assert knowledge_fresh.audit_file(f)["thin"] == 0


def test_health_endpoint_shape():
    r = client.get("/api/knowledge/health")
    assert r.status_code == 200
    d = r.json()
    assert d["self_updating"] is True
    assert "thin_sections" in d["library"]
    assert "needs_attention" in d


def test_refresh_endpoint_runs():
    # with no GLM key this still returns a valid (zero-fix) report
    r = client.post("/api/knowledge/refresh")
    assert r.status_code == 200
    assert "fixed_sections" in r.json() or "skipped" in r.json()


# ---------- chat burst limiter ----------

def test_burst_limiter_unit():
    from app.main import _burst_ok
    ok = all(_burst_ok("burst-test-pid") for _ in range(5))
    assert ok
    assert _burst_ok("burst-test-pid", max_per_hour=2) is False


def test_burst_limiter_blocks_chat(monkeypatch):
    import app.main as m
    pid = _mk(name="BurstKid", grade=4)
    m._chat_hist[pid] = [time.time()] * 500       # simulate a flood
    r = client.post("/api/chat", json={"pid": pid, "message": "hi"})
    assert r.status_code == 429
