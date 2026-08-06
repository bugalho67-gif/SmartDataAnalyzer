import streamlit as st

"""Utilitários para carregar arquivos tabulares em DataFrames do pandas."""

from pathlib import Path

import pandas as pd

from core.exceptions import DataLoadError


class DataLoader:
    """Carrega arquivos CSV, Excel e JSON em um DataFrame do pandas."""

    SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".json")

    @staticmethod
    def load(file) -> pd.DataFrame:
        extension = Path(file.name).suffix.lower()

        if extension not in DataLoader.SUPPORTED_EXTENSIONS:
            raise DataLoadError(
                f"Formato '{extension}' não suportado. "
                f"Use um dos formatos: {', '.join(DataLoader.SUPPORTED_EXTENSIONS)}."
            )

        try:
            if extension == ".csv":
                return pd.read_csv(file)
            if extension == ".xlsx":
                return pd.read_excel(file)
            return pd.read_json(file)
        except Exception as exc:
            raise DataLoadError(
                f"Não foi possível ler o arquivo '{file.name}': {exc}"
            ) from exc
