"""Stage B: levels engine + curriculum feed + level API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import curriculum_feed, levels
from app.main import app

client = TestClient(app)


def _mk(name="Leveler", grade=3, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    assert r.status_code == 200, r.text
    return r.json()["pid"]


# ---------- engine rules ----------
def test_prices_and_names():
    assert levels.level_price(1) == 0
    assert levels.level_price(2) == 45
    assert levels.level_price(7) == 120
    assert len(levels.level_map(5)) == 7
    assert levels.level_map(5)[6]["name"] == "Legend"


def test_every_grade_all_levels_have_tasks():
    for g in range(1, 13):
        counts = [curriculum_feed.task_count(g, l) for l in range(1, 8)]
        assert all(c >= 1 for c in counts), f"grade {g} empty levels: {counts}"
        tasks = curriculum_feed.grade_tasks(g)
        assert all(t["points"] > 0 for t in tasks)


def test_task_ids_resolve():
    for g in (1, 6, 12):
        for t in curriculum_feed.grade_tasks(g):
            assert curriculum_feed.task_by_id(g, t["id"]) is not None


# ---------- API flow: play a whole level, buy the next ----------
def test_full_level_flow():
    pid = _mk("Flowy", 4)
    # level map: L1 unlocked, rest locked
    m = client.get(f"/api/levels/{pid}").json()
    assert m["points"] == 0
    assert m["levels"][0]["unlocked"] and not m["levels"][1]["unlocked"]

    # L1 task list exists
    lt = client.get(f"/api/levels/{pid}/1").json()
    tasks = lt["tasks"]
    assert len(tasks) >= 2

    # do all tasks of level 1
    for t in tasks:
        r = client.post(f"/api/levels/{pid}/1/task",
                        json={"level": 1, "task_id": t["id"], "score": 10})
        assert r.status_code == 200, r.text
    prof = r.json()["profile"]
    earned = 10 * len(tasks) + levels.LEVEL_BONUS
    assert prof["points"] == earned
    # level 1 completed -> sticker dropped
    assert prof["stickers"].get("grade4_level1", 0) == 1

    # buying level 3 early fails (level 2 not unlocked)
    r = client.post(f"/api/levels/{pid}/buy", json={"level": 3})
    assert r.status_code == 400

    # complete level 2 as well to prove sequencing
    r = client.post(f"/api/levels/{pid}/buy", json={"level": 2})
    assert r.status_code == 200
    spent = levels.level_price(2)
    assert r.json()["profile"]["points"] == earned - spent

    lt2 = client.get(f"/api/levels/{pid}/2").json()
    for t in lt2["tasks"]:
        client.post(f"/api/levels/{pid}/2/task",
                    json={"level": 2, "task_id": t["id"], "score": 10})

    # duplicate task rejected
    first = lt2["tasks"][0]
    r = client.post(f"/api/levels/{pid}/2/task",
                    json={"level": 2, "task_id": first["id"], "score": 10})
    assert r.status_code == 400

    # unknown task rejected
    r = client.post(f"/api/levels/{pid}/2/task",
                    json={"level": 2, "task_id": "nope", "score": 10})
    assert r.status_code == 400


def test_cannot_afford_level():
    pid = _mk("Broke", 5)
    r = client.post(f"/api/levels/{pid}/buy", json={"level": 2})
    assert r.status_code == 400
    assert "points" in r.json()["detail"]


def test_task_in_locked_level_rejected():
    pid = _mk("Locked", 6)
    lt = client.get(f"/api/levels/{pid}/4").json()
    t = lt["tasks"][0]
    r = client.post(f"/api/levels/{pid}/4/task",
                    json={"level": 4, "task_id": t["id"], "score": 10})
    assert r.status_code == 400
