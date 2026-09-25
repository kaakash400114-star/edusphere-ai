"""Stage 2: MEMORY extraction — buddy-saved life details reach the profile."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_memory_line_extracted_from_answer(monkeypatch):
    import app.main as m

    def fake_ask(**kw):
        return "Wow, a dog named Kutta! FUN FACT: 3 x 4 is twelve.\nMEMORY: has a dog named Kutta"

    monkeypatch.setattr(m.tutor, "ask", fake_ask)
    r = client.post("/api/profile", json={
        "name": "Memor", "grade": 2, "parent_pin": "1234"})
    pid = r.json()["pid"]
    rc = client.post("/api/chat", json={"pid": pid, "message": "my dog Kutta is funny"})
    assert rc.status_code == 200
    data = rc.json()
    assert "MEMORY" not in data["answer"]
    assert data["memory_saved"] == "has a dog named Kutta"
    prof = client.get(f"/api/profile/{pid}").json()["profile"]
    assert "has a dog named Kutta" in prof["memories"]


def test_memory_line_case_insensitive(monkeypatch):
    import app.main as m

    def fake_ask(**kw):
        return "Okay! memory: loves football"

    monkeypatch.setattr(m.tutor, "ask", fake_ask)
    r = client.post("/api/profile", json={
        "name": "Memor2", "grade": 3, "parent_pin": "1234"})
    pid = r.json()["pid"]
    rc = client.post("/api/chat", json={"pid": pid, "message": "I love football"})
    data = rc.json()
    assert "memory" not in data["answer"].lower()
    assert data["memory_saved"] == "loves football"
