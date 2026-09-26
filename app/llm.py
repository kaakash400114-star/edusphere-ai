"""Multi-provider LLM adapter for EduSphere AI.

Supports any OpenAI-compatible API (GLM/Z.AI default, OpenAI, Mistral,
Together, Ollama local, Groq, Perplexity), plus Anthropic Claude natively.

Configuration (environment variables):
  EDUSPHERE_PROVIDER   = glm | openai | anthropic | ollama | groq | auto
  GLM_API_KEY          = your Z.AI key (default provider)
  GLM_BASE_URL         = https://api.z.ai/api/coding/paas/v4
  OPENAI_API_KEY       = your OpenAI key
  OPENAI_BASE_URL      = https://api.openai.com/v1  (or any compatible)
  ANTHROPIC_API_KEY    = your Anthropic key
  OLLAMA_BASE_URL      = http://localhost:11434/v1   (local Ollama)
  GROQ_API_KEY         = your Groq key
  EDUSPHERE_MODEL      = model name override (default: auto-selects best free)

The adapter presents ONE interface to tutor.py and knowledge_fresh.py:
  complete(messages, max_tokens, temperature, timeout) -> str
  quick(prompt, max_tokens, temperature, timeout) -> str   (single-turn)
"""
from __future__ import annotations

import os
import time
from typing import Any

import httpx

# ── Provider resolution ────────────────────────────────────────────────────────

def _resolve_provider() -> str:
    prov = os.environ.get("EDUSPHERE_PROVIDER", "").strip().lower()
    if prov and prov != "auto":
        return prov
    # auto-detect by which key is present
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if os.environ.get("OLLAMA_BASE_URL"):
        return "ollama"
    # default: Z.AI / GLM (the original EduSphere backend)
    return "glm"


_PROVIDER_DEFAULTS: dict[str, dict] = {
    "glm": {
        "base_url": "https://api.z.ai/api/coding/paas/v4",
        "model":    "glm-4.5-flash",
        "key_env":  "GLM_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model":    "gpt-4o-mini",
        "key_env":  "OPENAI_API_KEY",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model":    "llama-3.1-8b-instant",
        "key_env":  "GROQ_API_KEY",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model":    "llama3.2",
        "key_env":  None,                 # Ollama needs no key
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "model":    "mistral-small-latest",
        "key_env":  "MISTRAL_API_KEY",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "model":    "meta-llama/Llama-3-8b-chat-hf",
        "key_env":  "TOGETHER_API_KEY",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "model":    "claude-haiku-3-5",
        "key_env":  "ANTHROPIC_API_KEY",
    },
}


def _cfg() -> dict:
    """Resolve the active provider configuration."""
    prov = _resolve_provider()
    defaults = _PROVIDER_DEFAULTS.get(prov, _PROVIDER_DEFAULTS["glm"])
    # Environment can override base_url and model
    base_url = (
        os.environ.get("OPENAI_BASE_URL", "")
        or os.environ.get("GLM_BASE_URL", "")
        or os.environ.get("OLLAMA_BASE_URL", "")
        or defaults["base_url"]
    ).rstrip("/")
    model = os.environ.get("EDUSPHERE_MODEL", "") or defaults["model"]
    key_env = defaults.get("key_env")
    api_key = os.environ.get(key_env, "") if key_env else "ollama"
    return {"provider": prov, "base_url": base_url, "model": model,
            "api_key": api_key}


# ── OpenAI-compatible (GLM, OpenAI, Groq, Mistral, Together, Ollama) ──────────

def _oai_complete(cfg: dict, messages: list[dict], max_tokens: int,
                  temperature: float, timeout: float,
                  extra: dict | None = None) -> tuple[str, object]:
    """POST to any OpenAI-compatible /chat/completions."""
    body: dict[str, Any] = {
        "model": cfg["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if extra:
        body.update(extra)
    headers = {"Authorization": f"Bearer {cfg['api_key']}",
               "Content-Type": "application/json"}
    try:
        r = httpx.post(f"{cfg['base_url']}/chat/completions",
                       headers=headers, json=body, timeout=timeout)
        if r.status_code == 429:
            return "", "rate-limited"
        data = r.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or ""
        text = content.strip() or (reasoning[:2000] if reasoning else "")
        return text, None
    except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
        return "", exc


# ── Anthropic-native ───────────────────────────────────────────────────────────

def _anthropic_complete(cfg: dict, messages: list[dict], max_tokens: int,
                        temperature: float, timeout: float) -> tuple[str, object]:
    """POST to Anthropic Messages API."""
    # Separate system message from turns
    system = ""
    turns = []
    for m in messages:
        if m["role"] == "system":
            system = m["content"]
        else:
            turns.append(m)

    body: dict[str, Any] = {
        "model": cfg["model"],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": turns,
    }
    if system:
        body["system"] = system

    headers = {
        "x-api-key": cfg["api_key"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        r = httpx.post(f"{cfg['base_url']}/messages",
                       headers=headers, json=body, timeout=timeout)
        if r.status_code == 429:
            return "", "rate-limited"
        data = r.json()
        text = (data.get("content") or [{}])[0].get("text", "").strip()
        return text, None
    except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
        return "", exc


# ── Public interface ───────────────────────────────────────────────────────────

def complete(messages: list[dict], max_tokens: int = 3000,
             temperature: float = 0.4, timeout: float = 90.0,
             extra: dict | None = None) -> tuple[str, object]:
    """One completion call with automatic retries.

    Returns (content: str, error: Any).  error is None on success.
    """
    cfg = _cfg()
    if not cfg["api_key"] or cfg["api_key"] == "":
        return "", "no API key configured"

    for attempt in range(2):
        if cfg["provider"] == "anthropic":
            text, err = _anthropic_complete(cfg, messages, max_tokens,
                                            temperature, timeout)
        else:
            # GLM/OpenAI-compatible — pass GLM-specific thinking disable when on GLM
            ex = extra or {}
            if cfg["provider"] == "glm":
                ex = {"thinking": {"type": "disabled"}, **ex}
            text, err = _oai_complete(cfg, messages, max_tokens,
                                      temperature, timeout, ex)
        if text:
            return text, None
        if err == "rate-limited":
            time.sleep(2.0 * (attempt + 1))
        else:
            time.sleep(1.5 * (attempt + 1))

    return "", err


def quick(prompt: str, max_tokens: int = 400,
          temperature: float = 0.0, timeout: float = 45.0) -> tuple[str, object]:
    """Single-turn quick call (for self-review, validators, etc.)."""
    return complete([{"role": "user", "content": prompt}],
                    max_tokens=max_tokens, temperature=temperature,
                    timeout=timeout)


def model_name() -> str:
    """Return the currently active model name (for diagnostics)."""
    return _cfg()["model"]


def provider_name() -> str:
    """Return the currently active provider name (for diagnostics)."""
    return _cfg()["provider"]


def is_configured() -> bool:
    """True if at least one API key / provider is available."""
    cfg = _cfg()
    return bool(cfg["api_key"]) or cfg["provider"] == "ollama"
