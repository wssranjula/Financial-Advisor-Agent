# Deploying the Frontend to Vercel (and Backend Options)

This document explains how to deploy the `frontend/` (Next.js 14) on Vercel, and reviews options for the backend (keep on Fly, deploy to Render, or use Vercel serverless functions / Edge Functions).

## Summary recommendation

- Deploy the frontend to Vercel (best developer experience for Next.js).
- Keep the backend as a separate service (Fly, Render, or similar). The backend uses long-lived SSE streams, DB connections, and heavy Python dependencies better suited to a full container (Fly or Render) rather than serverless functions.

## 1) Prepare the frontend

- Ensure `frontend/package.json` and `next.config.js` are committed.
- Set `NEXT_PUBLIC_API_URL` to the production backend URL via Vercel environment variables.

## 2) Create a Vercel project

1. Sign in to Vercel (https://vercel.com) and connect your Git provider (GitHub/GitLab/Bitbucket).
2. Import the repository and select the `frontend` directory as the root for the project:
   - During setup, set the `Root Directory` to `frontend`.

3. Set build settings (these are usually auto-detected for Next.js):
   - Framework: Next.js
   - Build command: `npm run build`
   - Output Directory: (leave default; Next takes care of it)

## 3) Environment variables on Vercel

Set these environment variables in the Vercel project (Dashboard -> Settings -> Environment Variables):

- `NEXT_PUBLIC_API_URL` — the URL of your backend (e.g. `https://financial-advisor-backend.fly.dev` or a Render URL)

If your frontend needs to talk to external services directly (e.g. analytics), set those env vars too. Do NOT put server-only secrets in `NEXT_PUBLIC_*` variables.

## 4) Build & Deploy

- Vercel will run the build automatically on push to the branch you selected (e.g. `main`). You can also trigger a manual deploy from the Vercel dashboard.

## 5) Backend deployment options

Option A — Keep backend on Fly (recommended if already set up):
- Use the Fly deployment steps in `DEPLOY_FLY.md` to deploy the backend. Set `NEXT_PUBLIC_API_URL` to the Fly backend URL in Vercel.

Option B — Deploy backend to Render or Railway:
- These platforms host full containers with Postgres and Redis support and may be easier to manage for Python services in some teams.

Option C — Deploy backend as serverless (Vercel Functions) — NOT recommended:
- The backend depends on long-lived DB connections, SSE streaming, and heavy Python libs. Vercel serverless functions (or Edge Functions) are limited and not ideal for this workload.

## 6) Database & Redis

- For production, use a managed Postgres (with `pgvector`) and a managed Redis service. You can provision Postgres on Fly and keep the backend there, or use a managed provider and connect the backend.

## 7) Example Vercel environment variable values

- `NEXT_PUBLIC_API_URL=https://financial-advisor-backend.fly.dev`

## 8) CI / Git integration

- Every push to your configured branches will trigger a Vercel build and deployment. For PR previews, Vercel creates preview deployments automatically.

## 9) DNS and custom domains

- Use Vercel’s domain management to add custom domains for the frontend. Update `FRONTEND_URL` in the backend secrets if you change the domain.

## 10) Useful tips

- If you keep backend on Fly and frontend on Vercel, enable CORS in `backend/app/config.py` by allowing the Vercel domain in `ALLOWED_ORIGINS`.
- For local testing, use `vercel dev` (if you install Vercel CLI) or run `npm run dev` locally.

## Example quick flow (frontend on Vercel, backend on Fly):

1. Deploy backend to Fly following `DEPLOY_FLY.md`.
2. In Vercel project settings, set `NEXT_PUBLIC_API_URL=https://financial-advisor-backend.fly.dev`.
3. Import repo to Vercel and set `frontend` as root.
4. Trigger a deploy on Vercel.

If you'd like, I can create a Vercel-specific `.vercelignore` or add a `vercel.json` with any custom routing you need. I can also generate a short PowerShell script to set Vercel environment variables using the Vercel CLI.
