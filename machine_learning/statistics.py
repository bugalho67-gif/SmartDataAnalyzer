import streamlit as st
import pandas as pd


def show_statistics(df: pd.DataFrame):

    st.header("📈 Estatísticas Descritivas")

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        st.warning("Não existem colunas numéricas.")
        return

    tabela = pd.DataFrame(
        {
            "Tipo": numeric.dtypes,
            "Valores": numeric.count(),
            "Média": numeric.mean(),
            "Mediana": numeric.median(),
            "Moda": numeric.mode().iloc[0],
            "Mínimo": numeric.min(),
            "Máximo": numeric.max(),
            "Soma": numeric.sum(),
            "Desvio Padrão": numeric.std(),
            "Variância": numeric.var(),
            "Assimetria": numeric.skew(),
            "Curtose": numeric.kurt(),
        }
    )

    st.dataframe(tabela.round(2), use_container_width=True)

    st.subheader("Resumo Estatístico")

    st.dataframe(numeric.describe().T, use_container_width=True)
