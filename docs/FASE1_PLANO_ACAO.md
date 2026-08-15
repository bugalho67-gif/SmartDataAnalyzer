# Fase 1 — Auditoria e Plano de Ação

Data da auditoria: 2026-08-12

## Escopo analisado

Foram revisados os pontos solicitados no `PROMPT_EXECUCAO.md`: `app.py`, módulos em `ai/`, `core/`, `machine_learning/`, `database/`, `providers/`, `config/`, `tests/`, além de `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `README.md` e `Makefile`.

## Diagnóstico do estado atual

### O que está funcionando

- A aplicação principal em Streamlit inicializa com configuração de página, menu lateral, upload de arquivos, validação básica de tamanho, filtros, busca e roteamento para páginas de análise.
- O carregamento de dados aceita CSV, Excel e JSON por meio de `machine_learning.loader.DataLoader`.
- Existem módulos de EDA/ML para dashboard, estatísticas, gráficos, correlação, qualidade de dados, outliers, AutoML, relatórios e exportações.
- Há logging centralizado básico em `core.logger`, com escrita no arquivo `logs/application.log`.
- A camada de IA já possui abstrações iniciais (`AIClient`, `BaseProvider`, factory e provedores local/OpenAI), e o provider OpenAI já trata ausência de chave, autenticação e rate limit.
- O projeto possui Dockerfile, docker-compose, Makefile e uma suíte inicial de testes.

### O que está incompleto ou mockado

- A autenticação/RBAC exigida pelo plano ainda não existe nos pacotes atuais `security/` ou `pages/`; os testes de autenticação referenciam uma arquitetura `src.application`/`src.domain` que não está presente no repositório.
- O módulo de IA ainda não possui interface unificada completa para Gemini, Claude, Ollama e Azure OpenAI; a factory registra apenas `local` e `openai`.
- `ai.openai_client.OpenAIClient` permanece como stub e lança `NotImplementedError`.
- Não há chat persistente em SQLite nem uso estruturado do dataset carregado como system prompt para provedores externos.
- O Dockerfile declara healthcheck com `curl`, mas a imagem instala apenas `build-essential`; isso tende a quebrar o healthcheck em runtime.
- O README está incompleto na seção de segurança e não documenta todas as variáveis e fluxos de deploy previstos.

## Débitos técnicos

- O repositório mistura duas arquiteturas: módulos funcionais na raiz (`ai/`, `machine_learning/`, `database/`) e testes importando pacotes inexistentes em `src.application`, `src.domain` e `src.core`.
- Há várias funções sem type hints ou com assinaturas genéricas, especialmente em componentes Streamlit e módulos legados.
- Algumas docstrings e mensagens estão em português, mas parte dos testes e comentários usa inglês; é preciso padronizar o idioma do produto sem quebrar convenções de nomes em Python.
- O tratamento de erro no fluxo principal captura `Exception` de forma ampla; a UX é amigável, mas a observabilidade e a diferenciação por tipo de erro ainda são limitadas.
- `app.py` contém fluxo imperativo no nível do módulo, dificultando testes de integração e proteção por autenticação.
- `DataLoader.load` carrega o arquivo diretamente sem camada de validação de conteúdo, magic bytes ou proteção contra CSV Injection.

## Vulnerabilidades e riscos de segurança

- Não há autenticação obrigatória antes de acessar upload, dashboards, ML ou banco de dados.
- Não há RBAC para separar permissões de admin, analyst e viewer.
- Não há termo de consentimento, política de privacidade operacional, exportação/deleção de dados pessoais ou trilha de auditoria em SQLite.
- A validação de upload depende de extensão e tamanho; não valida magic bytes, tipo MIME, executáveis disfarçados, limite de uploads por usuário/IP ou fórmulas maliciosas em CSV/Excel.
- `SECRET_KEY` possui fallback fixo de desenvolvimento; isso é aceitável apenas localmente, mas deve falhar ou alertar em produção.
- Strings de conexão são construídas interpolando usuário/senha diretamente; isso exige encoding seguro e cuidado para não vazar credenciais em logs.
- Não foram encontrados usos de `eval`, `exec` ou `pickle.loads` em dados do usuário durante a auditoria com ripgrep.

## Problemas de UX e produto

- A interface principal ainda usa componentes padrão do Streamlit, com título simples, `file_uploader` direto e mensagens genéricas.
- Não há design system global premium, tema Plotly customizado aplicado de forma consistente, dark mode global persistente, header com usuário/logout ou onboarding.
- A experiência mobile não tem estratégia explícita de navegação responsiva, bottom nav/drawer ou cards adaptáveis.
- Loading states dependem de spinner/progress bar; ainda não há skeleton screens, toasts premium, hover states ou empty states elegantes.

## Plano de ação priorizado

### Prioridade 0 — Estabilização antes das features

1. Alinhar a arquitetura testada com a arquitetura real: ou criar os pacotes `src.application`/`src.domain` esperados pelos testes, ou migrar os testes para os módulos reais.
2. Extrair o fluxo de `app.py` para funções testáveis (`main`, `render_upload_flow`, `validate_upload_size`) sem alterar comportamento visível.
3. Padronizar configurações críticas com validação via Pydantic ou dataclasses enquanto mantemos compatibilidade com variáveis de ambiente existentes.

### Prioridade 1 — Segurança

1. Criar o pacote `security/` com autenticação, sessões, RBAC, auditoria, anonimização, rate limiting e validação de upload.
2. Proteger o app inteiro por login antes de qualquer upload ou consulta a banco.
3. Implementar papéis `admin`, `analyst` e `viewer`, aplicando permissões no upload, ML, exportações, banco de dados e páginas administrativas.
4. Registrar em SQLite eventos sensíveis: login/logout, upload, execução de ML, exportação e ações administrativas.
5. Implementar validação de upload com limite de 100 MB, magic bytes, rejeição de executáveis/scripts, rate limiting e detecção de CSV/Excel Injection.
6. Adicionar anonimização opcional de CPF, CNPJ, e-mail, telefone e RG no fluxo de upload.
7. Criar `.env.example`, revisar `.gitignore` e remover qualquer fallback inseguro em produção.

### Prioridade 2 — UX premium

1. Criar `ui/theme.css` ou módulo equivalente para design system global com paleta slate/indigo/emerald/rose, Inter, cards, botões, responsividade e transições.
2. Adicionar dark mode persistente em `st.session_state` e propagar o template para gráficos Plotly.
3. Reestruturar header/sidebar para um padrão SaaS: logo, breadcrumb, avatar, toggle de tema e logout.
4. Adicionar empty states, skeleton screens e toasts para upload, processamento e erros comuns.
5. Revisar páginas principais para grids responsivos e reduzir texto explicativo excessivo.

### Prioridade 3 — IA e features novas

1. Consolidar a interface de provedores em um contrato único (`chat`, `generate_insights`, `explain_chart`).
2. Finalizar adapters OpenAI, Ollama, Gemini, Claude e Azure OpenAI com configuração via ambiente/st.secrets.
3. Criar chat contextual com resumo estruturado do DataFrame e histórico persistido em SQLite.
4. Gerar 3-5 insights automáticos após upload e cards de destaque no dashboard.
5. Expandir importação para Parquet, SQL, XML e API REST com preview de 100 linhas.
6. Adicionar exportação PowerPoint e HTML.

### Prioridade 4 — Deploy, qualidade e documentação

1. Corrigir Dockerfile para multi-stage, Python slim, usuário não-root, `curl` para healthcheck e cache eficiente.
2. Expandir `docker-compose.yml` com app, reverse proxy, Postgres e Redis opcionais.
3. Criar GitHub Actions para `ruff check`, `ruff format --check`, `pytest --cov` e build Docker.
4. Atualizar README e criar `docs/ARCHITECTURE.md`, `docs/SECURITY.md` e `docs/DEPLOY.md`.
5. Elevar cobertura gradualmente até 70%, priorizando `security/`, `core/`, `ai/`, `database/` e `machine_learning/`.

## Estratégia incremental recomendada para a Fase 2

1. Primeiro commit: estrutura `security/`, entidades simples, hash de senha e testes unitários isolados.
2. Segundo commit: login/logout em Streamlit e proteção global do `app.py`.
3. Terceiro commit: RBAC aplicado às páginas e ações sensíveis.
4. Quarto commit: auditoria em SQLite e telas administrativas.
5. Quinto commit: upload seguro, anonimização e testes de arquivos maliciosos.

## Critério de aprovação para avançar

A implementação da Fase 2 deve começar somente após aprovação deste plano. A ordem sugerida é manter segurança como prioridade máxima e corrigir primeiro a divergência entre testes e arquitetura real, pois isso reduz risco de regressões durante autenticação, RBAC e upload seguro.
