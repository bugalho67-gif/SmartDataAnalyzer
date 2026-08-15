"""Treinamento supervisionado com validação cruzada."""

from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

from src.core.exceptions import MLTrainingError
from src.domain.entities.dataset import Dataset
from src.domain.enums.ml_enums import MLTaskType


class MLService:
    """Prepara dados e compara modelos básicos de ML."""

    def prepare_data(
        self,
        dataset: Dataset,
        target_column: str,
        feature_columns: list[str] | None = None,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, StandardScaler]:
        """Codifica, divide e normaliza as variáveis explicativas."""
        if target_column not in dataset.data:
            raise MLTrainingError("A coluna alvo não existe no dataset.")
        data = dataset.data.dropna(subset=[target_column]).copy()
        candidates = feature_columns or [
            column for column in data.columns if column != target_column
        ]
        features = pd.get_dummies(data[candidates], drop_first=True, dtype=float)
        if features.empty:
            raise MLTrainingError("Nenhuma variável explicativa válida foi encontrada.")
        target = data[target_column]
        stratify = target if target.nunique() < 20 and target.nunique() > 1 else None
        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=0.2,
            random_state=42,
            stratify=stratify,
        )
        scaler = StandardScaler()
        x_train = pd.DataFrame(
            scaler.fit_transform(x_train), columns=x_train.columns, index=x_train.index
        )
        x_test = pd.DataFrame(
            scaler.transform(x_test), columns=x_test.columns, index=x_test.index
        )
        return x_train, x_test, y_train, y_test, scaler

    def auto_train(
        self,
        dataset: Dataset,
        target_column: str,
        task_type: MLTaskType,
        feature_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Compara modelos por validação cruzada e retorna o melhor."""
        x_train, x_test, y_train, y_test, _ = self.prepare_data(
            dataset, target_column, feature_columns
        )
        if task_type == MLTaskType.CLASSIFICATION:
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Random Forest": RandomForestClassifier(
                    n_estimators=100, random_state=42
                ),
            }
            scoring = "accuracy"
        else:
            models = {
                "Linear Regression": LinearRegression(),
                "Random Forest": RandomForestRegressor(
                    n_estimators=100, random_state=42
                ),
            }
            scoring = "r2"
        folds = min(5, len(x_train))
        if folds < 2:
            raise MLTrainingError(
                "São necessários mais registros para treinar modelos."
            )
        scores = {
            name: float(
                cross_val_score(
                    model, x_train, y_train, cv=folds, scoring=scoring
                ).mean()
            )
            for name, model in models.items()
        }
        best_name = max(scores, key=scores.get)
        best_model = models[best_name].fit(x_train, y_train)
        importance = getattr(best_model, "feature_importances_", None)
        return {
            "best_model": best_name,
            "cv_score": scores[best_name],
            "test_score": float(best_model.score(x_test, y_test)),
            "scores": scores,
            "feature_importance": (
                dict(zip(x_train.columns, importance, strict=True))
                if importance is not None
                else {}
            ),
        }
