# Segurança

## Operação segura

- Nunca versione `.env`, bancos locais, logs ou chaves de API.
- Troque a senha administrativa inicial e use um `SECRET_KEY` aleatório em produção.
- Termine TLS no proxy ou balanceador; o Nginx incluído configura headers, mas certificados
  devem ser provisionados pela plataforma de deploy.
- Restrinja acesso ao diretório `data/` e mantenha backups criptografados.
- Ative PostgreSQL e Redis com credenciais do secret manager da plataforma.
- Revise os logs de auditoria e aplique retenção compatível com a LGPD.

## Controles implementados

- autenticação com expiração, RBAC e auditoria em SQLite;
- validação de tamanho, formato, magic bytes e fórmulas em uploads;
- anonimização opcional de CPF, CNPJ, RG, e-mail e telefone;
- limite de upload por usuário;
- headers de segurança no proxy Nginx;
- execução do container por usuário não-root.

## Limitações conhecidas

O armazenamento local atende desenvolvimento e instâncias únicas. Em produção distribuída,
use PostgreSQL para persistência, Redis para sessão/rate limiting e criptografia gerenciada
para volumes e backups. CSP contém permissões necessárias ao frontend do Streamlit e deve ser
revalidada a cada atualização do framework.

## Reporte de vulnerabilidade

Não abra uma issue pública com detalhes exploráveis. Use o canal privado de segurança do
repositório (GitHub Security Advisories) e informe versão, impacto, reprodução e mitigação
sugerida. Não inclua dados pessoais ou credenciais reais.
