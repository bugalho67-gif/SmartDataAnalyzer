"""Provedor para modelos locais servidos pelo Ollama."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from core.exceptions import AIError
from providers.base import BaseProvider, Message


class OllamaProvider(BaseProvider):
    """Adapter HTTP para a API local do Ollama."""

    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1")

    def chat(self, messages: list[Message]) -> str:
        """Envia mensagens para o endpoint `/api/chat` do Ollama."""
        payload = json.dumps(
            {"model": self.model, "messages": messages, "stream": False}
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise AIError("Não foi possível conectar ao Ollama local.") from exc

        return data.get("message", {}).get("content", "Sem resposta.")
