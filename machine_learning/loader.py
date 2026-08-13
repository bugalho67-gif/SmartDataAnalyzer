"""Utilitários para carregar arquivos tabulares em DataFrames do pandas."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd

from core.exceptions import DataLoadError


class DataLoader:
    """Carrega arquivos CSV, Excel, JSON, Parquet e XML em DataFrames."""

    SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".json", ".parquet", ".xml")

    @staticmethod
    def load(file: BinaryIO) -> pd.DataFrame:
        """Carrega o arquivo enviado em um DataFrame do pandas."""
        extension = Path(getattr(file, "name", "")).suffix.lower()

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
            if extension == ".json":
                return pd.read_json(file)
            if extension == ".parquet":
                return pd.read_parquet(file)
            return pd.read_xml(file, parser="etree")
        except ImportError as exc:
            raise DataLoadError(
                f"Dependência opcional ausente para ler '{extension}'. "
                "Instale o pacote indicado pelo pandas para esse formato."
            ) from exc
        except Exception as exc:
            raise DataLoadError(
                f"Não foi possível ler o arquivo '{getattr(file, 'name', 'upload')}': {exc}"
            ) from exc

    @staticmethod
    def preview(file: BinaryIO, rows: int = 100) -> pd.DataFrame:
        """Retorna uma prévia das primeiras linhas sem mudar a posição final do upload."""
        position = file.tell()
        try:
            df = DataLoader.load(file)
            return df.head(rows)
        finally:
            file.seek(position)
