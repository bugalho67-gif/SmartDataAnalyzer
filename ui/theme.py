"""Design system e helpers de tema para Streamlit e Plotly."""

from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

_THEME_CSS = Path(__file__).with_name("theme.css")

PLOTLY_LIGHT_TEMPLATE = "plotly_white"
PLOTLY_DARK_TEMPLATE = "plotly_dark"
PLOTLY_COLORWAY = ["#4f46e5", "#10b981", "#f59e0b", "#f43f5e", "#06b6d4", "#8b5cf6"]


def initialize_theme() -> None:
    """Inicializa o tema global persistente na sessão."""
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False


def render_theme_toggle() -> None:
    """Renderiza o seletor de dark mode na barra lateral."""
    st.sidebar.toggle(
        "Modo escuro",
        key="dark_mode",
        help="Alterna o tema global da interface e dos gráficos.",
    )


def apply_global_theme() -> None:
    """Aplica CSS premium e atributos de tema no Streamlit."""
    initialize_theme()
    css = _THEME_CSS.read_text(encoding="utf-8")
    theme_name = "dark" if st.session_state["dark_mode"] else "light"
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <script>
          document.documentElement.setAttribute('data-theme', '{theme_name}');
        </script>
        <div data-theme="{theme_name}"></div>
        """,
        unsafe_allow_html=True,
    )


def plotly_template() -> str:
    """Retorna o template Plotly compatível com o tema atual."""
    return (
        PLOTLY_DARK_TEMPLATE
        if st.session_state.get("dark_mode")
        else PLOTLY_LIGHT_TEMPLATE
    )


def apply_plotly_theme(fig: go.Figure) -> go.Figure:
    """Aplica paleta, fonte e margens premium a um gráfico Plotly."""
    fig.update_layout(
        template=plotly_template(),
        colorway=PLOTLY_COLORWAY,
        font={
            "family": "Inter, sans-serif",
            "color": "#f1f5f9" if st.session_state.get("dark_mode") else "#1e293b",
        },
        title={"x": 0.02, "xanchor": "left"},
        margin={"l": 32, "r": 24, "t": 64, "b": 32},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.18)", zeroline=False)
    return fig


def render_app_header(title: str, subtitle: str, user_label: str) -> None:
    """Renderiza um cabeçalho SaaS premium para a página atual."""
    st.markdown(
        f"""
        <section class="sda-header">
          <div>
            <div class="sda-header__eyebrow">SmartDataAnalyzer</div>
            <div class="sda-header__title">{title}</div>
            <p class="sda-header__subtitle">{subtitle}</p>
          </div>
          <div class="sda-card" style="padding: .8rem 1rem; min-width: 210px;">
            <div class="sda-card__eyebrow">Sessão ativa</div>
            <p class="sda-card__text">{user_label}</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, message: str, icon: str = "📊") -> None:
    """Renderiza um estado vazio elegante e responsivo."""
    st.markdown(
        f"""
        <section class="sda-empty-state">
          <div class="sda-empty-state__icon">{icon}</div>
          <h3>{title}</h3>
          <p>{message}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
