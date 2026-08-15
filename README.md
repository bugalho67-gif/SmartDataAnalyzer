 # 🚀 Sobre o projeto
 
 O **SmartDataAnalyzer** é uma plataforma inteligente para análise exploratória de dados (EDA), Machine Learning e geração automática de insights utilizando Inteligência Artificial.
 
 O objetivo do projeto é permitir que qualquer usuário envie um conjunto de dados (CSV, Excel ou JSON) e obtenha, em poucos segundos:
 
 - Dashboard automático;
 - Estatísticas descritivas;
 - Visualizações inteligentes;
 - Correlações;
 - Detecção de outliers;
 - Diagnóstico da qualidade dos dados;
 - Modelos de Machine Learning;
 - Relatórios em PDF;
 - Exportação dos resultados;
 - Insights automáticos gerados por IA.
 
 Tudo isso através de uma interface moderna, intuitiva e preparada para desktop e dispositivos móveis.
 
 ---
 
 # ✨ Principais funcionalidades
 
 ## 📂 Importação de dados
 
+A Fase 5 adiciona preview seguro das primeiras 100 linhas antes do processamento completo.
+
+
 - CSV
 - Excel (.xlsx)
 - JSON
+- Parquet (depende de `pyarrow`)
+- XML
 
 Em breve:
 
-- Parquet
 - SQL
-- XML
 - API REST
 
 ---
 
 ## 📈 Dashboard Automático
 
 Após o upload dos dados o sistema gera automaticamente:
 
 - Quantidade de registros
 - Quantidade de colunas
 - Valores nulos
 - Duplicados
 - Memória utilizada
 - Pré-visualização dos dados
 
 ---
 
 ## 📊 Visualizações Inteligentes
 
 Gráficos automáticos utilizando Plotly.
 
 Entre eles:
 
 - Histograma
 - Barras
@@ -109,67 +112,76 @@ Incluindo:
 
 ## 🚨 Detecção de Outliers
 
 Métodos disponíveis:
 
 - IQR
 - Z-Score
 
 Visualização através de BoxPlot.
 
 ---
 
 ## 🧹 Qualidade dos Dados
 
 Análise automática de:
 
 - Valores ausentes
 - Valores duplicados
 - Colunas constantes
 - Tipos incorretos
 - Cardinalidade
 - Distribuição
 
 ---
 
-# 🤖 Inteligência Artificial
+# 🎨 Design premium
 
-O projeto possui uma arquitetura preparada para múltiplos provedores de IA.
+A Fase 3 adiciona uma camada visual SaaS sobre o Streamlit sem trocar o framework:
 
-Atualmente:
+- Design system em `ui/theme.css` com fonte Inter, paleta slate/indigo/emerald/rose, cards arredondados, sombras sutis e transições de hover.
+- Toggle global de modo escuro persistido em `st.session_state`.
+- Header contextual com usuário autenticado e estado vazio elegante para o fluxo inicial de upload.
+- Tema Plotly centralizado para gráficos claros/escuros, com paleta consistente, fonte Inter, margens maiores e grids menos agressivos.
+- Ajustes responsivos para reduzir a aparência de app genérico em telas menores.
 
-- Provider Local ✅
+---
 
-Arquitetura preparada para:
+# 🤖 Inteligência Artificial
+
+O projeto possui uma arquitetura preparada para múltiplos provedores de IA.
+
+Atualmente, a Fase 4 adiciona uma factory unificada em `ai/llm_factory.py` com adapters para:
 
-- OpenAI
-- Gemini
-- Claude
-- Ollama
-- Azure OpenAI
+- Local ✅
+- OpenAI ✅
+- Gemini ✅
+- Claude ✅
+- Ollama ✅
+- Azure OpenAI ✅
 
-A IA poderá responder perguntas sobre os dados, gerar diagnósticos automáticos e auxiliar na interpretação dos resultados.
+Cada adapter expõe os métodos `chat(messages)`, `generate_insights(data_summary)` e `explain_chart(chart_data)`, mantendo compatibilidade com o método legado `ask(question, context)`. Configure o provedor com `LLM_PROVIDER` ou `AI_PROVIDER` no `.env`.
 
 ---
 
 # 🧠 Machine Learning
 
 O projeto inclui um módulo completo de Machine Learning.
 
 ## Algoritmos
 
 - Regressão Linear
 - Decision Tree
 - Random Forest
 - Logistic Regression
 - KNN
 
 ---
 
 ## Avaliação
 
 - Accuracy
 - Precision
 - Recall
 - F1 Score
 - ROC Curve
 - Confusion Matrix
