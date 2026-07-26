import streamlit as st
import plotly.express as px


def heatmap(df):

    corr = df.corr(
        numeric_only=True
    )

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
