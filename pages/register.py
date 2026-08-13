"""Página dedicada de cadastro local."""

import streamlit as st

from security.auth import AuthService
from security.rbac import Role


auth_service = AuthService()

st.title("Criar conta")
with st.form("register_form"):
    username = st.text_input("Nome")
    email = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Cadastrar")

if submitted:
    try:
        auth_service.register_user(username, email, password, Role.VIEWER)
        st.success("Conta criada. Faça login para continuar.")
    except Exception as exc:
        st.error(str(exc))
