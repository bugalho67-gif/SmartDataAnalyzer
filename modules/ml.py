import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


def regression(df: pd.DataFrame):

    st.header("🤖 Machine Learning")

    numericas = df.select_dtypes(include="number")

    if len(numericas.columns) < 2:
        st.warning("São necessárias pelo menos duas colunas numéricas.")
        return

    alvo = st.selectbox(
        "Variável alvo",
        numericas.columns
    )

    X = numericas.drop(columns=[alvo])

    y = numericas[alvo]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    modelo = RandomForestRegressor(
        random_state=42
    )

    modelo.fit(X_train, y_train)

    pred = modelo.predict(X_test)

    score = r2_score(
        y_test,
        pred
    )

    st.metric(
        "R²",
        round(score,3)
    )
