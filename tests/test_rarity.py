"""Stage F: sticker rarity milestones wired into level completion."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _mk(name="Rare", grade=6, **kw):
    r = client.post("/api/profile", json={
        "name": name, "grade": grade, "parent_pin": "1234", **kw})
    return r.json()["pid"]


def _complete_level(pid, level):
    lt = client.get(f"/api/levels/{pid}/{level}").json()
    for t in lt["tasks"]:
        r = client.post(f"/api/levels/{pid}/{level}/task",
                        json={"level": level, "task_id": t["id"], "score": 10})
        assert r.status_code == 200
    return r.json()["profile"]


def test_common_sticker_per_level():
    pid = _mk()
    prof = _complete_level(pid, 1)
    assert prof["stickers"].get("grade6_level1", 0) == 1


def test_rare_world_sticker_at_level_4():
    pid = _mk()
    # play L1, buy+play L2, L3, then L4 -> rare world sticker
    _complete_level(pid, 1)
    for lvl in (2, 3, 4):
        r = client.post(f"/api/levels/{pid}/buy", json={"level": lvl})
        assert r.status_code == 200, r.text
        _complete_level(pid, lvl)
    prof = client.get(f"/api/profile/{pid}").json()["profile"]
    rares = [k for k in prof["stickers"] if "rare" in k]
    assert rares, f"no rare sticker in {prof['stickers']}"
    assert prof["stickers"][rares[0]] == 1


def test_epic_grade_master_sticker_full_run():
    pid = _mk(name="Epic", grade=6)
    # play levels 1..7 legitimately by buying each next level after finishing
    for lvl in range(1, 8):
        if lvl > 1:
            r = client.post(f"/api/levels/{pid}/buy", json={"level": lvl})
            assert r.status_code == 200, r.text
        _complete_level(pid, lvl)
    prof = client.get(f"/api/profile/{pid}").json()["profile"]
    assert prof["stickers"].get("grade6_master_epic", 0) == 1
    epic_count = sum(1 for k in prof["stickers"] if k.endswith("_epic"))
    assert epic_count == 1
    # level stickers 1..7 all present
    for lvl in range(1, 8):
        assert f"grade6_level{lvl}" in prof["stickers"]
