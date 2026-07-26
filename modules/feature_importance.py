import streamlit as st
import plotly.express as px
import pandas as pd


def show_importance(modelo, X):

    importancia = pd.DataFrame({

        "Variável": X.columns,

        "Importância": modelo.feature_importances_

    })

    importancia = importancia.sort_values(
        "Importância",
        ascending=False
    )

    fig = px.bar(
        importancia,
        x="Importância",
        y="Variável",
        orientation="h",
        title="Importância das Variáveis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
