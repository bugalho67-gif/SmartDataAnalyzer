from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


def summary(df: pd.DataFrame) -> str:
    """
    Gera um resumo automático do conjunto de dados.
    """

    texto = f"""
    O conjunto de dados possui <b>{len(df):,}</b> registros,
    <b>{len(df.columns)}</b> colunas,
    <b>{int(df.isnull().sum().sum())}</b> valores ausentes
    e <b>{int(df.duplicated().sum())}</b> registros duplicados.
    """

    return texto


def generate_pdf(df: pd.DataFrame, filename: str = "exports/relatorio.pdf"):

    # Cria a pasta exports caso ela não exista
    Path("exports").mkdir(exist_ok=True)

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    elementos = []

    elementos.append(Paragraph("Smart Data Analyzer", styles["Title"]))

    elementos.append(
        Paragraph(
            f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            styles["Normal"],
        )
    )

    elementos.append(Paragraph("<br/><b>Resumo Executivo</b>", styles["Heading2"]))

    elementos.append(Paragraph(summary(df), styles["BodyText"]))

    elementos.append(Paragraph("<br/><b>Informações Gerais</b>", styles["Heading2"]))

    elementos.append(Paragraph(f"Quantidade de linhas: {len(df)}", styles["Normal"]))

    elementos.append(
        Paragraph(f"Quantidade de colunas: {len(df.columns)}", styles["Normal"])
    )

    elementos.append(
        Paragraph(f"Valores nulos: {int(df.isnull().sum().sum())}", styles["Normal"])
    )

    elementos.append(
        Paragraph(
            f"Registros duplicados: {int(df.duplicated().sum())}", styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Uso de memória: {round(df.memory_usage(deep=True).sum() / 1024, 2)} KB",
            styles["Normal"],
        )
    )

    doc.build(elementos)
