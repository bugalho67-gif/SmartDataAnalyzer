"""Anonimização de dados pessoais comuns no contexto brasileiro."""

from __future__ import annotations

import re

import pandas as pd

SENSITIVE_COLUMN_PATTERNS: dict[str, re.Pattern[str]] = {
    "cpf": re.compile(r"cpf|documento", re.IGNORECASE),
    "cnpj": re.compile(r"cnpj", re.IGNORECASE),
    "email": re.compile(r"e-?mail|email", re.IGNORECASE),
    "telefone": re.compile(r"tel[eé]fone|celular|phone", re.IGNORECASE),
    "rg": re.compile(r"\brg\b|registro_geral", re.IGNORECASE),
}

VALUE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b"),
    re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    re.compile(r"\b(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}\b"),
)


def detect_sensitive_columns(df: pd.DataFrame) -> list[str]:
    """Detecta colunas com nomes ou valores potencialmente sensíveis."""
    detected: list[str] = []
    for column in df.columns:
        column_name = str(column)
        if any(pattern.search(column_name) for pattern in SENSITIVE_COLUMN_PATTERNS.values()):
            detected.append(column_name)
            continue

        sample = df[column].dropna().astype(str).head(50)
        if sample.apply(_contains_sensitive_value).any():
            detected.append(column_name)

    return detected


def anonymize_dataframe(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Substitui valores sensíveis por marcador anonimizado."""
    anonymized = df.copy()
    target_columns = columns or detect_sensitive_columns(df)
    for column in target_columns:
        if column in anonymized.columns:
            anonymized[column] = "[ANONIMIZADO]"
    return anonymized


def _contains_sensitive_value(value: str) -> bool:
    return any(pattern.search(value) for pattern in VALUE_PATTERNS)
