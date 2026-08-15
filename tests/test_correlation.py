import pandas as pd

from machine_learning.correlation import calculate_correlation_matrix


def test_correlation_matrix_ignores_non_numeric_columns():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],
            "c": ["x", "y", "z", "x", "y"],
        }
    )

    matriz = calculate_correlation_matrix(df)

    assert list(matriz.columns) == ["a", "b"]


def test_correlation_perfectly_correlated_columns():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],
        }
    )

    matriz = calculate_correlation_matrix(df)

    assert matriz.loc["a", "b"] == 1.0


def test_correlation_method_spearman_runs():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [5, 3, 4, 1, 2],
        }
    )

    matriz = calculate_correlation_matrix(df, method="spearman")

    assert matriz.shape == (2, 2)
