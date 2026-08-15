"""Serviço de autenticação em memória usado pela interface legada."""

import hashlib
import hmac
import os
import secrets
from datetime import UTC, datetime, timedelta

from src.domain.entities.user import User, UserRole, UserSession


class AuthService:
    """Mantém usuários demonstrativos e sessões curtas em memória."""

    def __init__(self) -> None:
        credentials = {
            "admin@smartdataanalyzer.dev": (
                "usr_admin_001",
                UserRole.ADMIN,
                os.getenv("DEMO_ADMIN_PASSWORD", "admin123"),
            ),
            "analyst@smartdataanalyzer.dev": (
                "usr_analyst_001",
                UserRole.ANALYST,
                os.getenv("DEMO_ANALYST_PASSWORD", "analyst123"),
            ),
            "viewer@smartdataanalyzer.dev": (
                "usr_viewer_001",
                UserRole.VIEWER,
                os.getenv("DEMO_VIEWER_PASSWORD", "viewer123"),
            ),
        }
        self._users: dict[str, tuple[User, str]] = {
            email: (User(user_id, email, role), self._digest(password))
            for email, (user_id, role, password) in credentials.items()
        }
        self._sessions: dict[str, UserSession] = {}

    @staticmethod
    def _digest(password: str) -> str:
        """Gera digest apenas para o modo demonstrativo compatível."""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, email: str, password: str) -> UserSession | None:
        """Autentica credenciais e cria uma sessão de trinta minutos."""
        record = self._users.get(email.strip().lower())
        if record is None or not hmac.compare_digest(record[1], self._digest(password)):
            return None
        token = secrets.token_urlsafe(32)
        session = UserSession(
            token, record[0].id, datetime.now(UTC) + timedelta(minutes=30)
        )
        self._sessions[token] = session
        return session

    def validate_session(self, token: str) -> User | None:
        """Retorna o usuário quando a sessão existe e não expirou."""
        session = self._sessions.get(token)
        if session is None or session.expires_at <= datetime.now(UTC):
            self._sessions.pop(token, None)
            return None
        return next(
            (user for user, _ in self._users.values() if user.id == session.user_id),
            None,
        )

    def check_permission(self, token: str, required_role: UserRole) -> bool:
        """Verifica a hierarquia de acesso da sessão."""
        user = self.validate_session(token)
        hierarchy = {UserRole.VIEWER: 1, UserRole.ANALYST: 2, UserRole.ADMIN: 3}
        return bool(user and hierarchy[user.role] >= hierarchy[required_role])

    def invalidate_session(self, token: str) -> None:
        """Invalida uma sessão existente."""
        self._sessions.pop(token, None)
