import streamlit as st

from database.connections import DatabaseConnection

from database.queries import (
    execute_query,
    list_tables
)


def connect_database():

    st.header("🗄 Banco de Dados")

    tipo = st.selectbox(

        "Banco",

        [

            "SQLite",

            "PostgreSQL",

            "MySQL",

            "SQL Server"

        ]

    )

    if tipo == "SQLite":

        arquivo = st.text_input(
            "Arquivo .db"
        )

        if st.button("Conectar"):

            engine = DatabaseConnection.sqlite(
                arquivo
            )

            st.session_state["engine"] = engine

            st.success("Conectado!")

    else:

        host = st.text_input("Host")

        porta = st.number_input(
            "Porta",
            value=5432
        )

        banco = st.text_input("Banco")

        usuario = st.text_input("Usuário")

        senha = st.text_input(
            "Senha",
            type="password"
        )

        if st.button("Conectar"):

            if tipo == "PostgreSQL":

                engine = DatabaseConnection.postgres(

                    host,

                    porta,

                    banco,

                    usuario,

                    senha

                )

            elif tipo == "MySQL":

                engine = DatabaseConnection.mysql(

                    host,

                    porta,

                    banco,

                    usuario,

                    senha

                )

            else:

                engine = DatabaseConnection.sqlserver(

                    host,

                    banco,

                    usuario,

                    senha

                )

            st.session_state["engine"] = engine

            st.success("Conectado!")

    if "engine" in st.session_state:

        st.divider()

        st.subheader("Consulta SQL")

        sql = st.text_area(

            "SQL",

            "SELECT * FROM tabela LIMIT 100"

        )

        if st.button("Executar"):

            df = execute_query(

                st.session_state["engine"],

                sql

            )

            st.dataframe(df)
