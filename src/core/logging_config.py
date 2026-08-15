"""Configuração centralizada de logging."""

import logging
from typing import Any

logger = logging.getLogger("smartdataanalyzer")


def configure_logging(settings: Any | None = None) -> None:
    """Inicializa logging com formato consistente."""
    del settings
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
