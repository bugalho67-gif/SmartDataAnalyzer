"""Provedor Anthropic Claude via API REST."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from core.exceptions import AIError
from providers.base import BaseProvider, Message


class ClaudeProvider(BaseProvider):
    """Adapter mínimo para Claude sem dependências extras."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1024"))

    def chat(self, messages: list[Message]) -> str:
        """Envia mensagens para a Messages API da Anthropic."""
        if not self.api_key:
            raise AIError("Configure ANTHROPIC_API_KEY para usar Claude.")

        system_prompt, claude_messages = _split_system_messages(messages)
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": claude_messages,
        }
        if system_prompt:
            payload["system"] = system_prompt

        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise AIError("Erro ao consultar Claude.") from exc

        blocks = data.get("content", [])
        return (
            "\n".join(block.get("text", "") for block in blocks).strip()
            or "Sem resposta."
        )


def _split_system_messages(messages: list[Message]) -> tuple[str, list[Message]]:
    system_parts = [
        message["content"] for message in messages if message["role"] == "system"
    ]
    chat_messages = [message for message in messages if message["role"] != "system"]
    return "\n\n".join(system_parts), chat_messages