@@ -197,69 +209,97 @@ Exportação em:
 - Excel
 
 Em breve:
 
 - PowerPoint
 - HTML
 
 ---
 
 # 🗄 Banco de Dados
 
 Suporte para:
 
 - SQLite ✅
 
 Arquitetura preparada para:
 
 - PostgreSQL
 - MySQL
 - SQL Server
 
 ---
 
 # 🔒 Segurança
 
+A Fase 2 começou com uma base local de segurança para reduzir riscos antes das próximas features:
+
+- Login obrigatório antes de acessar upload, análise ou banco de dados.
+- Hash de senha com PBKDF2-HMAC e salt único por usuário.
+- Sessões persistidas em SQLite com expiração por inatividade de 30 minutos.
+- RBAC com papéis `admin`, `analyst` e `viewer`.
+- Termo de consentimento LGPD no primeiro acesso autenticado.
+- Logs de auditoria em SQLite para eventos sensíveis.
+- Validação segura de upload com limite de 100 MB, rejeição de executáveis/scripts, checagem básica de magic bytes e detecção de CSV/Formula Injection.
+- Anonimização automática opcional de CPF, CNPJ, e-mail, telefone e RG.
+
+Conta administrativa local inicial:
+
+```text
+E-mail: admin@smartdataanalyzer.dev
+Senha: valor de DEFAULT_ADMIN_PASSWORD ou admin12345 em desenvolvimento
+```
+
+> Em produção, configure `DEFAULT_ADMIN_PASSWORD`, `SECRET_KEY` e chaves de provedores via `.env`, `st.secrets` ou variáveis de ambiente. Nunca commite secrets.
+
+## Variáveis de ambiente principais
+
+Consulte `.env.example` para o template completo. As variáveis mais importantes são:
+
+- `DEFAULT_ADMIN_PASSWORD`: senha inicial do admin local.
+- `SECRET_KEY`: segredo da aplicação em produção.
+- `MAX_UPLOAD_SIZE_MB`: limite de upload, com padrão seguro de 100 MB.
+- `AI_PROVIDER`, `AI_MODEL`, `OPENAI_API_KEY`: configuração dos provedores de IA.
+- `LLM_PROVIDER`: adapter ativo (`local`, `openai`, `gemini`, `claude`, `ollama` ou
+  `azure_openai`).
+- `DATABASE_URL`: conexão SQLite por padrão ou conexão externa em produção.
+- `POSTGRES_PASSWORD` e `REDIS_URL`: infraestrutura do perfil Docker `production`.
+
+
 O projeto foi desenvolvido considerando boas práticas de segurança.
 
 Recursos atuais:
 
 - Configuração centralizada
 - Variáveis de ambiente (.env)
 - Logging
 - Tratamento de exceções
 - Upload controlado
 
-Próximas implementações:
-
-- Criptografia
-- Anonimização de dados
-- Controle de acesso
-- Auditoria
-- Sessões seguras
-- LGPD
-- Rate Limiting
+Os controles atuais incluem autenticação, RBAC, anonimização opcional, auditoria, consentimento
+LGPD, sessões com expiração, rate limiting e validação defensiva de uploads. Consulte
+[`docs/SECURITY.md`](docs/SECURITY.md) antes de publicar uma instância.
 
 ---
 
 # 🏗 Arquitetura
 
 ```
 SmartDataAnalyzer/
 
 ├── ai/
 ├── config/
 ├── core/
 ├── database/
 ├── machine_learning/
 ├── providers/
 ├── tests/
 ├── docs/
 ├── app.py
 ├── Dockerfile
 ├── docker-compose.yml
 └── README.md
 ```
 
 ---
 
 # ⚙ Tecnologias
@@ -274,151 +314,170 @@ SmartDataAnalyzer/
 - SQLite
 - Docker
 
 ---
 
 # 🚀 Instalação
 
 Clone o projeto.
 
 ```bash
 git clone https://github.com/SEU-USUARIO/SmartDataAnalyzer.git
 ```
 
 Entre na pasta.
 
 ```bash
 cd SmartDataAnalyzer
 ```
 
 Instale as dependências.
 
 ```bash
 pip install -r requirements.txt
 ```
 
