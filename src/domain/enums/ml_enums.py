"""Enums compartilhados entre análise, ML e exportação."""

from enum import StrEnum


class MLTaskType(StrEnum):
    """Tipos de tarefa de aprendizado supervisionado."""

    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class MetricType(StrEnum):
    """Métricas disponíveis para avaliação."""

    ACCURACY = "accuracy"
    R2 = "r2"


class OutlierMethod(StrEnum):
    """Métodos suportados para detecção de outliers."""

    IQR = "iqr"
    ZSCORE = "zscore"


class ExportFormat(StrEnum):
    """Formatos de exportação suportados."""

    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    HTML = "html"
