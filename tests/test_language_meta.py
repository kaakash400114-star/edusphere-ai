"""Stage 2 extras: meta-narration strip + language-directive wiring."""
from app import language, tutor


def test_strip_meta_leading_narration():
    assert tutor._strip_meta(
        "Sure! Let me try that again with shorter sentences. The sky is blue."
    ) == "The sky is blue."


def test_strip_meta_variants():
    for lead in ("Okay, here is a simpler version. Water boils at 100 degrees.",
                 "I'll explain simply. Plants need sunlight.",
                 "Certainly! Gravity pulls things down.",
                 "Trying again: two plus two is four."):
        out = tutor._strip_meta(lead)
        assert not out.lower().startswith(("sure", "okay", "here", "i'll",
                                           "certainly", "trying")), lead


def test_strip_meta_keeps_normal_answers():
    a = "Let's count the apples together! One, two, three!"
    assert tutor._strip_meta(a) == a


def test_strip_meta_two_lines():
    out = tutor._strip_meta("Sure. Okay, let me rewrite that. The answer is 4.")
    assert out == "The answer is 4."


def test_criticism_has_no_meta_leak():
    r = language.lint("This is an extraordinarily long sentence with "
                      "numerous elaborate polysyllabic words everywhere "
                      "making everything incomprehensible.", 1)
    c = language.criticism(r["violations"], 1)
    assert "never mention" in c.lower()


def test_directive_hard_for_primary():
    for g in (0, 1, 2, 3, 5):
        assert "MUST" in language.language_directive(g)
    assert "MUST" not in language.language_directive(11)
