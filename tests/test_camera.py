"""Stage 3 — camera homework helper (app/camera.py). Offline tests."""
import base64
import pytest
from app import camera


def _png() -> bytes:
    # minimal 1x1 red PNG (valid magic bytes)
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8"
        "AAAAMBAQAY3Y2wAAAAAElFTkSuQmCC")


def test_decode_valid_png_with_mime_lie():
    raw, mime = camera.decode_image(base64.b64encode(_png()).decode(),
                                    "image/jpeg")   # gallery lies
    assert mime == "image/png"
    assert raw[:4] == b"\x89PNG"


def test_decode_data_url_prefix_stripped():
    b64 = "data:image/png;base64," + base64.b64encode(_png()).decode()
    raw, mime = camera.decode_image(b64, None)
    assert mime == "image/png"


def test_decode_garbage_raises():
    with pytest.raises(ValueError):
        camera.decode_image(base64.b64encode(b"not an image at all").decode(),
                            None)


def test_decode_oversize_raises():
    big = b"\x89PNG\r\n" + b"\x00" * (camera.MAX_PHOTO_BYTES + 1)
    with pytest.raises(OverflowError):
        camera.decode_image(base64.b64encode(big).decode(), "image/png")


def test_album_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(camera, "DATA_DIR", tmp_path)
    rec = camera.save_photo("kid-1", _png(), "image/png", note="hello")
    assert rec["note"] == "hello"
    album = camera.album("kid-1")
    assert len(album) == 1 and album[0]["id"] == rec["id"]
    camera.update_answer("kid-1", rec["id"], "great work")
    assert camera.album("kid-1")[0]["answer"] == "great work"


def test_photo_path_traversal_safe(tmp_path, monkeypatch):
    monkeypatch.setattr(camera, "DATA_DIR", tmp_path)
    camera.save_photo("kid-2", _png(), "image/png")
    fname = camera.album("kid-2")[0]["file"]
    assert camera.photo_path("kid-2", fname) is not None
    assert camera.photo_path("kid-2", "../../secrets.json") is None
    assert camera.photo_path("kid-2", "nope.jpg") is None
    # a dirty pid resolves to the SAME sanitized folder it was saved under
    camera.save_photo("ki d/2", _png(), "image/png")
    dirty_fname = camera.album("kid2")[0]["file"]
    assert camera.photo_path("kid2", dirty_fname) is not None


def test_album_capped_at_100(tmp_path, monkeypatch):
    monkeypatch.setattr(camera, "DATA_DIR", tmp_path)
    for _ in range(105):
        camera.save_photo("kid-3", _png(), "image/png")
    assert len(camera.album("kid-3")) == 100
