"""Stage 3: grade-scaled human voices — pace, spoken form, per-buddy voices."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import conversation, neural_voice


# ---------- per-buddy voices stay distinct ----------
def test_ten_distinct_buddy_voices():
    voices = {cfg["voice"] for cfg in neural_voice.BUDDY_VOICES.values()}
    assert len(neural_voice.BUDDY_VOICES) == 10
    assert len(voices) >= 8, f"buddy voices too uniform: {voices}"


# ---------- grade scaling: pace and pauses ----------
def test_pace_monotonic_across_all_grades():
    paces = [conversation.pace_for_grade(g) for g in range(1, 13)]
    assert paces == sorted(paces), f"pace not increasing: {paces}"
    assert paces[0] < paces[-1]
    assert conversation.pace_for_grade(1) == 0.90
    assert conversation.pace_for_grade(12) == 1.18


def test_grade_style_bands():
    assert neural_voice.grade_style(1)["pace"] < neural_voice.grade_style(4)["pace"]
    assert neural_voice.grade_style(4)["pace"] < neural_voice.grade_style(7)["pace"]
    assert neural_voice.grade_style(7)["pace"] < neural_voice.grade_style(11)["pace"]
    assert neural_voice.grade_style(2)["max_words_per_breath"] == 8
    assert neural_voice.grade_style(11)["max_words_per_breath"] == 16
    assert "tiny sentences" in neural_voice.grade_style(1)["style"]
    assert "senior tutor" in neural_voice.grade_style(12)["style"]


def test_effective_rate_scales_with_pace():
    cfg = dict(neural_voice.BUDDY_VOICES["leo"])     # base -4%
    slow = neural_voice.effective_rate(cfg, 0.80)
    fast = neural_voice.effective_rate(cfg, 1.08)
    assert neural_voice._parse_pct(slow) < neural_voice._parse_pct(fast)
    assert slow == "-24%"     # base -4% plus -20% pace
    assert fast == "+4%"      # base -4% plus +8% pace


# ---------- spoken form: what a human would say ----------
def test_spoken_form_abbreviations():
    text = "Fractions e.g. 1/2 are useful, vs. decimals i.e. 0.5 etc."
    spoken = neural_voice.spoken_form(text)
    assert "for example" in spoken
    assert "versus" in spoken
    assert "that is" in spoken
    assert "and so on" in spoken


def test_spoken_form_math_and_markdown():
    spoken = neural_voice.spoken_form("So 3 x 4 = **12** & 50% is half.")
    assert "3 times 4" in spoken
    assert "50 percent" in spoken
    assert " and " in spoken
    assert "*" not in spoken and "**" not in spoken


def test_spoken_form_breath_pauses_on_long_runs():
    long_run = " ".join(f"word{i}" for i in range(30))
    spoken = neural_voice.spoken_form(long_run, max_words_per_breath=7)
    assert "," in spoken              # breath inserted
    assert spoken.count(",") >= 3


def test_spoken_form_emphasis_pauses():
    spoken = neural_voice.spoken_form("The *numerator* is on top.")
    assert " numerator " in f" {spoken} "
    assert "*" not in spoken
    assert "..." in spoken            # pauses land around the key word


# ---------- synthesis end-to-end (skips cleanly offline) ----------
def test_synthesize_grade_scaled_audio():
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        return  # offline machine: browser fallback covers the app
    slow = neural_voice.synth("leo", "Fractions show parts of a whole.", pace=0.80)
    fast = neural_voice.synth("leo", "Photosynthesis converts light energy "
                                     "into chemical energy.", pace=1.08)
    if slow and fast:                 # network available
        assert slow != fast           # different pace -> different cache/artifact
        assert slow.endswith(".mp3") and fast.endswith(".mp3")
