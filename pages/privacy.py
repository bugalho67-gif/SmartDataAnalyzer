"""Página de privacidade e direitos do titular."""

import streamlit as st

from security.auth import AuthService
from security.rbac import Role


auth_service = AuthService()
user = auth_service.require_role(Role.VIEWER)

st.title("Privacidade e meus dados")
st.write("Você pode solicitar exportação ou deleção dos seus dados pessoais.")
st.download_button(
    "Exportar meus dados de conta",
    data=f"email,role\n{user.email},{user.role.value}\n",
    file_name="meus_dados.csv",
    mime="text/csv",
)
st.info(
    "Solicitações de deleção devem ser revisadas por um administrador "
    "para preservar logs legais de auditoria."
)
