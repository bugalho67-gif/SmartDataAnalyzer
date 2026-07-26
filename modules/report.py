from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from datetime import datetime
import pandas as pd


def generate_pdf(df: pd.DataFrame, filename="exports/relatorio.pdf"):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    elementos = []

    elementos.append(
        Paragraph("<b>Smart Data Analyzer</b>", styles["Title"])
    )

    elementos.append(
        Paragraph(
            f"Gerado em: {datetime.now()}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Quantidade de linhas: {len(df)}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Quantidade de colunas: {len(df.columns)}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Valores nulos: {df.isnull().sum().sum()}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Duplicados: {df.duplicated().sum()}",
            styles["Normal"]
        )
    )

    doc.build(elementos)
