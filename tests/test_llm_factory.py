"""Testes da factory unificada de LLMs."""

from ai.llm_factory import available_providers, create_llm_provider
from providers.base import BaseProvider
from providers.local import LocalProvider


def test_available_providers_includes_phase_4_adapters() -> None:
    providers = available_providers()

    assert "openai" in providers
    assert "gemini" in providers
    assert "claude" in providers
    assert "ollama" in providers
    assert "azure_openai" in providers


def test_create_llm_provider_defaults_to_local(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("AI_PROVIDER", raising=False)

    provider = create_llm_provider()

    assert isinstance(provider, LocalProvider)


def test_create_llm_provider_falls_back_for_unknown_name() -> None:
    provider = create_llm_provider("desconhecido")

    assert isinstance(provider, LocalProvider)


def test_base_provider_contract_methods() -> None:
    provider: BaseProvider = LocalProvider()

    assert "Modo local" in provider.ask("Pergunta?", "Contexto")
    assert "Modo local" in provider.generate_insights("Resumo")
    assert "Modo local" in provider.explain_chart({"tipo": "bar"})
