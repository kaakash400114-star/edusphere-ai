"""Stage 2 — grade-perfect language gate (app/language.py). Offline tests."""
from app import language


def test_band_limits_kinder_tiny():
    lim = language.band_limits(0)
    assert lim["max_words"] <= 9
    assert lim["hard"] is True


def test_band_limits_senior_loose():
    lim = language.band_limits(11)
    assert lim["max_words"] >= 30
    assert lim["hard"] is False


def test_lint_clean_short_answer_passes():
    a = "A triangle has three sides. Count them: one, two, three! " \
        "Can you find a triangle near you?"
    r = language.lint(a, 1)
    assert r["ok"] is True, r["violations"]


def test_lint_catches_long_sentences_for_little_kids():
    a = ("Photosynthesis is the remarkable biological process by which "
         "green plants manufacture carbohydrate molecules from carbon "
         "dioxide and water using chlorophyll and sunlight energy.")
    r = language.lint(a, 1)
    assert r["ok"] is False
    assert any("exceed" in v for v in r["violations"])


def test_lint_catches_hard_vocabulary_for_little_kids():
    # short-ish sentences but dense with 3+ syllable words
    a = ("Photosynthesis provides vegetation nourishment. "
         "Chlorophyll transforms luminosity. "
         "Carbohydrates constitute vegetation. "
         "Meanwhile organisms consume vegetables. "
         "Eventually photosynthesis energizes everybody. "
         "Subsequently chlorophyll deteriorates gradually. "
         "Nevertheless vegetation continues photosynthesizing.")
    r = language.lint(a, 2)
    assert any("long-word" in v for v in r["violations"])


def test_lint_senior_long_words_allowed():
    a = ("Photosynthesis converts carbon dioxide into glucose using "
         "chlorophyll. The light-dependent reactions occur in the "
         "thylakoid membranes. ATP and NADPH power the Calvin cycle.")
    r = language.lint(a, 10)
    assert r["ok"] is True, r["violations"]


def test_lint_markdown_and_code_ignored():
    a = "Do 2 plus 2.\n```python\nx = 2 + 2  # very long code line counts zero\n```\nThat makes 4!"
    r = language.lint(a, 1)
    assert r["ok"] is True, r["violations"]


def test_criticism_mentions_grade():
    r = language.lint("This is an extraordinarily long sentence with "
                      "numerous elaborate polysyllabic words everywhere "
                      "making everything incomprehensible.", 1)
    c = language.criticism(r["violations"], 1)
    assert "6-7 year old" in c
    assert "Rewrite" in c


def test_directive_contains_contract():
    d = language.language_directive(0)
    assert "LANGUAGE CONTRACT" in d
    assert "9 words" in d


def test_band_names_round_trip():
    for grade in range(0, 13):
        assert language.band_for(grade) in language.BANDS


def test_known_kid_words_not_penalized():
    # 'butterfly', 'elephant' are fine for grade 1
    a = ("A butterfly has four wings. An elephant has a long trunk. "
         "Together they are animals. Sometimes they play near water. "
         "Remember to look for them!")
    r = language.lint(a, 1)
    assert r["ok"] is True, r["violations"]
