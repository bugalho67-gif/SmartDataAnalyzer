# 📊 SmartDataAnalyzer

<p align="center">

<img src="docs/images/logo.png" width="180"/>

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.x-blue?style=for-the-badge&logo=pandas)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-Latest-orange?style=for-the-badge&logo=scikit-learn)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blueviolet?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

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

- CSV
- Excel (.xlsx)
- JSON

Em breve:

- Parquet
- SQL
- XML
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
- Pizza
- Linha
- Dispersão
- Boxplot
- Heatmap
- Correlação

Os gráficos são escolhidos automaticamente conforme o tipo da variável.

---

## 📉 Estatísticas

Análise estatística completa.

Incluindo:

- Média
- Mediana
- Moda
- Variância
- Desvio padrão
- Quartis
- Percentis
- Máximo
- Mínimo

---

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

# 🎨 Design premium

A Fase 3 adiciona uma camada visual SaaS sobre o Streamlit sem trocar o framework:

- Design system em `ui/theme.css` com fonte Inter, paleta slate/indigo/emerald/rose, cards arredondados, sombras sutis e transições de hover.
- Toggle global de modo escuro persistido em `st.session_state`.
- Header contextual com usuário autenticado e estado vazio elegante para o fluxo inicial de upload.
- Tema Plotly centralizado para gráficos claros/escuros, com paleta consistente, fonte Inter, margens maiores e grids menos agressivos.
- Ajustes responsivos para reduzir a aparência de app genérico em telas menores.

---

# 🤖 Inteligência Artificial

O projeto possui uma arquitetura preparada para múltiplos provedores de IA.

Atualmente, a Fase 4 adiciona uma factory unificada em `ai/llm_factory.py` com adapters para:

- Local ✅
- OpenAI ✅
- Gemini ✅
- Claude ✅
- Ollama ✅
- Azure OpenAI ✅

Cada adapter expõe os métodos `chat(messages)`, `generate_insights(data_summary)` e `explain_chart(chart_data)`, mantendo compatibilidade com o método legado `ask(question, context)`. Configure o provedor com `LLM_PROVIDER` ou `AI_PROVIDER` no `.env`.

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

---

## AutoML

Comparação automática entre modelos para selecionar o melhor algoritmo conforme o dataset.

---

## Feature Importance

Visualização automática da importância das variáveis.

---

# 📄 Relatórios

Exportação em:

- PDF
- CSV
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

A Fase 2 começou com uma base local de segurança para reduzir riscos antes das próximas features:

- Login obrigatório antes de acessar upload, análise ou banco de dados.
- Hash de senha com PBKDF2-HMAC e salt único por usuário.
- Sessões persistidas em SQLite com expiração por inatividade de 30 minutos.
- RBAC com papéis `admin`, `analyst` e `viewer`.
- Termo de consentimento LGPD no primeiro acesso autenticado.
- Logs de auditoria em SQLite para eventos sensíveis.
- Validação segura de upload com limite de 100 MB, rejeição de executáveis/scripts, checagem básica de magic bytes e detecção de CSV/Formula Injection.
- Anonimização automática opcional de CPF, CNPJ, e-mail, telefone e RG.

Conta administrativa local inicial:

```text
E-mail: admin@smartdataanalyzer.dev
Senha: valor de DEFAULT_ADMIN_PASSWORD ou admin12345 em desenvolvimento
```

> Em produção, configure `DEFAULT_ADMIN_PASSWORD`, `SECRET_KEY` e chaves de provedores via `.env`, `st.secrets` ou variáveis de ambiente. Nunca commite secrets.

## Variáveis de ambiente principais

Consulte `.env.example` para o template completo. As variáveis mais importantes são:

- `DEFAULT_ADMIN_PASSWORD`: senha inicial do admin local.
- `SECRET_KEY`: segredo da aplicação em produção.
- `MAX_UPLOAD_SIZE_MB`: limite de upload, com padrão seguro de 100 MB.
- `AI_PROVIDER`, `AI_MODEL`, `OPENAI_API_KEY`: configuração dos provedores de IA.


O projeto foi desenvolvido considerando boas práticas de segurança.

Recursos atuais:

- Configuração centralizada
- Variáveis de ambiente (.env)
- Logging
- Tratamento de exceções
- Upload controlado

Próximas implementações:

- Criptografia
- Anonimização de dados
- Controle de acesso
- Auditoria
- Sessões seguras
- LGPD
- Rate Limiting

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

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-Learn
- ReportLab
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

Execute.

```bash
streamlit run app.py
```

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
- [ ] Dark Mode
- [ ] Animações suaves
- [ ] Dashboard Premium
- [ ] Assistente Inteligente

---

## Q3 — Segurança

- [ ] Autenticação
- [ ] Controle de usuários
- [ ] Criptografia
- [ ] LGPD
- [ ] Auditoria
- [ ] Backup automático

---

## Q4 — Inteligência Artificial

- [ ] OpenAI
- [ ] Gemini
- [ ] Claude
- [ ] Ollama
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
| IA | 🚧 |
| Machine Learning | ✅ |
| Banco de Dados | ✅ |
| Exportação | ✅ |
| Docker | ✅ |
| Segurança | 🚧 |

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

Projeto desenvolvido como plataforma de análise inteligente de dados, unindo Data Analytics, Machine Learning e Inteligência Artificial, com foco em produtividade, arquitetura escalável e experiência moderna para analistas de dados.