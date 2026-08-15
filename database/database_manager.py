import streamlit as st

from database.connections import DatabaseConnection
from database.queries import (
    execute_query,
)
from core.exceptions import DatabaseError, show_error


def connect_database():
    st.header("🗄 Banco de Dados")

    tipo = st.selectbox("Banco", ["SQLite", "PostgreSQL", "MySQL", "SQL Server"])

    if tipo == "SQLite":
        arquivo = st.text_input("Arquivo .db", value="smartdata.db")
        if st.button("Conectar"):
            try:
                engine = DatabaseConnection.sqlite(arquivo)
                st.session_state["engine"] = engine
                st.success("Conectado!")
            except Exception as exc:
                show_error(DatabaseError(f"Falha ao conectar no SQLite: {exc}"))
    else:
        host = st.text_input("Host")
        porta = st.number_input("Porta", value=5432)
        banco = st.text_input("Banco")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Conectar"):
            try:
                if tipo == "PostgreSQL":
                    engine = DatabaseConnection.postgres(
                        host, porta, banco, usuario, senha
                    )
                elif tipo == "MySQL":
                    engine = DatabaseConnection.mysql(
                        host, porta, banco, usuario, senha
                    )
                else:
                    engine = DatabaseConnection.sqlserver(host, banco, usuario, senha)

                # Testa a conexão
                with engine.connect() as conn:
                    conn.execute("SELECT 1")

                st.session_state["engine"] = engine
                st.success("Conectado com sucesso!")

            except Exception as exc:
                show_error(DatabaseError(f"Falha ao conectar em {tipo}: {exc}"))

    if "engine" in st.session_state:
        st.divider()
        st.subheader("Consulta SQL")

        sql = st.text_area("SQL", "SELECT * FROM tabela LIMIT 100")

        if st.button("Executar"):
            try:
                df = execute_query(st.session_state["engine"], sql)
                st.dataframe(df)
            except Exception as exc:
                show_error(DatabaseError(f"Erro na consulta: {exc}"))
