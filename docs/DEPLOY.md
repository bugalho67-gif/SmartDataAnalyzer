# Guia de deploy

## Docker Compose

1. Copie `.env.example` para `.env` e preencha segredos fora do Git.
2. Execute `make build` e `make up` para desenvolvimento.
3. Acesse diretamente `http://localhost:8501` ou pelo Nginx em
   `http://localhost:8080`.
4. Para infraestrutura adicional, defina `POSTGRES_PASSWORD`, `DATABASE_URL` e execute
   `make deploy`; o perfil `production` inicia PostgreSQL e Redis.

Volumes nomeados preservam bancos. `exports/` e `logs/` são bind mounts para facilitar a
operação local. Em nuvem, prefira volumes criptografados e logging externo.

## TLS

O arquivo `deploy/nginx.conf` fornece reverse proxy, WebSocket e headers. Para produção,
adicione certificado no load balancer da plataforma ou monte certificados no Nginx e escute
na porta 443. Nunca exponha tráfego autenticado sem HTTPS.

## Streamlit Community Cloud

- defina `app.py` como entrypoint;
- copie variáveis sensíveis para **Secrets**, nunca para o repositório;
- não dependa do SQLite local para persistência durável;
- use PostgreSQL externo quando dados precisarem sobreviver a redeploys.

## AWS, Azure e GCP

A imagem pode ser publicada em ECR, ACR ou Artifact Registry e executada em ECS/Fargate,
Azure Container Apps ou Cloud Run. Configure porta 8501, healthcheck `/_stcore/health`, HTTPS,
secret manager, banco gerenciado e volume/objeto criptografado. Execute migrações antes de
trocar tráfego e mantenha rollback para a imagem anterior.

## Verificação

```bash
make lint
make test
docker compose config
curl --fail http://localhost:8501/_stcore/health
```
