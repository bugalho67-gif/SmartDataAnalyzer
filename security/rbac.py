"""Controle de acesso baseado em papéis (RBAC)."""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    """Papéis disponíveis na aplicação."""

    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


_ROLE_LEVELS: dict[Role, int] = {
    Role.VIEWER: 1,
    Role.ANALYST: 2,
    Role.ADMIN: 3,
}


def normalize_role(role: Role | str) -> Role:
    """Normaliza uma string ou enum para um papel válido."""
    if isinstance(role, Role):
        return role
    return Role(str(role).lower())


def has_permission(user_role: Role | str, required_role: Role | str) -> bool:
    """Verifica se o papel do usuário atende ao nível mínimo exigido."""
    role = normalize_role(user_role)
    required = normalize_role(required_role)
    return _ROLE_LEVELS[role] >= _ROLE_LEVELS[required]
