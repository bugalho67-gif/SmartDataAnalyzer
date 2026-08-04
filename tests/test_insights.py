import pandas as pd

from machine_learning.outliers import detect_outliers_iqr, detect_outliers_zscore


def test_detect_outliers_iqr_finds_extreme_value():
    df = pd.DataFrame({"valor": [10, 11, 12, 13, 14, 100]})

    resultado = detect_outliers_iqr(df, "valor")

    assert len(resultado) == 1
    assert resultado.iloc[0]["valor"] == 100


def test_detect_outliers_iqr_no_outliers():
    df = pd.DataFrame({"valor": [10, 11, 12, 13, 14]})

    resultado = detect_outliers_iqr(df, "valor")

    assert len(resultado) == 0


def test_detect_outliers_zscore_finds_extreme_value():
    # Amostra maior: com poucos pontos, um único valor extremo infla o
    # próprio desvio padrão e o z-score nunca ultrapassa 3 (limitação
    # conhecida do método, não um bug). Por isso, 19 valores normais + 1 outlier.
    df = pd.DataFrame({"valor": [10] * 19 + [1000]})

    resultado = detect_outliers_zscore(df, "valor")

    assert len(resultado) == 1
    assert resultado.iloc[0]["valor"] == 1000


def test_detect_outliers_zscore_constant_column_returns_empty():
    df = pd.DataFrame({"valor": [5, 5, 5, 5]})

    resultado = detect_outliers_zscore(df, "valor")

    assert len(resultado) == 0
