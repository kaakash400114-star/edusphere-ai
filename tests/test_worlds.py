"""Worlds tests — grade-band routing only (no preschool lands)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app import worlds
from app.main import app

client = TestClient(app)


def test_grades_route_to_bands():
    assert worlds.resolve_world(1)["id"] == "village"
    assert worlds.resolve_world(2)["id"] == "village"
    assert worlds.resolve_world(3)["id"] == "mountains"
    assert worlds.resolve_world(5)["id"] == "mountains"
    assert worlds.resolve_world(6)["id"] == "academy"
    assert worlds.resolve_world(8)["id"] == "academy"
    assert worlds.resolve_world(9)["id"] == "tower"
    assert worlds.resolve_world(12)["id"] == "tower"


def test_five_worlds_kg_to_twelve():
    ids = {w["id"] for w in worlds.roster()}
    assert ids == {"meadow", "village", "mountains", "academy", "tower"}


def test_no_age_routing():
    # age argument is ignored; without a grade the default is grade 0 (meadow)
    assert worlds.resolve_world(None, 3)["id"] == "meadow"
    assert worlds.resolve_world(None, 10)["id"] == "meadow"
    assert worlds.resolve_world(10)["id"] == "tower"


def test_world_for_profile_uses_grade():
    p = {"grade": 2, "age": None}
    assert worlds.world_for_profile(p)["id"] == "village"


def test_worlds_api_for_profile():
    r = client.post("/api/profile", json={
        "name": "Worldy", "grade": 5, "parent_pin": "1234"})
    pid = r.json()["pid"]
    r2 = client.get(f"/api/worlds/for-profile/{pid}")
    assert r2.status_code == 200
    assert r2.json()["world"]["id"] == "mountains"
