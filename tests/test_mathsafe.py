"""Stage 5 — MathSafe: verified calculator, never-trust-the-LLM arithmetic."""
from app import mathsafe


def test_compute_basics():
    assert mathsafe.compute("12 + 23") == 35
    assert mathsafe.compute("3.5 × 4") == 14.0
    assert mathsafe.compute("2^10") == 1024
    assert mathsafe.compute("(1/2) of 8") == 4.0
    assert mathsafe.compute("1,200 + 800") == 2000
    assert mathsafe.compute("7 ÷ 0") is None
    assert mathsafe.compute("import os") is None


def test_verify_good_draft():
    t = "Add the ones: 2 + 3 is 5. So 12 + 23 = 35!"
    ok, problems, _ = mathsafe.verify_text(t)
    assert ok and not problems


def test_verify_wrong_claim():
    t = "12 + 23 = 36!"
    ok, problems, spans = mathsafe.verify_text(t)
    assert not ok
    assert any("36" in p for p in problems)
    assert spans[0][2] == "35"


def test_guard_patches_and_keeps_punctuation():
    t = "First 12 + 23 = 35. Then 34 + 15 = 50. And 7 + 8 = 16, wow!"
    patched, meta = mathsafe.guard(t, 3)
    assert "34 + 15 = 49" in patched
    assert "7 + 8 = 15, wow!" in patched       # comma preserved
    assert meta["fixed"] == 2


def test_guard_clean_text_untouched():
    t = "Nothing numeric is wrong here: 5 + 5 = 10."
    patched, meta = mathsafe.guard(t, 2)
    assert patched == t and meta["fixed"] == 0


def test_answer_check_word_and_symbol():
    assert mathsafe.answer_check("What is 12 plus 23?", "") == "35"
    assert mathsafe.answer_check("9 x 7", "") == "63"


def test_guard_never_raises_on_garbage():
    for bad in ("", None, "###", "x = 42 for i in range(10)"):
        try:
            out, meta = mathsafe.guard(bad, 2)
            assert isinstance(meta, dict)
        except Exception as e:                   # pragma: no cover
            raise AssertionError(f"raised on {bad!r}: {e}")


def test_extract_ignores_code_blocks():
    t = "Run `print(2+2)` or:\n```python\nx = 2 + 2\n```\n2 + 2 is 4."
    ok, _, _ = mathsafe.verify_text(t)
    assert ok
