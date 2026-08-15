"""Entidades usadas no processamento de datasets."""

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass(slots=True)
class ColumnProfile:
    """Representa o perfil de qualidade de uma coluna."""

    name: str
    dtype: str
    null_percentage: float
    unique_count: int
    cardinality_ratio: float
    is_high_cardinality: bool


@dataclass(slots=True)
class QualityReport:
    """Consolida indicadores de qualidade de um dataset."""

    total_rows: int
    total_columns: int
    total_cells: int
    missing_percentage: float
    duplicate_percentage: float
    memory_usage_mb: float
    column_profiles: list[ColumnProfile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class Dataset:
    """Representa um conjunto de dados carregado na aplicação."""

    id: str
    name: str
    source_type: str
    data: pd.DataFrame
    quality_report: QualityReport | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def row_count(self) -> int:
        """Retorna a quantidade de linhas."""
        return len(self.data)

    @property
    def column_count(self) -> int:
        """Retorna a quantidade de colunas."""
        return len(self.data.columns)

    @property
    def memory_usage_mb(self) -> float:
        """Retorna o consumo aproximado de memória em MiB."""
        return float(self.data.memory_usage(deep=True).sum() / 1024**2)

    def get_numeric_columns(self) -> list[str]:
        """Retorna os nomes das colunas numéricas."""
        return self.data.select_dtypes(include="number").columns.tolist()

    def get_categorical_columns(self) -> list[str]:
        """Retorna os nomes das colunas categóricas."""
        return self.data.select_dtypes(exclude="number").columns.tolist()
