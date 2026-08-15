from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def suggest_chart(df: pd.DataFrame):

    st.header("🧠 Dashboard Inteligente")

    if df.empty:
        st.warning("O DataFrame está vazio.")
        return

    coluna = st.selectbox("Escolha uma coluna", df.columns)

    serie = df[coluna]

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Valores únicos", serie.nunique())

    c2.metric("Valores nulos", int(serie.isnull().sum()))

    c3.metric("Tipo", str(serie.dtype))

    st.divider()

    # -------------------------
    # Numérica
    # -------------------------

    if pd.api.types.is_numeric_dtype(serie):
        st.subheader("📈 Histograma")

        fig = px.histogram(
            df, x=coluna, nbins=30, marginal="box", title=f"Distribuição de {coluna}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Estatísticas")

        st.dataframe(serie.describe().to_frame().T, use_container_width=True)

        return

    # -------------------------
    # Data
    # -------------------------

    if pd.api.types.is_datetime64_any_dtype(serie):
        st.subheader("📅 Série Temporal")

        contagem = df.groupby(coluna).size().reset_index(name="Quantidade")

        fig = px.line(
            contagem,
            x=coluna,
            y="Quantidade",
            markers=True,
            title=f"Ocorrências ao longo do tempo ({coluna})",
        )

        st.plotly_chart(fig, use_container_width=True)

        return

    # -------------------------
    # Categórica
    # -------------------------

    st.subheader("📊 Frequência das Categorias")

    contagem = serie.value_counts(dropna=False).reset_index()

    # Compatível com qualquer versão do pandas
    contagem.columns = [coluna, "Quantidade"]

    fig = px.bar(
        contagem,
        x=coluna,
        y="Quantidade",
        text="Quantidade",
        title=f"Distribuição de {coluna}",
    )

    fig.update_layout(xaxis_title=coluna, yaxis_title="Quantidade")

    st.plotly_chart(fig, use_container_width=True)

    if len(contagem) <= 15:
        fig2 = px.pie(
            contagem,
            names=coluna,
            values="Quantidade",
            hole=0.45,
            title="Distribuição Percentual",
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Tabela de Frequências")

    st.dataframe(contagem, use_container_width=True)
