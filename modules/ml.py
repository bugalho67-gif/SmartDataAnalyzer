import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    classification_report
)

from modules.feature_importance import show_importance


def regression(df: pd.DataFrame):

    st.header("🤖 Machine Learning Automático")

    numericas = df.select_dtypes(include="number").columns.tolist()

    categoricas = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    todas = numericas + categoricas

    if len(todas) < 2:
        st.warning(
            "São necessárias pelo menos duas colunas para criar um modelo."
        )
        return

    alvo = st.selectbox(
        "Variável alvo",
        todas
    )

    dados = df[todas].dropna()

    if len(dados) < 20:
        st.warning(
            "O conjunto de dados é muito pequeno para treinamento."
        )
        return

    X = pd.get_dummies(
        dados.drop(columns=[alvo]),
        drop_first=True
    )

    y = dados[alvo]

    tipo = (
        "Classificação"
        if alvo in categoricas
        else "Regressão"
    )

    st.info(f"Modelo detectado automaticamente: **{tipo}**")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    if tipo == "Regressão":

        modelo = RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )

    else:

        modelo = RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )

    modelo.fit(
        X_train,
        y_train
    )

    previsoes = modelo.predict(X_test)

    st.subheader("📊 Resultados")

    if tipo == "Regressão":

        r2 = r2_score(
            y_test,
            previsoes
        )

        mae = mean_absolute_error(
            y_test,
            previsoes
        )

        rmse = mean_squared_error(
            y_test,
            previsoes
        ) ** 0.5

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "R²",
            f"{r2:.3f}"
        )

        c2.metric(
            "MAE",
            f"{mae:.2f}"
        )

        c3.metric(
            "RMSE",
            f"{rmse:.2f}"
        )

        comparacao = pd.DataFrame({

            "Valor Real": y_test.values,

            "Valor Previsto": previsoes

        })

        st.subheader("Comparação")

        st.dataframe(
            comparacao.head(30),
            use_container_width=True
        )

        fig = px.scatter(
            comparacao,
            x="Valor Real",
            y="Valor Previsto",
            trendline="ols",
            title="Valor Real x Valor Previsto"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        acuracia = accuracy_score(
            y_test,
            previsoes
        )

        st.metric(
            "Acurácia",
            f"{acuracia:.2%}"
        )

        st.subheader("Relatório de Classificação")

        relatorio = classification_report(
            y_test,
            previsoes,
            output_dict=True
        )

        st.dataframe(
            pd.DataFrame(relatorio).transpose(),
            use_container_width=True
        )

        comparacao = pd.DataFrame({

            "Valor Real": y_test.values,

            "Valor Previsto": previsoes

        })

        st.dataframe(
            comparacao.head(30),
            use_container_width=True
        )

    st.subheader("🌳 Importância das Variáveis")

    show_importance(
        modelo,
        X
    )

    st.subheader("ℹ️ Informações do Modelo")

    st.write(f"**Tipo:** {tipo}")

    st.write(f"**Algoritmo:** {modelo.__class__.__name__}")

    st.write(f"**Registros utilizados:** {len(dados)}")

    st.write(f"**Variáveis de entrada:** {X.shape[1]}")

    st.success("Treinamento concluído com sucesso!")
