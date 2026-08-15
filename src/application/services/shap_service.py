"""Integração opcional para explicabilidade de modelos."""

from pathlib import Path

from src.core.exceptions import MLTrainingError
from src.domain.entities.dataset import Dataset


class SHAPService:
    """Localiza modelos persistidos antes de calcular explicações."""

    def __init__(self, models_directory: str | Path = "models") -> None:
        self.models_directory = Path(models_directory)

    def explain_model(self, model_id: str, dataset: Dataset) -> dict[str, object]:
        """Valida a existência do modelo para uma explicação posterior."""
        model_path = self.models_directory / f"{model_id}.joblib"
        if not model_path.is_file():
            raise MLTrainingError("Modelo treinado não encontrado.")
        raise MLTrainingError("Explicação SHAP ainda não disponível para este modelo.")
