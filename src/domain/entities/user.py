"""Entidades de autenticação."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class UserRole(StrEnum):
    """Papéis reconhecidos pela aplicação."""

    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


@dataclass(frozen=True, slots=True)
class User:
    """Representa um usuário autenticável."""

    id: str
    email: str
    role: UserRole


@dataclass(frozen=True, slots=True)
class UserSession:
    """Representa uma sessão autenticada e temporária."""

    token: str
    user_id: str
    expires_at: datetime
