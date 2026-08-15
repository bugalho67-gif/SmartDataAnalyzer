"""ML service tests."""

import pytest

from src.application.services.ml_service import MLService
from src.domain.enums.ml_enums import MLTaskType


def test_prepare_data(sample_dataset):
    service = MLService()
    X_train, X_test, y_train, y_test, scaler = service.prepare_data(
        sample_dataset,
        target_column="score",
    )

    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) == len(X_train)


@pytest.mark.slow
def test_auto_train_classification(sample_dataset):
    service = MLService()

    # Convert score to categorical for classification test
    sample_dataset.data["category_target"] = (sample_dataset.data["score"] > 50).astype(
        int
    )

    results = service.auto_train(
        dataset=sample_dataset,
        target_column="category_target",
        task_type=MLTaskType.CLASSIFICATION,
    )

    assert "best_model" in results
    assert "cv_score" in results
    assert results["cv_score"] > 0
