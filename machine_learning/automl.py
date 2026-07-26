import streamlit as st
import pandas as pd

from sklearn.model_selection import cross_val_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

MODELOS = {

    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(),

    "Random Forest": RandomForestRegressor(
        random_state=42
    )

}


def escolher_modelo(X, y):

    resultados = {}

    for nome, modelo in MODELOS.items():

        score = cross_val_score(

            modelo,

            X,

            y,

            cv=5,

            scoring="r2"

        ).mean()

        resultados[nome] = score

    melhor = max(
        resultados,
        key=resultados.get
    )

    return melhor, resultados
