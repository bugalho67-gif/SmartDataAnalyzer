"""Serviço de perfil e resumo de datasets."""

import pandas as pd

from src.domain.entities.dataset import ColumnProfile, Dataset, QualityReport


class DataService:
    """Calcula indicadores de qualidade e metadados."""

    def _generate_quality_report(self, data: pd.DataFrame) -> QualityReport:
        """Gera um relatório de qualidade sem modificar os dados."""
        rows, columns = data.shape
        total_cells = rows * columns
        missing = int(data.isna().sum().sum())
        duplicate_percentage = float(data.duplicated().mean() * 100) if rows else 0.0
        profiles = []
        for name in data.columns:
            series = data[name]
            unique_count = int(series.nunique(dropna=True))
            cardinality = unique_count / rows if rows else 0.0
            profiles.append(
                ColumnProfile(
                    name=str(name),
                    dtype=str(series.dtype),
                    null_percentage=float(series.isna().mean() * 100) if rows else 0.0,
                    unique_count=unique_count,
                    cardinality_ratio=cardinality,
                    is_high_cardinality=cardinality > 0.8,
                )
            )
        return QualityReport(
            total_rows=rows,
            total_columns=columns,
            total_cells=total_cells,
            missing_percentage=(missing / total_cells * 100) if total_cells else 0.0,
            duplicate_percentage=duplicate_percentage,
            memory_usage_mb=float(data.memory_usage(deep=True).sum() / 1024**2),
            column_profiles=profiles,
        )

    def get_dataset_summary(self, dataset: Dataset) -> dict[str, object]:
        """Retorna um resumo serializável do dataset."""
        return {
            "id": dataset.id,
            "name": dataset.name,
            "shape": [dataset.row_count, dataset.column_count],
            "columns": [str(column) for column in dataset.data.columns],
            "dtypes": {
                str(key): str(value) for key, value in dataset.data.dtypes.items()
            },
        }
