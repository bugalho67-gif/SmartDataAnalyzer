"""Serviços estatísticos para análise exploratória."""

from typing import Any

import numpy as np

from src.domain.entities.dataset import Dataset
from src.domain.enums.ml_enums import OutlierMethod


class AnalyticsService:
    """Executa estatísticas descritivas e detecção de outliers."""

    def get_descriptive_statistics(self, dataset: Dataset) -> dict[str, Any]:
        """Retorna estatísticas das colunas numéricas."""
        numeric = dataset.data.select_dtypes(include="number")
        return numeric.describe().to_dict() if not numeric.empty else {}

    def get_correlation_matrix(self, dataset: Dataset):
        """Calcula a matriz de correlação das colunas numéricas."""
        numeric = dataset.data.select_dtypes(include="number")
        analytical_columns = [
            column
            for column in numeric.columns
            if str(column).strip().lower()
            not in {"id", "identifier", "codigo", "código"}
        ]
        return numeric[analytical_columns].corr()

    def detect_outliers(
        self,
        dataset: Dataset,
        method: OutlierMethod = OutlierMethod.IQR,
    ) -> dict[str, Any]:
        """Detecta outliers pelo intervalo interquartil ou z-score."""
        output: dict[str, Any] = {}
        for column in dataset.get_numeric_columns():
            series = dataset.data[column].dropna()
            if method == OutlierMethod.ZSCORE:
                std = series.std()
                mask = (
                    abs((series - series.mean()) / std) > 3
                    if std
                    else np.zeros(len(series), dtype=bool)
                )
            else:
                first, third = series.quantile([0.25, 0.75])
                interval = third - first
                mask = (series < first - 1.5 * interval) | (
                    series > third + 1.5 * interval
                )
            indexes = series.index[mask].tolist()
            if indexes:
                output[column] = indexes
        output["_summary"] = {
            "total": sum(
                len(value) for key, value in output.items() if key != "_summary"
            )
        }
        return output
