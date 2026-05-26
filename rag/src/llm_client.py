"""Unified, beginner-friendly LLM wrapper.

Goals
-----
* One function:  ``ask_llm(prompt, model=None, system=None, ...)``  →  string answer
* Switch providers with one line in ``.env``: ``LLM_PROVIDER=openai|anthropic|google|mock``
* If no API key is configured, gracefully fall back to a **MOCK** mode so the
  rest of the lesson still runs.
"""
from __future__ import annotations

import json
import os
import textwrap
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Provider resolution
# ---------------------------------------------------------------------------
def _provider() -> str:
    p = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    # If user requested a real provider but the corresponding key is missing,
    # silently degrade to "mock" so notebooks still execute.
    if p == "openai" and not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        return "mock"
    if p == "anthropic" and not os.getenv("ANTHROPIC_API_KEY", "").startswith("sk-"):
        return "mock"
    if p == "google" and not os.getenv("GOOGLE_API_KEY"):
        return "mock"
    return p


def llm_status() -> dict:
    """Return a human-readable status dict — used by Notebook 00."""
    p = _provider()
    return {
        "provider": p,
        "model": _default_model(p),
        "is_mock": p == "mock",
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        "anthropic_key_set": bool(os.getenv("ANTHROPIC_API_KEY", "").strip()),
        "google_key_set": bool(os.getenv("GOOGLE_API_KEY", "").strip()),
    }


def _default_model(provider: str) -> str:
    return {
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        "google": os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"),
        "mock": "mock-llm",
    }[provider]


# ---------------------------------------------------------------------------
# Mock LLM (used when no key is set)
# ---------------------------------------------------------------------------
def _mock_answer(prompt: str, system: Optional[str] = None) -> str:
    """A deliberately obvious mock response. It echoes the input so participants
    can see the prompt is wired correctly, even without a real key."""
    snippet = textwrap.shorten(prompt.replace("\n", " "), width=240, placeholder=" ...")
    header = "[MOCK LLM — no API key configured. Returning a canned answer.]"
    if system:
        header += f"\n[system: {textwrap.shorten(system, width=120, placeholder=' ...')}]"
    return (
        f"{header}\n\n"
        f"You asked: {snippet}\n\n"
        "I cannot give a real answer because no API key is set. Set one in `.env` "
        "(OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY) and restart the "
        "notebook kernel."
    )


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------
def _ask_openai(prompt: str, model: str, system: Optional[str], temperature: float) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def _ask_anthropic(prompt: str, model: str, system: Optional[str], temperature: float) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system or "",
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    parts = [b.text for b in resp.content if getattr(b, "type", "") == "text"]
    return "\n".join(parts)


def _ask_google(prompt: str, model: str, system: Optional[str], temperature: float) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    full = (system + "\n\n" if system else "") + prompt
    m = genai.GenerativeModel(model)
    resp = m.generate_content(full, generation_config={"temperature": temperature})
    return getattr(resp, "text", "") or ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def ask_llm(
    prompt: str,
    model: Optional[str] = None,
    system: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """Send a prompt to the configured LLM and return the text answer.

    Parameters
    ----------
    prompt : str
        The user message.
    model : str, optional
        Override the provider's default model. Provider is selected from .env
        (``LLM_PROVIDER``); the ``model`` string is interpreted by that provider.
    system : str, optional
        Optional system message — e.g. "You are an experienced Nepali CA".
    temperature : float
        0.0 = deterministic; 1.0 = creative. Default 0.2 for factual tasks.
    """
    provider = _provider()
    model = model or _default_model(provider)
    if provider == "mock":
        return _mock_answer(prompt, system)
    try:
        if provider == "openai":
            return _ask_openai(prompt, model, system, temperature)
        if provider == "anthropic":
            return _ask_anthropic(prompt, model, system, temperature)
        if provider == "google":
            return _ask_google(prompt, model, system, temperature)
    except Exception as e:  # noqa: BLE001 — keep the notebook lesson alive
        return (
            f"[LLM ERROR — provider={provider}, model={model}]\n"
            f"{type(e).__name__}: {e}\n\n"
            "Falling back to the mock response so the lesson can continue:\n\n"
            + _mock_answer(prompt, system)
        )
    return _mock_answer(prompt, system)


def ask_llm_json(prompt: str, **kw) -> dict:
    """Same as ask_llm but tries to parse the response as JSON.

    Adds a short JSON-only instruction to the user prompt. If parsing fails,
    returns ``{"_raw": <text>, "_parse_error": <msg>}`` instead of raising,
    so the lesson keeps running.
    """
    instruction = (
        "Respond with **only** valid JSON. No commentary, no markdown fences. "
        "Use double quotes for strings."
    )
    full = f"{prompt}\n\n{instruction}"
    text = ask_llm(full, **kw)
    # strip common code-fence wrapping
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"_raw": text, "_parse_error": str(e)}
