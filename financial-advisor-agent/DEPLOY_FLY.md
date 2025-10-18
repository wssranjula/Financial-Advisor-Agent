# Deploying to Fly.io

This document describes how to deploy the Financial Advisor AI Agent's backend and frontend to Fly.io. It assumes you already have the repository cloned and the Dockerfiles and example `fly.toml` files present in `backend/` and `frontend/`.

Sections:
- Prerequisites
- Create Fly apps
- Create and attach Postgres (pgvector)
- Redis recommendations
- Set secrets (API keys & env vars)
- Deploy backend
- Run migrations
- Deploy frontend
- Optional: Celery worker
- Troubleshooting & notes

---

## Prerequisites

- Install `flyctl` and log in:

  ```powershell
  # Interactive login
  flyctl auth login
  ```

- Choose a region and organization in Fly. Keep these handy (e.g. `iad`, `ord`, `ams`).
- Make sure you have your AI provider API keys (OpenAI, Anthropic) and OAuth credentials if you plan to use integrations.

## 1) Create Fly apps

We recommend two separate apps:

- Backend: `financial-advisor-backend`
- Frontend: `financial-advisor-frontend`

Create backend app:

```powershell
cd backend
flyctl apps create financial-advisor-backend --org <your-org> --region <region>
```

Create frontend app:

```powershell
cd frontend
flyctl apps create financial-advisor-frontend --org <your-org> --region <region>
```

If you prefer interactive setup, run `flyctl launch` from each directory and follow the prompts.

## 2) Create and attach Postgres (with pgvector)

Create a managed Postgres cluster and attach it to the backend app:

```powershell
flyctl postgres create --name financial-advisor-db --org <your-org> --region <region>
# attach to backend
flyctl postgres attach --app financial-advisor-backend --name financial-advisor-db
```

After the DB is provisioned, enable the `pgvector` extension:

```powershell
# connect to the postgres cluster
flyctl pg connect -a financial-advisor-db
# in psql shell:
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

Fly will also inject a `DATABASE_URL` into the backend app when the DB is attached. Confirm with `flyctl secrets list -a financial-advisor-backend` or via the Fly dashboard.

## 3) Redis

The app expects `REDIS_URL`. Options:

- Recommended: Use a managed Redis provider (Upstash, Redis Cloud). Create an instance and copy the URL.
- Alternative: Run Redis as another Fly app (not recommended for production).

Set `REDIS_URL` in the backend app:

```powershell
flyctl secrets set REDIS_URL="redis://:password@host:port" -a financial-advisor-backend
```

## 4) Required secrets & env vars

At minimum set the following (customize values):

- `SECRET_KEY` — random secret string
- `ENCRYPTION_KEY` — random 32/64 byte secret
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (depending on provider)
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (if using Google OAuth)
- `HUBSPOT_*` OAuth vars if using HubSpot
- `FRONTEND_URL` — will be the frontend Fly URL (e.g. `https://financial-advisor-frontend.fly.dev`)

Example:

```powershell
flyctl secrets set \
  SECRET_KEY="$(openssl rand -hex 32)" \
  ENCRYPTION_KEY="$(openssl rand -hex 32)" \
  OPENAI_API_KEY="sk_..." \
  ANTHROPIC_API_KEY="claude-..." \
  FRONTEND_URL="https://financial-advisor-frontend.fly.dev" \
  -a financial-advisor-backend
```

Note: On Windows, you may need to substitute your preferred random generation method rather than `openssl`.

## 5) Deploy backend

From `backend/` (Dockerfile present):

```powershell
cd backend
flyctl deploy --app financial-advisor-backend
```

This will build the Docker image and deploy. The `backend/Dockerfile` runs `uvicorn app.main:app` on `$PORT`.

## 6) Run migrations

After the app is up, run Alembic migrations to create tables:

Option A: One-off remote command

```powershell
flyctl ssh console -a financial-advisor-backend
# then inside the container:
alembic upgrade head
```

Option B: Use `flyctl run` for one-off commands if available.

## 7) Deploy frontend

Set `NEXT_PUBLIC_API_URL` to the backend URL (either via `fly.toml` or secret/env):

```powershell
cd frontend
flyctl secrets set NEXT_PUBLIC_API_URL="https://financial-advisor-backend.fly.dev" -a financial-advisor-frontend
flyctl deploy --app financial-advisor-frontend
```

The `frontend/Dockerfile` builds the Next app and starts it on port 3000.

## 8) Optional: Celery worker

If you use Celery, run it as a separate Fly app or process. Example `fly.toml` process type `worker` with command:

```
celery -A app.celery_app worker --loglevel=info
```

Ensure `REDIS_URL` is set.

## Troubleshooting & notes
- If the Docker build fails due to compilation errors for packages like `psycopg2`, make sure `libpq-dev` and `build-essential` are installed in the Dockerfile (the provided Dockerfile includes these packages).
- To inspect logs: `flyctl logs -a financial-advisor-backend`.
- To run database checks: `flyctl pg connect -a financial-advisor-db`.
- If streaming endpoints appear blocked, check Fly health checks and concurrency settings in `fly.toml`.

---

If you want I can add PowerShell scripts to automate the `flyctl` steps (create apps, set secrets, attach DB, deploy). Tell me which app names, org, and region you'd like to use and I can generate them.
