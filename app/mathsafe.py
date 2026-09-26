"""MathSafe (Stage 5) — the tutor's CALCULATOR, never the LLM's guess.

Khanmigo's core insight: genAI predicts numbers, it does not compute them.
Every arithmetic computation in a tutor answer is verified here:

  extract_expressions(text) -> arithmetic expressions found in prose
  compute(expr)             -> safe AST-evaluated result (no eval())
  verify_text(text)         -> (ok, corrections) for an answer draft
  check_numeric_answer(question, claimed) -> ground truth for a sum

Grammar (intentionally small): + - * / × ÷ ^ % of, parentheses,
decimals, negatives, thousand separators. Everything else is ignored.
"""
from __future__ import annotations

import ast
import operator
import re

MAX_VALUE = 10 ** 15

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg, ast.UAdd: operator.pos,
        ast.FloorDiv: operator.floordiv}

# "12 + 23", "3.5 × 4", "2^10", "(1/2) of 8" ...
_EXPR_RE = re.compile(
    r"""
    (?:(?P<of>\bof\b)?\s*)?                  # "of" multiplier word
    (?P<expr>
        (?:[\(]?\s*-?\d+(?:,\d{3})*(?:\.\d+)?\s*[\)]?)          # first number
        (?:\s*[\+\-\*×÷x/^%]\s*[\(]?\s*-?\d+(?:,\d{3})*(?:\.\d+)?\s*[\)]?)+
    )
    """,
    re.VERBOSE,
)

_EQ_RE = re.compile(
    r"(?P<lhs>[\d\.\s\+\-\*×÷x/^%\(i\)]+?)"
    r"\s*(?:=|equals|is equal to)\s*(?P<rhs>-?\d+(?:,\d{3})*(?:\.\d+)?)",
    re.I,
)


def _normalize(expr: str) -> str:
    e = expr.lower()
    e = e.replace("×", "*").replace("÷", "/").replace("^", "**")
    e = re.sub(r"\bof\b", "*", e)
    e = e.replace(",", "")
    e = re.sub(r"(\d)\s*x\s*(\d)", r"\1*\2", e)
    return e


class _Eval(ast.NodeVisitor):
    def visit(self, node):  # noqa: D102
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        if isinstance(node, ast.BinOp):
            fn = _OPS.get(type(node.op))
            if fn is None:
                raise ValueError("bad operator")
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(node.op, ast.Pow) and (
                    abs(left) > 200 or abs(right) > 20):
                raise ValueError("power too large")
            val = fn(left, right)
            if not isinstance(val, (int, float)) or abs(val) > MAX_VALUE:
                raise ValueError("value too large")
            return val
        if isinstance(node, ast.UnaryOp):
            fn = _OPS.get(type(node.op))
            if fn is None:
                raise ValueError("bad unary")
            return fn(self.visit(node.operand))
        if isinstance(node, ast.Constant) and isinstance(node.value,
                                                         (int, float)):
            return node.value
        raise ValueError("unsupported token")


def compute(expr: str) -> float | None:
    """Safely evaluate one arithmetic expression. None if not evaluable."""
    norm = _normalize(expr.strip())
    if not re.fullmatch(r"[-\d\.\,\s\(\)\*\+/%%]+", norm):
        return None
    try:
        tree = ast.parse(norm, mode="eval")
        return _Eval().visit(tree)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        return None


def _fmt(val: float) -> str:
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return f"{val:g}"


def extract_expressions(text: str) -> list[tuple[str, float | None]]:
    """All bare-arithmetic snippets in the text with computed truth."""
    # remove code blocks: they are allowed to compute things themselves
    cleaned = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    cleaned = re.sub(r"`[^`\n]*`", " ", cleaned)   # inline code too
    found: list[tuple[str, float | None]] = []
    seen: set[str] = set()
    for m in _EXPR_RE.finditer(cleaned):
        raw = m.group("expr").strip()
        if raw.lower() in seen or len(raw) < 3:
            continue
        seen.add(raw.lower())
        found.append((raw, compute(raw)))
    return found


def verify_text(text: str) -> tuple[bool, list[str], list[tuple[int, int, str]]]:
    """Check every arithmetic claim. Returns (all_ok, corrections, spans).

    Each span is (start, end, correct_value_string) pointing at the WRONG
    claimed number inside `text` — precise enough to patch safely.
    """
    problems: list[str] = []
    spans: list[tuple[int, int, str]] = []
    hay = text or ""
    for raw, truth in extract_expressions(hay):
        if truth is None:
            continue
        tail_idx = hay.lower().find(raw.lower())
        if tail_idx == -1:
            continue
        tail_start = tail_idx + len(raw)
        tail = hay[tail_start: tail_start + 40]
        m = re.search(r"(?P<pre>\s*(?:is|:|=|equals|gives|makes|get)\s*)"
                      r"(?P<num>-?\d+(?:,\d{3})*(?:\.\d+)?)", tail, re.I)
        if not m:
            continue
        claimed = m.group("num").replace(",", "")
        try:
            claimed_val = float(claimed)
        except ValueError:
            continue
        if abs(claimed_val - truth) > 1e-9:
            s = tail_start + m.start("num")
            e = tail_start + m.end("num")
            problems.append(
                f"{raw} = {_fmt(truth)}, but the text says "
                f"{_fmt(claimed_val)}")
            spans.append((s, e, _fmt(truth)))
    return (not problems, problems, spans)


def _patch_claims(text: str, spans: list[tuple[int, int, str]]) -> str:
    """Rewrite wrong numeric claims at their exact spans (right-to-left)."""
    for s, e, truth in sorted(spans, reverse=True):
        text = text[:s] + truth + text[e:]
    return text


def guard(text: str, grade: int) -> tuple[str, dict]:
    """Full Stage-5 gate: verify + auto-patch arithmetic in a draft.

    Returns (final_text, meta). Never raises.
    """
    meta: dict = {"checked": 0, "fixed": 0, "problems": []}
    try:
        ok, problems, spans = verify_text(text)
        meta["checked"] = len(extract_expressions(text))
        if ok:
            return text, meta
        meta["problems"] = problems
        patched = _patch_claims(text, spans)
        ok2, problems2, _ = verify_text(patched)
        if ok2:
            meta["fixed"] = len(problems)
            return patched, meta
        # still wrong: let the tutor rewrite itself
        fix_note = "; ".join(problems2[:3])
        rewrite = (
            "Your reply contains arithmetic mistakes: " + fix_note +
            ". Recompute every calculation carefully step by step and "
            "resend ONLY the corrected reply in character.")
        meta["rewrite_prompt"] = rewrite
        return text, meta
    except Exception:            # math guarding must never break chat
        return text, meta


def answer_check(question: str, claimed: str) -> str | None:
    """If the question is a single sum and the answer claims a value,
    return the ground-truth answer (else None)."""
    q = (question or "").strip().rstrip("?!. ")
    exprs = extract_expressions(q)
    if len(exprs) == 1 and exprs[0][1] is not None:
        return _fmt(exprs[0][1])
    # "what is 12 plus 23" word form
    m = re.search(r"(-?\d+(?:,\d{3})*(?:\.\d+)?)\s*(plus|minus|times|multiplied by|"
                  r"divided by)\s*(-?\d+(?:,\d{3})*(?:\.\d+)?)",
                  question or "", re.I)
    if m:
        word = m.group(2).lower()
        op = {"plus": "+", "minus": "-", "times": "*",
              "multiplied by": "*", "divided by": "/"}[word]
        val = compute(f"{m.group(1)} {op} {m.group(3)}")
        if val is not None:
            return _fmt(val)
    return None
