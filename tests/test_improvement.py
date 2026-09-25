"""Stage 2 rework: honest improvement engine + account settings API."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import improvement
from app.main import app

client = TestClient(app)


def _mk(name="Setter", grade=4, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


def _ev(days_ago, correct, total, subject="math"):
    t = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - days_ago * 86400))
    return {"t": t, "subject": subject, "correct": correct, "total": total,
            "source": "test"}


# ---------- rating bands are honest ----------
def test_rating_bands():
    assert improvement.rating_for(1.00) == "Amazing"
    assert improvement.rating_for(0.96) == "Amazing"
    assert improvement.rating_for(0.86) == "Very Good"
    assert improvement.rating_for(0.70) == "Good"
    assert improvement.rating_for(0.50) == "Fair"
    assert improvement.rating_for(0.30) == "Bad"
    assert improvement.rating_for(0.10) == "Worst"


def test_no_data_means_no_rating():
    rep = improvement.improvement_report({"practice_log": []}, 4)
    assert rep["overall"]["rating"] is None
    assert "No practice yet" in rep["overall"]["note"]
    assert rep["subjects"] == []


def test_trend_detection():
    now = time.time()
    events = [
        # previous fortnight: strong
        _ev(20, 9, 10), _ev(18, 9, 10), _ev(16, 8, 10),
        # recent fortnight: weaker
        _ev(3, 5, 10), _ev(2, 4, 10), _ev(1, 5, 10),
    ]
    rep = improvement.improvement_report({"practice_log": events}, 7)
    assert rep["overall"]["trend"] == "slipping"
    assert rep["overall"]["delta"] is not None and rep["overall"]["delta"] <= -5
    assert rep["overall"]["rating"] in ("Bad", "Worst", "Fair")


def test_improving_trend_and_upward_delta():
    events = [
        _ev(20, 4, 10), _ev(18, 5, 10), _ev(16, 4, 10),
        _ev(3, 9, 10), _ev(2, 9, 10), _ev(1, 8, 10),
    ]
    rep = improvement.improvement_report({"practice_log": events}, 7)
    assert rep["overall"]["trend"] == "improving"
    assert rep["overall"]["delta"] >= 5


# ---------- tone scales with grade, verdict does not ----------
def test_wording_scales_by_grade_same_rating():
    events = [_ev(1, 3, 10), _ev(2, 3, 10)]
    young = improvement.improvement_report({"practice_log": events}, 2)
    teen = improvement.improvement_report({"practice_log": events}, 10)
    assert young["overall"]["rating"] == teen["overall"]["rating"]
    assert "You got 6 of 20" in young["overall"]["note"]       # gentle
    assert "% accuracy" in teen["overall"]["note"]             # direct
    assert "practice_log" not in teen["overall"]["note"]


def test_per_subject_weakest_first():
    events = ([_ev(1, 9, 10, "math"), _ev(2, 9, 10, "math")]
              + [_ev(1, 2, 10, "english"), _ev(2, 2, 10, "english")])
    rep = improvement.improvement_report({"practice_log": events}, 6)
    subjects = [s["subject"] for s in rep["subjects"]]
    assert subjects[0] == "english"          # weakest first
    assert rep["subjects"][0]["rating"] in ("Bad", "Worst")
    assert rep["subjects"][1]["rating"] in ("Amazing", "Very Good")


# ---------- settings API ----------
def test_settings_get_and_save():
    pid = _mk("Setty", 4)
    r = client.get(f"/api/settings/{pid}")
    assert r.status_code == 200
    d = r.json()
    assert d["profile"]["voice_speed"] == 1.0 and d["profile"]["voice_on"] is True
    assert "improvement" in d

    # save name + grade + buddy + voice
    r = client.post(f"/api/settings/{pid}", json={
        "name": "Setty2", "grade": 7, "character": "nova",
        "voice_speed": 1.3, "voice_on": False})
    assert r.status_code == 200, r.text
    p = r.json()["profile"]
    assert p["name"] == "Setty2" and p["grade"] == 7
    assert p["character"] == "nova"
    assert p["voice_speed"] == 1.3 and p["voice_on"] is False
    # grade change is journaled (improvement history stays interpretable)
    import json, pathlib
    raw = json.loads(pathlib.Path(f"data/profiles/{pid}.json").read_text())
    assert raw["grade_changes"][-1]["from"] == 4
    assert raw["grade_changes"][-1]["to"] == 7
    pathlib.Path(f"data/profiles/{pid}.json").unlink()


def test_pin_change_requires_current_pin():
    pid = _mk("Pinny", 5)
    # wrong current pin rejected
    r = client.post(f"/api/settings/{pid}", json={
        "current_pin": "0000", "new_pin": "5678"})
    assert r.status_code == 403
    # correct current pin works
    r = client.post(f"/api/settings/{pid}", json={
        "current_pin": "1234", "new_pin": "5678"})
    assert r.status_code == 200
    # old pin no longer opens the parent report; new one does
    assert client.post("/api/parent/report",
                       json={"pid": pid, "pin": "1234"}).status_code == 403
    assert client.post("/api/parent/report",
                       json={"pid": pid, "pin": "5678"}).status_code == 200


def test_parent_report_has_improvement():
    pid = _mk("Repor", 6)
    client.post(f"/api/practice/{pid}", json={})  # no-op sanity (404 ok)
    events_missing = client.get(f"/api/settings/{pid}").json()["improvement"]
    assert events_missing["overall"]["rating"] is None
    # one practice event -> rating appears
    topics = client.get(f"/api/practice/{pid}").json()["topics"]
    t = topics[0]
    client.post(f"/api/practice/{pid}/{t['id']}/done", json={"topic_id": t["id"]})
    rep = client.post("/api/parent/report",
                      json={"pid": pid, "pin": "1234"}).json()["report"]
    assert "improvement" in rep
    assert rep["improvement"]["overall"]["rating"] is not None
