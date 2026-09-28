"""Multi-provider LLM adapter for EduSphere AI.

Supports any OpenAI-compatible API (GLM/Z.AI default, Google Gemini, OpenAI, Mistral,
Together, Ollama local, Groq, Perplexity), plus Anthropic Claude natively.

Configuration (environment variables):
  EDUSPHERE_PROVIDER   = gemini | glm | openai | anthropic | ollama | groq | auto
  GEMINI_API_KEY       = your Google AI Studio / Gemini key
  GEMINI_BASE_URL      = https://generativelanguage.googleapis.com/v1beta/openai
  GLM_API_KEY          = your Z.AI key (default provider)
  GLM_BASE_URL         = https://api.z.ai/api/coding/paas/v4
  OPENAI_API_KEY       = your OpenAI key
  OPENAI_BASE_URL      = https://api.openai.com/v1  (or any compatible)
  ANTHROPIC_API_KEY    = your Anthropic key
  OLLAMA_BASE_URL      = http://localhost:11434/v1   (local Ollama)
  GROQ_API_KEY         = your Groq key
  EDUSPHERE_MODEL      = model name override (default: auto-selects best free)

The adapter presents ONE unified interface to tutor.py, camera.py, and knowledge_fresh.py:
  complete(messages, max_tokens, temperature, timeout) -> tuple[str, Any]
  complete_stream(messages, max_tokens, temperature, timeout) -> Iterator[str]
  quick(prompt, max_tokens, temperature, timeout) -> tuple[str, Any]
"""
from __future__ import annotations

import json
import os
import re
import time
from typing import Any, Iterator

import httpx

# Shared HTTP client for connection pooling
_HTTP_CLIENT: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _HTTP_CLIENT
    if _HTTP_CLIENT is None or _HTTP_CLIENT.is_closed:
        _HTTP_CLIENT = httpx.Client(timeout=90.0, follow_redirects=True)
    return _HTTP_CLIENT


# ── Provider resolution ────────────────────────────────────────────────────────

def _resolve_provider() -> str:
    prov = os.environ.get("EDUSPHERE_PROVIDER", "").strip().lower()
    if prov and prov != "auto":
        return prov
    # auto-detect by which key is present
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if os.environ.get("OLLAMA_BASE_URL"):
        return "ollama"
    if os.environ.get("GLM_API_KEY"):
        return "glm"
    # default fallback: glm (the original EduSphere backend)
    return "glm"


_PROVIDER_DEFAULTS: dict[str, dict] = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model":    "gemini-2.0-flash",
        "key_env":  "GEMINI_API_KEY",
    },
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
        "model":    "claude-3-5-haiku-20241022",
        "key_env":  "ANTHROPIC_API_KEY",
    },
}


def _cfg() -> dict:
    """Resolve the active provider configuration."""
    prov = _resolve_provider()
    defaults = _PROVIDER_DEFAULTS.get(prov, _PROVIDER_DEFAULTS["glm"])
    # Environment can override base_url and model
    base_url = (
        os.environ.get("GEMINI_BASE_URL", "")
        or os.environ.get("OPENAI_BASE_URL", "")
        or os.environ.get("GLM_BASE_URL", "")
        or os.environ.get("OLLAMA_BASE_URL", "")
        or defaults["base_url"]
    ).rstrip("/")
    model = os.environ.get("EDUSPHERE_MODEL", "") or defaults["model"]
    key_env = defaults.get("key_env")
    api_key = os.environ.get(key_env, "") if key_env else "ollama"
    return {"provider": prov, "base_url": base_url, "model": model,
            "api_key": api_key}


