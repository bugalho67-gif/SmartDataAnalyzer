"""Provedor Google Gemini via API REST."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from core.exceptions import AIError
from providers.base import BaseProvider, Message


class GeminiProvider(BaseProvider):
    """Adapter mínimo para Gemini sem dependências extras."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    def chat(self, messages: list[Message]) -> str:
        """Envia mensagens para o endpoint generateContent do Gemini."""
        if not self.api_key:
            raise AIError("Configure GEMINI_API_KEY para usar o Gemini.")

        prompt = _messages_to_prompt(messages)
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
        query = urllib.parse.urlencode({"key": self.api_key})
        request = urllib.request.Request(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?{query}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise AIError("Erro ao consultar Gemini.") from exc

        candidates = data.get("candidates", [])
        if not candidates:
            return "Sem resposta."
        parts = candidates[0].get("content", {}).get("parts", [])
        return "\n".join(part.get("text", "") for part in parts).strip() or "Sem resposta."


def _messages_to_prompt(messages: list[Message]) -> str:
    return "\n\n".join(f"{message['role']}: {message['content']}" for message in messages)
