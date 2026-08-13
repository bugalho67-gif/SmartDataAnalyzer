"""Validações de segurança para arquivos enviados pelo usuário."""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import BinaryIO

from core.exceptions import ValidationError

MAX_UPLOAD_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json", ".parquet", ".xml"}
BLOCKED_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".ps1", ".zip", ".js", ".py"}
DANGEROUS_PREFIXES = ("=", "+", "-", "@")

_MAGIC_BYTES: dict[str, tuple[bytes, ...]] = {
    ".csv": (b"",),
    ".json": (b"{", b"["),
    ".xlsx": (b"PK\x03\x04",),
    ".parquet": (b"PAR1",),
    ".xml": (b"<",),
}


class UploadRateLimiter:
    """Limita a quantidade de uploads por chave em uma janela de tempo."""

    def __init__(self, max_uploads: int = 5, window_minutes: int = 60) -> None:
        self.max_uploads = max_uploads
        self.window = timedelta(minutes=window_minutes)
        self._events: defaultdict[str, deque[datetime]] = defaultdict(deque)

    def is_allowed(self, key: str) -> bool:
        """Retorna se a chave ainda pode realizar upload."""
        now = datetime.now(UTC)
        events = self._events[key]
        while events and now - events[0] > self.window:
            events.popleft()
        if len(events) >= self.max_uploads:
            return False
        events.append(now)
        return True


upload_rate_limiter = UploadRateLimiter()


def validate_upload_file(file: BinaryIO, max_size_mb: int = MAX_UPLOAD_SIZE_MB) -> None:
    """Valida extensão, tamanho, magic bytes e conteúdo inicial do upload."""
    file_name = getattr(file, "name", "")
    extension = Path(file_name).suffix.lower()
    file_size = int(getattr(file, "size", 0))

    if extension in BLOCKED_EXTENSIONS or extension not in ALLOWED_EXTENSIONS:
        raise ValidationError("Formato de arquivo não permitido para upload.")

    if file_size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"O arquivo excede o limite de {max_size_mb} MB.")

    position = file.tell()
    head = file.read(4096)
    file.seek(position)

    if _looks_like_executable(head):
        raise ValidationError("Arquivo executável ou script rejeitado por segurança.")

    expected_headers = _MAGIC_BYTES[extension]
    if expected_headers != (b"",) and not head.lstrip().startswith(expected_headers):
        raise ValidationError("Assinatura do arquivo incompatível com a extensão informada.")

    if extension in {".csv", ".json", ".xml"} and has_formula_injection(head):
        raise ValidationError("Possível CSV/Formula Injection detectada no arquivo.")


def has_formula_injection(content: bytes) -> bool:
    """Detecta células iniciadas por caracteres perigosos em amostra textual."""
    text = content.decode("utf-8", errors="ignore")
    for line in text.splitlines():
        cells = [cell.strip().strip('"\'') for cell in line.split(",")]
        if any(cell.startswith(DANGEROUS_PREFIXES) for cell in cells if cell):
            return True
    return False


def _looks_like_executable(content: bytes) -> bool:
    signatures = (b"MZ", b"\x7fELF", b"#!/", b"<script")
    return content.lstrip().startswith(signatures)