# ── OpenAI-compatible (Gemini, GLM, OpenAI, Groq, Mistral, Together, Ollama) ─

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
        client = _get_client()
        r = client.post(f"{cfg['base_url']}/chat/completions",
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


def _oai_stream(cfg: dict, messages: list[dict], max_tokens: int,
                temperature: float, timeout: float,
                extra: dict | None = None) -> Iterator[str]:
    """Stream from any OpenAI-compatible /chat/completions."""
    body: dict[str, Any] = {
        "model": cfg["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }
    if extra:
        body.update(extra)
    headers = {"Authorization": f"Bearer {cfg['api_key']}",
               "Content-Type": "application/json"}
    try:
        with httpx.stream("POST", f"{cfg['base_url']}/chat/completions",
                          headers=headers, json=body, timeout=timeout) as response:
            if response.status_code != 200:
                yield f"[Error: status {response.status_code}]"
                return
            for line in response.iter_lines():
                line = line.strip()
                if not line or not line.startswith("data:"):
                    continue
                data_str = line[5:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content") or ""
                    if content:
                        yield content
                except Exception:
                    continue
    except Exception as exc:
        yield f"[Connection error: {exc}]"


# ── Anthropic-native ───────────────────────────────────────────────────────────

def _format_anthropic_turns(messages: list[dict]) -> tuple[str, list[dict]]:
    system = ""
    turns = []
    for m in messages:
        if m["role"] == "system":
            system = m["content"]
        else:
            content = m.get("content")
            # Convert OpenAI vision structure to Anthropic if present
            if isinstance(content, list):
                adapted = []
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        url = part.get("image_url", {}).get("url", "")
                        match = re.match(r"^data:([^;]+);base64,(.+)$", url)
                        if match:
                            adapted.append({
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": match.group(1),
                                    "data": match.group(2),
                                },
                            })
                    else:
                        adapted.append(part)
                turns.append({"role": m["role"], "content": adapted})
            else:
                turns.append(m)
    return system, turns


def _anthropic_complete(cfg: dict, messages: list[dict], max_tokens: int,
                        temperature: float, timeout: float) -> tuple[str, object]:
    """POST to Anthropic Messages API."""
    system, turns = _format_anthropic_turns(messages)

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
        client = _get_client()
        r = client.post(f"{cfg['base_url']}/messages",
                        headers=headers, json=body, timeout=timeout)
        if r.status_code == 429:
            return "", "rate-limited"
        data = r.json()
        text = (data.get("content") or [{}])[0].get("text", "").strip()
        return text, None
    except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
        return "", exc


def _anthropic_stream(cfg: dict, messages: list[dict], max_tokens: int,
                      temperature: float, timeout: float) -> Iterator[str]:
    """Stream from Anthropic Messages API."""
    system, turns = _format_anthropic_turns(messages)
    body: dict[str, Any] = {
        "model": cfg["model"],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": turns,
        "stream": True,
    }
    if system:
        body["system"] = system
    headers = {
        "x-api-key": cfg["api_key"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        with httpx.stream("POST", f"{cfg['base_url']}/messages",
                          headers=headers, json=body, timeout=timeout) as response:
            if response.status_code != 200:
                yield f"[Error: status {response.status_code}]"
                return
            for line in response.iter_lines():
                line = line.strip()
                if not line or not line.startswith("data:"):
                    continue
                data_str = line[5:].strip()
                try:
                    event = json.loads(data_str)
                    if event.get("type") == "content_block_delta":
                        delta = event.get("delta", {})
                        if delta.get("type") == "text_delta":
                            text = delta.get("text", "")
                            if text:
                                yield text
                except Exception:
                    continue
    except Exception as exc:
        yield f"[Connection error: {exc}]"


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

    attempts = 4 if cfg["provider"] == "glm" else 2
    for attempt in range(attempts):
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
            # account-level concurrency limit: wait it out patiently
            time.sleep(min(12.0, 2.5 * (attempt + 1)))
        else:
            time.sleep(1.5 * (attempt + 1))

    return "", err


def complete_stream(messages: list[dict], max_tokens: int = 3000,
                    temperature: float = 0.4, timeout: float = 90.0,
                    extra: dict | None = None) -> Iterator[str]:
    """Stream token chunks from the active LLM provider."""
    cfg = _cfg()
    if not cfg["api_key"] or cfg["api_key"] == "":
        yield "Setup needed: no LLM API key is configured. Set GEMINI_API_KEY, GLM_API_KEY, or OPENAI_API_KEY."
        return

    if cfg["provider"] == "anthropic":
        yield from _anthropic_stream(cfg, messages, max_tokens, temperature, timeout)
    else:
        ex = extra or {}
        if cfg["provider"] == "glm":
            ex = {"thinking": {"type": "disabled"}, **ex}
        yield from _oai_stream(cfg, messages, max_tokens, temperature, timeout, ex)


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
