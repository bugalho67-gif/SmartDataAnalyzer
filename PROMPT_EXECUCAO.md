PROMPT DE EXECUÇÃO — SmartDataAnalyzer
Cole este prompt inteiro no Codex (web ou CLI) e peça para executar. O Codex lerá o repositório, analisará o estado atual e executará as melhorias de forma incremental e segura.
INSTRUÇÃO MESTRA
Você é o engenheiro sênior responsável por levar o SmartDataAnalyzer do estado atual (MVP funcional) para um produto SaaS pronto para produção.
O projeto é uma plataforma de análise de dados (EDA + ML + IA) em Python + Streamlit + SQLite + Docker.
Execute as tarefas abaixo de forma incremental, segura e modular. Nunca quebre funcionalidades existentes. Sempre teste antes de prosseguir.
FASE 1 — AUDITAR E PLANEJAR
Leia todo o repositório: app.py, todos os módulos em ai/, core/, machine_learning/, database/, providers/, config/, tests/, Dockerfile, docker-compose.yml, requirements.txt.
Identifique:
O que está funcionando vs. o que está incompleto ou mockado.
Débitos técnicos (código duplicado, falta de type hints, tratamento de erro frágil).
Vulnerabilidades de segurança (eval, falta de validação de upload, secrets expostos).
Problemas de UX (layout genérico, falta de dark mode, mobile quebrado).
Gere um PLANO DE AÇÃO detalhado em markdown, priorizando: segurança > UX > features novas > deploy.
Apresente o plano e aguarde minha aprovação antes de começar a implementação.
FASE 2 — SEGURANÇA (PRIORIDADE MÁXIMA)
2.1 Autenticação e Sessões
Crie um módulo security/auth.py com:
Registro de usuário (username, e-mail, senha).
Login com bcrypt/argon2 para hash de senha.
Sessão segura usando JWT (pyjwt) ou session state criptografado do Streamlit.
Logout e expiração de sessão (30 min de inatividade).
Proteja todas as rotas: se não estiver autenticado, redirecione para a tela de login.
Crie as páginas pages/login.py e pages/register.py.
2.2 Controle de Acesso (RBAC)
Crie security/rbac.py com roles: admin (tudo), analyst (upload, análise, ML), viewer (apenas visualizar dashboards e relatórios).
Aplique permissões em cada função do app (upload só para analyst+, deletar dataset só admin, etc.).
Adicione uma tela de gerenciamento de usuários visível apenas para admin.
2.3 LGPD e Auditoria
Crie security/audit.py que registre em SQLite:
Quem fez login/logout e quando.
Quem uploadou qual arquivo (nome, tamanho, timestamp).
Quem executou modelos de ML.
Quem exportou relatórios.
Crie uma tela de "Logs de Auditoria" para admins.
Adicione um modal de "Termo de Consentimento" na primeira vez que o usuário logar.
Adicione uma página de "Privacidade e Meus Dados" onde o usuário pode exportar ou solicitar a deleção de seus dados.
2.4 Proteção de Dados
Crie security/anonymizer.py que detecte e anonimize colunas sensíveis (CPF, CNPJ, e-mail, telefone, RG) usando regex/patterns brasileiros.
Ofereça ao usuário, no upload, a opção de "Anonimizar dados sensíveis automaticamente".
Criptografe o banco SQLite de produção usando SQLCipher ou criptografia a nível de aplicação para dados sensíveis.
2.5 Upload Seguro
Valide magic bytes de arquivos (não confie apenas na extensão).
Limite de tamanho: 100MB por arquivo, 5 uploads/hora por usuário (rate limiting por IP e por user_id).
Rejeite arquivos executáveis, scripts ou ZIPs não esperados.
Escaneie o CSV/Excel em busca de injeção de fórmula (CSV Injection: células começando com =, +, -, @).
2.6 Secrets e Configuração
Garanta que NENHUMA chave de API (OpenAI, Gemini, etc.) esteja hardcoded.
Use st.secrets com fallback para variáveis de ambiente.
Crie .env.example completo e atualize o .gitignore.
FASE 3 — DESIGN PREMIUM (ANTI-APP-DE-IA)
3.1 Design System Global
Injete CSS customizado no Streamlit via st.markdown(..., unsafe_allow_html=True) ou via arquivo ui/theme.css carregado no início do app.py.
Palette:
Fundo light: #f8fafc (slate-50)
Fundo dark: #0f172a (slate-950)
Primária: #4f46e5 (indigo-600)
Sucesso: #10b981 (emerald-500)
Erro: #f43f5e (rose-500)
Aviso: #f59e0b (amber-500)
Texto primário: #1e293b / #f1f5f9
Texto secundário: #64748b / #94a3b8
Fonte: Inter (Google Fonts) ou carregue localmente.
Cards: background: white; border-radius: 16px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;
Botões: border-radius: 10px; padding: 10px 20px; font-weight: 500; transition: all 0.2s ease; Hover: leve elevação + escurecimento.
3.2 Layout e Navegação
Sidebar minimalista: ícones (Material Symbols) + labels curtos. Collapsável.
Área principal em grid de 2-3 colunas para cards de métricas (não lista vertical).
Header fixo com: logo + nome do projeto + avatar do usuário + toggle dark mode + botão logout.
Breadcrumbs ou título de página contextual.
3.3 Dark Mode
Implemente toggle global no header que persiste em st.session_state.
Todos os componentes Plotly devem usar template="plotly_dark" quando dark mode ativo, e template="plotly_white" customizado no light.
Transição suave entre temas (CSS transition).
3.4 Microinterações e Polish
Skeleton screens enquanto carrega dados (não spinners genéricos do Streamlit).
Toasts de notificação no canto superior direito para sucesso/erro (implemente via CSS/JS injection ou componente customizado).
Hover states em cards (leve elevação translateY(-2px) + sombra maior).
Empty states elegantes: ícone ilustrativo + texto curto + CTA clara.
Tooltips informativos em ícones de ajuda (ℹ️).
3.5 Gráficos Plotly
Tema customizado: cores da palette, fonte Inter, títulos alinhados à esquerda, sem gridlines excessivas.
Margens generosas (layout.margin ajustado).
Legendas posicionadas de forma inteligente (top-right ou dentro do gráfico se possível).
3.6 Mobile
Teste com dev tools mobile (375px, 768px, 1440px).
Sidebar vira drawer/bottom sheet em mobile.
Grids de cards viram 1 coluna em telas pequenas.
Fontes adaptáveis (clamp() ou breakpoints).
3.7 Onboarding
Na primeira vez que um usuário logar, exiba um tour guiado (3-4 passos) destacando: upload, dashboard, ML, exportação.
Use st.session_state para marcar que o tour foi visto.
FASE 4 — FEATURES E INTELIGÊNCIA ARTIFICIAL
4.1 Provedores de IA
Finalize providers/ com adapters para:
OpenAI (GPT-4o, GPT-4o-mini)
Google Gemini
Anthropic Claude
Ollama (local)
Azure OpenAI
Crie ai/llm_factory.py que selecione o provedor baseado em configuração (LLM_PROVIDER no .env).
Cada adapter deve ter: chat(messages), generate_insights(data_summary), explain_chart(chart_data).
4.2 Chat Inteligente
Crie uma página pages/chat.py com interface de chat estilo ChatGPT (bubbles, avatar do bot, histórico).
O chat deve ter contexto do dataset atualmente carregado: o LLM recebe um resumo estruturado do DataFrame (schema, estatísticas, amostra) como system prompt.
Permita ao usuário fazer perguntas como: "Qual a correlação entre X e Y?", "Sugira o melhor modelo de ML para esses dados.", "Explique esse outlier."
Histórico de conversa por sessão (persistir em SQLite).
4.3 Insights Automáticos
Após o upload, gere automaticamente 3-5 insights em linguagem natural (via LLM) baseados no resumo estatístico.
Exiba como cards de destaque no topo do dashboard.
4.4 Auto-Dashboard
Permita ao usuário pedir: "Gere um dashboard automático para mim" e o sistema (via LLM + heurísticas) selecione os melhores gráficos e estatísticas para aquele dataset específico.
FASE 5 — MACHINE LEARNING E DADOS
5.1 Melhorias no ML
Adicione mais algoritmos: XGBoost, LightGBM, SVM, Neural Network (MLP via sklearn).
Cross-validation k-fold nos modelos.
Hyperparameter tuning com GridSearchCV ou Optuna.
Explicação de predições com SHAP values (quando aplicável).
Salvamento de modelos treinados (pickle/joblib) com metadados em SQLite.
5.2 Importação de Dados
Adicione suporte a: Parquet, SQL (conexão com string de conexão), XML, API REST (URL + headers).
Preview dos dados antes do upload completo (primeiras 100 linhas).
5.3 Exportação
Adicione exportação PowerPoint (python-pptx) e HTML (relatório interativo com Plotly embedado).
FASE 6 — TESTES E QUALIDADE
Atingir mínimo 70% de cobertura de testes.
Testes unitários para: core/, security/, ai/, machine_learning/, database/.
Testes de integração para: upload, autenticação, fluxo de ML completo.
Testes de UI/UX: verificar que dark mode persiste, que login funciona, que upload rejeita arquivos inválidos.
Configure pytest.ini e conftest.py.
Adicione ruff para lint e formatação.
FASE 7 — DEPLOY E DOCUMENTAÇÃO
7.1 Docker
Otimize o Dockerfile:
Multi-stage build (builder + runtime).
Imagem base python:3.11-slim.
Usuário não-root (USER app).
Healthcheck (HEALTHCHECK CMD curl -f http://localhost:8501/_stcore/health).
docker-compose.yml com:
App Streamlit
Nginx (reverse proxy + SSL)
PostgreSQL (opcional, para produção)
Redis (cache de sessões e rate limiting)
7.2 CI/CD
.github/workflows/ci.yml:
Roda ruff check e ruff format --check.
Roda pytest com coverage.
Builda imagem Docker.
.github/workflows/cd.yml (opcional): deploy automático para Streamlit Cloud ou VPS.
7.3 Documentação
Atualize README.md com:
Badges (build, coverage, Python version).
GIF de demonstração (placeholder se não tiver ainda).
Instruções de instalação detalhadas.
Lista completa de variáveis de ambiente.
Arquitetura do sistema (diagrama textual ou mermaid).
Crie docs/ARCHITECTURE.md explicando a estrutura de diretórios e fluxo de dados.
Crie docs/SECURITY.md com: checklist de segurança, como reportar vulnerabilidades, política de secrets.
Crie docs/DEPLOY.md com: Docker, Streamlit Cloud, AWS, Azure, GCP.
7.4 Makefile
makefile
dev:
	streamlit run app.py

test:
	pytest tests/ -v --cov=.

lint:
	ruff check . && ruff format .

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down
REGRAS DE OURO
Nunca use eval, exec, pickle.loads em dados do usuário.
Nunca commit secrets. Use .env.example e st.secrets.
Sempre valide inputs antes de processar.
Sempre logue ações sensíveis no audit log.
Mantenha o código em português (docstrings, mensagens de erro, labels da UI — o público-alvo é brasileiro).
Teste em dark mode e mobile antes de marcar uma tela como pronta.
Faça commits pequenos e atômicos com mensagens claras em português.
ENTREGA ESPERADA
Ao final, o projeto deve:
[ ] Ter autenticação funcional com 3 roles.
[ ] Estar protegido contra os 10 principais riscos de segurança (OWASP Top 10 para apps web).
[ ] Ter um design que pareça um SaaS premium (não um template de IA).
[ ] Ter dark mode, responsividade e onboarding.
[ ] Ter chat com IA funcional (mínimo OpenAI + Ollama).
[ ] Ter testes com 70%+ de cobertura.
[ ] Ter Docker pronto para produção.
[ ] Ter CI/CD no GitHub Actions.
[ ] Ter documentação completa.
Execute o plano fase por fase. Apresente o resultado de cada fase antes de prosseguir para a próxima.
