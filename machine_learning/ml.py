import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.tree import (
    DecisionTreeRegressor,
    DecisionTreeClassifier
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    classification_report,
)

from modules.feature_importance import show_importance
from modules.model_manager import save_model


# ======================================================
# Modelos disponíveis
# ======================================================

REGRESSION_MODELS = {
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),
    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),
    "Linear Regression": LinearRegression()
}

CLASSIFICATION_MODELS = {
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),
    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),
    "Logistic Regression": LogisticRegression(
        max_iter=1000
    )
}


# ======================================================
# Função principal
# ======================================================

def regression(df: pd.DataFrame):

    st.header("🤖 Machine Learning Automático")

    numericas = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categoricas = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    todas = numericas + categoricas

    if len(todas) < 2:
        st.warning(
            "São necessárias pelo menos duas colunas."
        )
        return

    alvo = st.selectbox(
        "Selecione a variável alvo",
        todas
    )

    dados = df[todas].dropna()

    if len(dados) < 20:
        st.warning(
            "Poucos registros para treinamento."
        )
        return

    X = pd.get_dummies(
        dados.drop(columns=[alvo]),
        drop_first=True
    )

    y = dados[alvo]

    if X.empty:
        st.warning(
            "Não existem variáveis suficientes."
        )
        return

    # ------------------------------------
    # Detecta automaticamente o tipo
    # ------------------------------------

    if alvo in numericas:

        tipo = "Regressão"

        modelos = REGRESSION_MODELS

        metrica_nome = "R²"

    else:

        tipo = "Classificação"

        modelos = CLASSIFICATION_MODELS

        metrica_nome = "Acurácia"

        if y.nunique() < 2:
            st.warning(
                "A variável alvo possui apenas uma classe."
            )
            return

    st.info(f"Problema detectado: **{tipo}**")

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42

    )

    resultados = {}

    modelos_treinados = {}

    # ------------------------------------
    # Treina todos os modelos
    # ------------------------------------

    with st.spinner("Treinando modelos..."):

        for nome, modelo in modelos.items():

            modelo.fit(
                X_train,
                y_train
            )

            pred = modelo.predict(
                X_test
            )

            if tipo == "Regressão":

                score = r2_score(
                    y_test,
                    pred
                )

            else:

                score = accuracy_score(
                    y_test,
                    pred
                )

            resultados[nome] = score

            modelos_treinados[nome] = modelo

    melhor_modelo_nome = max(
        resultados,
        key=resultados.get
    )

    melhor_modelo = modelos_treinados[
        melhor_modelo_nome
    ]

    previsoes = melhor_modelo.predict(
        X_test
    )

    st.success(
        f"🏆 Melhor modelo: **{melhor_modelo_nome}**"
    )

    # ------------------------------------
    # Comparação dos modelos
    # ------------------------------------

    tabela = pd.DataFrame({

        "Modelo": resultados.keys(),

        metrica_nome: resultados.values()

    }).sort_values(
        metrica_nome,
        ascending=False
    )

    st.subheader("Comparação dos Modelos")

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(

        tabela,

        x="Modelo",

        y=metrica_nome,

        text_auto=".3f",

        title="Desempenho dos Modelos"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ------------------------------------
    # Resultados
    # ------------------------------------

    st.subheader("Resultado Final")

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
            f"{mae:.3f}"
        )

        c3.metric(
            "RMSE",
            f"{rmse:.3f}"
        )

        comparacao = pd.DataFrame({

            "Valor Real": y_test.values,

            "Valor Previsto": previsoes

        })

        st.subheader("Valores Reais x Previstos")

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

        relatorio = classification_report(

            y_test,

            previsoes,

            output_dict=True

        )

        st.subheader(
            "Relatório de Classificação"
        )

        st.dataframe(

            pd.DataFrame(relatorio).transpose(),

            use_container_width=True

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

    # ------------------------------------
    # Importância das variáveis
    # ------------------------------------

    if hasattr(
        melhor_modelo,
        "feature_importances_"
    ):

        st.subheader(
            "Importância das Variáveis"
        )

        show_importance(
            melhor_modelo,
            X
        )

    # ------------------------------------
    # Informações
    # ------------------------------------

    st.subheader("Resumo")

    st.write(f"**Tipo do problema:** {tipo}")
    st.write(f"**Melhor modelo:** {melhor_modelo_nome}")
    st.write(f"**Registros utilizados:** {len(dados)}")
    st.write(f"**Variáveis utilizadas:** {X.shape[1]}")

    # ------------------------------------
    # Salvar modelo
    # ------------------------------------

    if st.button("💾 Salvar Modelo"):

        save_model(

            melhor_modelo,

            model_name=melhor_modelo_nome.replace(" ", "_"),

            metadata={

                "tipo": tipo,

                "algoritmo": melhor_modelo_nome,

                "registros": len(dados),

                "variaveis": X.shape[1],

                "score": float(
                    resultados[melhor_modelo_nome]
                )

            }

        )

        st.success("Modelo salvo com sucesso!")
