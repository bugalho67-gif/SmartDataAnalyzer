SmartDataAnalyzer — Instruções para Agentes Codex
Contexto do Projeto
O SmartDataAnalyzer é uma plataforma de análise exploratória de dados (EDA), Machine Learning e geração de insights via IA. Stack: Python + Streamlit + Pandas + Plotly + Scikit-Learn + SQLite + Docker.
O projeto já possui: upload de dados, dashboard automático, estatísticas, gráficos, correlação, outliers, qualidade de dados, ML (AutoML), exportação PDF/CSV/Excel, SQLite e Docker.
O que está pendente ou incompleto: segurança, autenticação, LGPD, design premium (não pode parecer app genérico de IA), integração com provedores de IA (OpenAI, Gemini, Claude, Ollama), responsividade fina, testes automatizados, deploy pronto.
Regras Gerais de Desenvolvimento
Nunca quebre funcionalidades existentes. Antes de alterar qualquer módulo, leia o código atual, entenda o fluxo e só então modifique.
Mantenha a arquitetura modular. Cada feature nova deve morar no diretório correto (ai/, core/, machine_learning/, database/, providers/, security/, ui/).
Siga PEP 8 e mantenha docstrings em português (o projeto é brasileiro).
Type hints obrigatórios em todas as funções novas ou refatoradas.
Não adicione dependências sem justificativa. Se precisar de um novo pacote, cite o motivo e adicione ao requirements.txt e Dockerfile.
Commits atômicos: cada mudança deve ser pequena, revisável e com mensagem clara em português.
Não modifique .env ou arquivos de secrets. Use templates (.env.example).
1. Desenvolvimento de Features
Prioridades
Finalizar o módulo de IA (ai/, providers/): integrar OpenAI, Gemini, Claude, Ollama, Azure OpenAI via interface unificada.
Chat inteligente sobre os dados com contexto do dataset carregado.
Geração automática de dashboards e explicação de gráficos via IA.
Suporte a Parquet, SQL, XML, API REST na importação.
Exportação PowerPoint e HTML dos relatórios.
Suporte a PostgreSQL, MySQL, SQL Server (além do SQLite existente).
Padrões de Código
Use pydantic para validação de configurações e schemas de dados.
Use pytest para todos os testes novos.
Use logging centralizado (nunca print em produção).
Tratamento de exceções com mensagens amigáveis ao usuário (Streamlit).
2. Segurança (Crítico)
Obrigatório implementar
Autenticação: sistema de login com hash de senha (bcrypt/argon2), sessões seguras (JWT com expiração ou session management do Streamlit).
Controle de acesso (RBAC): roles admin, analyst, viewer. Cada role vê apenas o que pode.
Criptografia: criptografar dados sensíveis em repouso (SQLite) e em trânsito (TLS/HTTPS no deploy).
Anonimização de dados: opção de anonimizar colunas sensíveis (CPF, e-mail, telefone) antes de processar.
LGPD compliance:
Termo de consentimento no primeiro acesso.
Política de privacidade visível.
Opção de exportar/deletar dados pessoais do usuário.
Log de auditoria de ações (quem acessou qual dataset e quando).
Rate Limiting: limitar uploads por usuário/hora para evitar abuse.
Validação de upload: verificar magic bytes, limitar tamanho (max 100MB), rejeitar executáveis.
Sanitização de inputs: nunca executar código dinâmico baseado em input do usuário (eval, exec proibidos).
Secrets management: nunca commitar chaves de API. Usar st.secrets ou variáveis de ambiente.
CSP e headers de segurança no deploy (nginx/traefik).
3. Aparência e UX (Anti-App-de-IA)
Diretriz principal
O app NÃO pode parecer genérico, cinza, com botões gigantes e layout de template. Deve parecer um produto SaaS premium, pensado por um designer.
Design System
Cores: palette sofisticada, não os defaults do Streamlit. Sugestão: fundo slate-50 / slate-950 (dark), primária indigo-600, acentos emerald-500 para sucesso, rose-500 para erro. Nunca usar o azul padrão do Streamlit.
Tipografia: usar fonte moderna (Inter ou Geist) via CSS injection no Streamlit. Tamanhos hierárquicos claros.
Espaçamento: padding generoso (24–32px), cards com sombra sutil (box-shadow: 0 1px 3px rgba(0,0,0,0.1)), bordas arredondadas (border-radius: 12px), não os quadradões padrão.
Dark Mode: implementar toggle global que persiste na sessão. Todos os gráficos Plotly devem respeitar o tema.
Animações: transições suaves (0.2s ease) nos cards e botões. Nada de "popping" instantâneo.
Microinterações: hover states nos cards, loading skeletons em vez de spinners genéricos, toasts de notificação no canto superior direito.
Layout: sidebar minimalista (ícones + labels), área principal em grid de cards, não lista vertical interminável.
Gráficos Plotly: tema customizado com cores da palette, fonte consistente, títulos bem posicionados, sem gridlines excessivas.
Responsividade: funcionar perfeitamente em mobile. Sidebar vira bottom nav ou hamburger menu.
Empty states: ilustrações ou ícones elegantes quando não há dados, nunca uma tela em branco.
Onboarding: tour guiado na primeira vez que o usuário entra (usando st.session_state).
O que EVITAR
Botões st.button gigantes e azuis empilhados.
Texto explicativo excessivo em cima de cada seção.
Layout de uma única coluna para tudo.
Cores neon ou gradientes agressivos.
Emojis demais (máximo 1 por card).
4. Preparar para Funcionar (Deploy)
Obrigatório
Dockerfile otimizado (multi-stage, imagem slim, não root user).
docker-compose.yml com serviços: app, nginx/traefik, postgres (futuro), redis (cache/sessions).
Makefile ou scripts com comandos: make dev, make test, make build, make deploy.
Healthcheck no container.
CI/CD básico: GitHub Actions para lint (ruff), testes (pytest), build Docker.
README.md atualizado com: instalação, variáveis de ambiente, arquitetura, contribuição.
docs/ com: arquitetura, guia de deploy, guia de segurança.
tests/ com cobertura mínima de 70%.
Comandos do Projeto
bash
# Ambiente
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Execução
streamlit run app.py

# Testes
pytest tests/ -v --cov=core --cov=ai --cov=machine_learning --cov=database --cov=security

# Lint
ruff check . && ruff format .

# Docker
docker-compose up --build
Checklist de Entrega
Antes de considerar uma tarefa concluída:
[ ] Código passa em ruff check e pytest.
[ ] Não há secrets hardcoded.
[ ] UI foi testada em mobile (dev tools).
[ ] Dark mode funciona em todas as telas.
[ ] Logging de auditoria está ativo para ações sensíveis.
[ ] Documentação foi atualizada.
