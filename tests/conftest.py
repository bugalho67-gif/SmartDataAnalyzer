"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    import pandas as pd
    import numpy as np

    return pd.DataFrame(
        {
            "id": range(100),
            "name": [f"item_{i}" for i in range(100)],
            "value": np.random.randn(100),
            "category": np.random.choice(["A", "B", "C"], 100),
            "score": np.random.randint(0, 100, 100),
        }
    )


@pytest.fixture
def sample_dataset(sample_dataframe):
    """Create a sample Dataset entity."""
    from src.domain.entities.dataset import Dataset

    return Dataset(
        id="test-123",
        name="test.csv",
        source_type="upload",
        data=sample_dataframe,
    )
