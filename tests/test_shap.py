"""SHAP service tests."""

import numpy as np
import pandas as pd
import pytest

from src.domain.entities.dataset import Dataset


@pytest.fixture
def sample_dataset():
    df = pd.DataFrame(
        {
            "feature_a": np.random.randn(100),
            "feature_b": np.random.randn(100),
            "target": np.random.randint(0, 2, 100),
        }
    )
    return Dataset(
        id="test-shap",
        name="test.csv",
        source_type="upload",
        data=df,
    )


def test_shap_service_import():
    """Test that SHAP service can be instantiated."""
    from src.application.services.shap_service import SHAPService

    service = SHAPService()
    assert service is not None


def test_explain_model_no_model_file(sample_dataset):
    """Test graceful handling when model file doesn't exist."""
    from src.application.services.shap_service import SHAPService
    from src.core.exceptions import MLTrainingError

    service = SHAPService()
    with pytest.raises(MLTrainingError):
        service.explain_model("nonexistent-id", sample_dataset)
