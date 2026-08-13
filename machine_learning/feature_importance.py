import streamlit as st
import pandas as pd
import plotly.express as px
from ui.theme import apply_plotly_theme


def show_importance(modelo, X):

    importancia = pd.DataFrame({

        "Variável": X.columns,

        "Importância": modelo.feature_importances_

    })

    importancia = importancia.sort_values(
        by="Importância",
        ascending=False
    )

    fig = px.bar(
        importancia,
        x="Importância",
        y="Variável",
        orientation="h",
        text_auto=".3f",
        title="Importância das Variáveis"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        apply_plotly_theme(fig),
        use_container_width=True
    )

    st.dataframe(
        importancia,
        use_container_width=True,
        hide_index=True
    )
