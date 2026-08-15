"""Autenticação local com hash de senha e sessão do Streamlit."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import streamlit as st

from app_config import BASE_DIR
from core.logger import logger
from security.rbac import Role, has_permission, normalize_role


DATABASE_PATH = BASE_DIR / "smartdata_security.db"
DEFAULT_SESSION_MINUTES = 30


@dataclass(frozen=True)
class User:
    """Representa um usuário autenticado na aplicação."""

    id: int
    username: str
    email: str
    role: Role
    accepted_terms: bool


@dataclass(frozen=True)
class Session:
    """Representa uma sessão autenticada."""

    token: str
    user: User
    expires_at: datetime


class AuthService:
    """Serviço de autenticação local persistido em SQLite."""

    def __init__(self, database_path: Path = DATABASE_PATH) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()
        self._ensure_default_admin()

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        role: Role | str = Role.VIEWER,
    ) -> User:
        """Registra um usuário com senha protegida por hash."""
        username = username.strip()
        email = email.strip().lower()
        if not username or not email or len(password) < 8:
            raise ValueError(
                "Informe nome, e-mail e senha com pelo menos 8 caracteres."
            )

        password_hash = hash_password(password)
        user_role = normalize_role(role)

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (username, email, password_hash, user_role.value),
            )
            connection.commit()
            user_id = int(cursor.lastrowid)

        logger.info("Usuário registrado: %s", email)
        return User(user_id, username, email, user_role, accepted_terms=False)

    def authenticate(self, email: str, password: str) -> Session | None:
        """Autentica usuário e cria sessão com expiração por inatividade."""
        user_row = self._get_user_row(email.strip().lower())
        if user_row is None or not verify_password(password, user_row["password_hash"]):
            logger.warning("Tentativa de login inválida para %s", email)
            return None

        user = _row_to_user(user_row)
        expires_at = datetime.now(UTC) + timedelta(minutes=DEFAULT_SESSION_MINUTES)
        token = secrets.token_urlsafe(32)

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO sessions (token, user_id, expires_at, last_activity)
                VALUES (?, ?, ?, ?)
                """,
                (token, user.id, expires_at.isoformat(), datetime.now(UTC).isoformat()),
            )
            connection.commit()

        logger.info("Login realizado: %s", user.email)
        return Session(token=token, user=user, expires_at=expires_at)

    def validate_session(self, token: str | None) -> User | None:
        """Valida uma sessão ativa e renova a expiração por inatividade."""
        if not token:
            return None

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT sessions.expires_at, users.*
                FROM sessions
                JOIN users ON users.id = sessions.user_id
                WHERE sessions.token = ?
                """,
                (token,),
            ).fetchone()

            if row is None:
                return None

            expires_at = datetime.fromisoformat(row["expires_at"])
            if expires_at <= datetime.now(UTC):
                connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
                connection.commit()
                return None

            new_expiration = datetime.now(UTC) + timedelta(
                minutes=DEFAULT_SESSION_MINUTES
            )
            connection.execute(
                "UPDATE sessions SET expires_at = ?, last_activity = ? WHERE token = ?",
                (new_expiration.isoformat(), datetime.now(UTC).isoformat(), token),
            )
            connection.commit()

        return _row_to_user(row)

    def logout(self, token: str | None) -> None:
        """Encerra a sessão atual."""
        if not token:
            return
        with self._connect() as connection:
            connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
            connection.commit()

    def accept_terms(self, user_id: int) -> None:
        """Marca o termo de consentimento LGPD como aceito pelo usuário."""
        with self._connect() as connection:
            connection.execute(
                "UPDATE users SET accepted_terms = 1 WHERE id = ?", (user_id,)
            )
            connection.commit()

    def current_user(self) -> User | None:
        """Obtém o usuário autenticado na sessão atual do Streamlit."""
        return self.validate_session(st.session_state.get("auth_token"))

    def require_role(self, required_role: Role) -> User | None:
        """Exige autenticação e um papel mínimo para continuar o fluxo."""
        user = self.current_user()
        if user is None:
            render_login_form(self)
            st.stop()

        if not has_permission(user.role, required_role):
            st.error("Você não possui permissão para acessar este recurso.")
            st.stop()

        return user

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'viewer',
                    accepted_terms INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    expires_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                """
            )
            connection.commit()

    def _ensure_default_admin(self) -> None:
        if self._get_user_row("admin@smartdataanalyzer.dev") is not None:
            return
        password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin12345")
        self.register_user(
            username="Administrador",
            email="admin@smartdataanalyzer.dev",
            password=password,
            role=Role.ADMIN,
        )

    def _get_user_row(self, email: str) -> sqlite3.Row | None:
        with self._connect() as connection:
            return connection.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,),
            ).fetchone()


def hash_password(password: str) -> str:
    """Gera hash PBKDF2-HMAC para senha, com salt único por usuário."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 390_000)
    return "pbkdf2_sha256$390000$%s$%s" % (
        base64.b64encode(salt).decode(),
        base64.b64encode(digest).decode(),
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Compara uma senha em texto puro com o hash armazenado."""
    algorithm, iterations, salt_b64, digest_b64 = stored_hash.split("$", 3)
    if algorithm != "pbkdf2_sha256":
        return False
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        int(iterations),
    )
    return hmac.compare_digest(actual, expected)


def render_login_form(auth_service: AuthService) -> None:
    """Renderiza o formulário de login quando não há sessão válida."""
    st.title("SmartDataAnalyzer")
    st.subheader("Acesse sua conta")
    with st.form("login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        session = auth_service.authenticate(email, password)
        if session is None:
            st.error("E-mail ou senha inválidos.")
            return
        st.session_state["auth_token"] = session.token
        st.success("Login realizado com sucesso.")
        st.rerun()


def render_user_header(auth_service: AuthService, user: User) -> None:
    """Renderiza ações de sessão no topo da barra lateral."""
    st.sidebar.caption(f"Conectado como {user.email} ({user.role.value})")
    if st.sidebar.button("Sair"):
        auth_service.logout(st.session_state.get("auth_token"))
        st.session_state.pop("auth_token", None)
        st.rerun()


def _row_to_user(row: sqlite3.Row | dict[str, Any]) -> User:
    return User(
        id=int(row["id"]),
        username=str(row["username"]),
        email=str(row["email"]),
        role=normalize_role(row["role"]),
        accepted_terms=bool(row["accepted_terms"]),
    )