+Para contribuir e executar lint/cobertura, instale também as ferramentas de desenvolvimento:
+
+```bash
+pip install -r requirements-dev.txt
+```
+
 Execute.
 
 ```bash
 streamlit run app.py
 ```
 
+Também é possível usar os atalhos padronizados:
+
+```bash
+make lint
+make test
+make up
+```
+
+O Nginx fica disponível em `http://localhost:8080`, e o Streamlit diretamente em
+`http://localhost:8501`. O perfil de produção (`make deploy`) exige credenciais externas e
+também inicia PostgreSQL e Redis. Veja os guias de [arquitetura](docs/ARCHITECTURE.md),
+[deploy](docs/DEPLOY.md) e [segurança](docs/SECURITY.md).
+
 ---
 
 # 📸 Demonstração
 
 Em breve serão adicionados:
 
 - GIF do sistema
 - Screenshots
 - Vídeo de demonstração
 
 ---
 
 # 📅 Roadmap
 
 ## Q1 — Estrutura e Arquitetura
 
 - [x] Upload de arquivos
 - [x] Dashboard
 - [x] Estatísticas
 - [x] Gráficos
 - [x] Correlação
 - [x] Outliers
 - [x] Qualidade dos dados
 - [x] Machine Learning
 - [x] AutoML
 - [x] Exportação
 - [x] Banco de Dados
 - [x] Docker
 - [x] Configuração centralizada
 
 ---
 
 ## Q2 — Interface e Experiência
 
 - [ ] Design inspirado na Apple
 - [ ] Responsividade completa
-- [ ] Dark Mode
+- [x] Dark Mode
 - [ ] Animações suaves
-- [ ] Dashboard Premium
+- [x] Dashboard Premium
 - [ ] Assistente Inteligente
 
 ---
 
 ## Q3 — Segurança
 
-- [ ] Autenticação
-- [ ] Controle de usuários
+- [x] Autenticação
+- [ ] Gerenciamento administrativo completo de usuários
 - [ ] Criptografia
-- [ ] LGPD
-- [ ] Auditoria
+- [x] LGPD
+- [x] Auditoria
 - [ ] Backup automático
 
 ---
 
 ## Q4 — Inteligência Artificial
 
-- [ ] OpenAI
-- [ ] Gemini
-- [ ] Claude
-- [ ] Ollama
+- [x] OpenAI
+- [x] Gemini
+- [x] Claude
+- [x] Ollama
 - [ ] Chat Inteligente
 - [ ] Geração automática de dashboards
 - [ ] Explicação automática de gráficos
 
 ---
 
 ## Q5 — Deploy
 
 - [ ] Streamlit Cloud
 - [ ] Docker Hub
 - [ ] AWS
 - [ ] Azure
 - [ ] Google Cloud
 
 ---
 
 # 📈 Situação do Projeto
 
 | Módulo | Status |
 |---------|--------|
 | Upload | ✅ |
 | Dashboard | ✅ |
 | Estatísticas | ✅ |
 | Gráficos | ✅ |
 | Correlação | ✅ |
 | Outliers | ✅ |
 | Qualidade | ✅ |
-| IA | 🚧 |
+| IA | ✅ |
 | Machine Learning | ✅ |
 | Banco de Dados | ✅ |
 | Exportação | ✅ |
 | Docker | ✅ |
-| Segurança | 🚧 |
+| Segurança | ✅ |
 
 ---
 
 # 🤝 Contribuindo
 
 Contribuições são bem-vindas.
 
 Caso queira colaborar:
 
 1. Faça um Fork
 2. Crie uma branch
 3. Faça suas alterações
 4. Abra um Pull Request
 
 ---
 
 # 📜 Licença
 
 Este projeto está licenciado sob a licença MIT.
 
 ---
 
 # 👨‍💻 Autor
 
 **Gabriel de Lima Bugalho**
 
-Projeto desenvolvido como plataforma de análise inteligente de dados, unindo Data Analytics, Machine Learning e Inteligência Artificial, com foco em produtividade, arquitetura escalável e experiência moderna para analistas de dados.
\ No newline at end of file
+Projeto desenvolvido como plataforma de análise inteligente de dados, unindo Data Analytics, Machine Learning e Inteligência Artificial, com foco em produtividade, arquitetura escalável e experiência moderna para analistas de dados.
