"""Testes dos módulos de segurança adicionados na Fase 2."""

from io import BytesIO

import pandas as pd
import pytest

from core.exceptions import ValidationError
from security.anonymizer import anonymize_dataframe, detect_sensitive_columns
from security.auth import AuthService, hash_password, verify_password
from security.rbac import Role, has_permission
from security.upload import UploadRateLimiter, validate_upload_file


class NamedBytesIO(BytesIO):
    """Buffer em memória com atributos de upload do Streamlit."""

    def __init__(self, content: bytes, name: str) -> None:
        super().__init__(content)
        self.name = name
        self.size = len(content)


def test_password_hash_roundtrip() -> None:
    password_hash = hash_password("senha-segura")

    assert verify_password("senha-segura", password_hash) is True
    assert verify_password("senha-errada", password_hash) is False


def test_auth_service_register_and_authenticate(tmp_path) -> None:
    service = AuthService(tmp_path / "security.db")
    service.register_user(
        "Analista", "analista@example.com", "senha12345", Role.ANALYST
    )

    session = service.authenticate("analista@example.com", "senha12345")

    assert session is not None
    assert session.user.role == Role.ANALYST
    assert service.validate_session(session.token) is not None


def test_rbac_hierarchy() -> None:
    assert has_permission(Role.ADMIN, Role.VIEWER) is True
    assert has_permission(Role.ANALYST, Role.ADMIN) is False


def test_detect_and_anonymize_sensitive_columns() -> None:
    df = pd.DataFrame(
        {
            "nome": ["Maria"],
            "email": ["maria@example.com"],
            "cpf_cliente": ["123.456.789-10"],
        }
    )

    sensitive_columns = detect_sensitive_columns(df)
    anonymized = anonymize_dataframe(df, sensitive_columns)

    assert set(sensitive_columns) == {"email", "cpf_cliente"}
    assert anonymized.loc[0, "email"] == "[ANONIMIZADO]"


def test_validate_upload_rejects_formula_injection() -> None:
    upload = NamedBytesIO(b"nome,valor\nMaria,=cmd|' /C calc'!A0\n", "dados.csv")

    with pytest.raises(ValidationError):
        validate_upload_file(upload)


def test_upload_rate_limiter_blocks_after_limit() -> None:
    limiter = UploadRateLimiter(max_uploads=2, window_minutes=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False


def test_validate_upload_accepts_parquet_magic_bytes() -> None:
    upload = NamedBytesIO(b"PAR1conteudo-minimo", "dados.parquet")

    validate_upload_file(upload)
