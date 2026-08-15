"""Primitivas de validação e limitação de requisições."""

import re
import time
from collections import defaultdict, deque
from pathlib import Path

from src.core.exceptions import FileUploadError

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "json", "parquet", "xml"}


def sanitize_column_name(name: str) -> str:
    """Normaliza um nome de coluna sem executar conteúdo fornecido."""
    normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip().lower()).strip("_")
    if not normalized:
        return "column"
    return f"col_{normalized}" if normalized[0].isdigit() else normalized


def validate_file_extension(filename: str) -> str:
    """Valida e retorna a extensão sem ponto."""
    extension = Path(filename).suffix.lower().lstrip(".")
    if extension not in ALLOWED_EXTENSIONS:
        raise FileUploadError("Formato de arquivo não permitido.")
    return extension


def validate_file_size(size_bytes: int, max_size_mb: int = 100) -> None:
    """Rejeita arquivos maiores que o limite configurado."""
    if size_bytes > max_size_mb * 1024**2:
        raise FileUploadError(f"O arquivo excede o limite de {max_size_mb} MB.")


class RateLimiter:
    """Limitador em memória por janela deslizante."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    def is_allowed(self, key: str) -> bool:
        """Informa se a chave ainda pode realizar uma requisição."""
        now = time.monotonic()
        requests = self._requests[key]
        while requests and now - requests[0] >= self.window_seconds:
            requests.popleft()
        if len(requests) >= self.max_requests:
            return False
        requests.append(now)
        return True

    def check_or_raise(self, key: str) -> None:
        """Gera erro quando a chave excede o limite."""
        if not self.is_allowed(key):
            raise RuntimeError("Limite de requisições excedido.")


_RATE_LIMITER = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Retorna o limitador compartilhado da aplicação."""
    return _RATE_LIMITER
