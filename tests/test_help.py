"""Launch pass — help & feedback + report payload basics. Offline tests."""
import io, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import help as help_mod, profiles


def test_help_submit_and_list(tmp_path, monkeypatch):
    monkeypatch.setattr(help_mod, "DATA", tmp_path)
    r = help_mod.submit("kid-1", "Aarav", "The mic button is not working", "complaint")
    assert r["ok"]
    rows = help_mod.list_all()
    assert len(rows) == 1 and rows[0]["kind"] == "complaint"
    assert rows[0]["pid"] == "kid-1"


def test_help_rejects_short(tmp_path, monkeypatch):
    monkeypatch.setattr(help_mod, "DATA", tmp_path)
    r = help_mod.submit("kid-1", "A", "hi", "question")
    assert not r["ok"]


def test_help_sanitize_pid(tmp_path, monkeypatch):
    monkeypatch.setattr(help_mod, "DATA", tmp_path)
    r = help_mod.submit("../evil/../pid", "X", "a longer message here")
    assert r["ok"]
    assert help_mod.list_all()[0]["pid"] == "evilpid"


def test_help_routes(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app
    monkeypatch.setattr(help_mod, "DATA", tmp_path)
    client = TestClient(app)
    pid = client.post("/api/profile", json={
        "name": "Helpy", "grade": 3, "character": "leo",
        "board": "cbse"}).json()["pid"]
    r = client.post(f"/api/help/{pid}",
                    json={"message": "How do I change my buddy?", "kind": "question"})
    assert r.status_code == 200 and r.json()["ok"]
    lst = client.get(f"/api/help/{pid}").json()
    assert len(lst["tickets"]) == 1
    client.close()
