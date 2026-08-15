"""Configurações compatíveis com a interface modular em src."""

import os
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True, slots=True)
class SecuritySettings:
    """Limites de segurança configuráveis."""

    max_upload_size_mb: int = 100


@dataclass(frozen=True, slots=True)
class Settings:
    """Configurações essenciais da aplicação."""

    app_name: str = "SmartDataAnalyzer"
    app_version: str = "1.0.0"
    app_env: str = "development"
    allowed_extensions: str = "csv,xlsx,xls,json,parquet,xml"
    security: SecuritySettings = field(default_factory=SecuritySettings)

    @property
    def allowed_extensions_list(self) -> list[str]:
        """Retorna extensões aceitas pelo uploader."""
        return [
            item.strip() for item in self.allowed_extensions.split(",") if item.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Carrega configurações do ambiente uma única vez."""
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        security=SecuritySettings(int(os.getenv("MAX_UPLOAD_SIZE_MB", "100"))),
    )
