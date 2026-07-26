import streamlit as st
import plotly.express as px


def auto_chart(df):

    st.header("📊 Gráfico Inteligente")

    coluna = st.selectbox(
        "Coluna",
        df.columns
    )

    if df[coluna].dtype == "object":

        fig = px.bar(
            df[coluna].value_counts().reset_index(),
            x="index",
            y=coluna
        )

    else:

        fig = px.histogram(
            df,
            x=coluna
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
