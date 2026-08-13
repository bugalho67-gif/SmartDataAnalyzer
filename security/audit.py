"""Registro de auditoria para ações sensíveis."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app_config import BASE_DIR


AUDIT_DATABASE_PATH = BASE_DIR / "smartdata_security.db"


class AuditLogger:
    """Persiste eventos de auditoria em SQLite."""

    def __init__(self, database_path: Path = AUDIT_DATABASE_PATH) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def log_event(
        self,
        action: str,
        user_id: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Registra uma ação sensível com metadados opcionais."""
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO audit_logs (user_id, action, metadata, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    action,
                    json.dumps(metadata or {}, ensure_ascii=False),
                    datetime.now(UTC).isoformat(),
                ),
            )
            connection.commit()

    def list_events(self, limit: int = 100) -> list[dict[str, Any]]:
        """Lista os eventos mais recentes para administradores."""
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, user_id, action, metadata, created_at
                FROM audit_logs
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def _initialize_database(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()
