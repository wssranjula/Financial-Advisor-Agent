# Financial Advisor AI Agent - Complete Setup Guide

This guide provides step-by-step instructions for setting up the Financial Advisor AI Agent, including all manual tasks such as creating OAuth applications, configuring databases, and deploying to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Google Cloud Console Setup (Gmail + Calendar)](#google-cloud-console-setup)
3. [HubSpot Developer Account Setup](#hubspot-developer-account-setup)
4. [Database Setup](#database-setup)
5. [Backend Configuration](#backend-configuration)
6. [Frontend Configuration](#frontend-configuration)
7. [Running Locally](#running-locally)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Node.js** 18+ installed
- **Python** 3.11+ installed
- **PostgreSQL** 15+ with pgvector extension
- **Git** installed
- **Google account** for Google Cloud Console
- **HubSpot account** (free tier available)
- **Anthropic API key** (for Claude)
- **OpenAI API key** (for embeddings)

---

## Google Cloud Console Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click **"New Project"**
4. Enter project name: `Financial Advisor Agent`
5. Click **"Create"**
6. Wait for the project to be created, then select it

### Step 2: Enable Required APIs

1. In the left sidebar, go to **"APIs & Services" > "Library"**
2. Search for and enable the following APIs:
   - **Gmail API** - Click "Enable"
   - **Google Calendar API** - Click "Enable"
   - **Google People API** (optional, for contacts) - Click "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services" > "Credentials"**
2. Click **"+ CREATE CREDENTIALS"** > **"OAuth client ID"**
3. If prompted, configure the OAuth consent screen first (see Step 4)
4. For Application type, select **"Web application"**
5. Name: `Financial Advisor Agent Web Client`
6. **Authorized JavaScript origins**:
   - For local dev: `http://localhost:3000`
   - For production: `https://yourdomain.com`
7. **Authorized redirect URIs**:
   - For local dev: `http://localhost:8000/api/auth/google/callback`
   - For production: `https://yourdomain.com/api/auth/google/callback`
8. Click **"Create"**
9. **IMPORTANT**: Copy and save:
   - **Client ID**
   - **Client Secret**
   (You'll need these for your `.env` file)

### Step 4: Configure OAuth Consent Screen

1. Go to **"APIs & Services" > "OAuth consent screen"**
2. Select **"External"** user type (or "Internal" if using Google Workspace)
3. Click **"Create"**
4. Fill in the required fields:
   - **App name**: `Financial Advisor Agent`
   - **User support email**: Your email
   - **Developer contact information**: Your email
5. Click **"Save and Continue"**

### Step 5: Add Scopes

1. Click **"Add or Remove Scopes"**
2. Add the following scopes:
   ```
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/gmail.send
   https://www.googleapis.com/auth/gmail.modify
   https://www.googleapis.com/auth/calendar.events
   https://www.googleapis.com/auth/calendar.readonly
   https://www.googleapis.com/auth/userinfo.email
   https://www.googleapis.com/auth/userinfo.profile
   ```
3. Click **"Update"**
4. Click **"Save and Continue"**

### Step 6: Add Test Users

1. In the "Test users" section, click **"+ ADD USERS"**
2. Add: `webshookeng@gmail.com` (as specified in requirements)
3. Add your own email for testing
4. Click **"Save and Continue"**
5. Review and click **"Back to Dashboard"**

### Step 7: Publish App (Optional)

For production use:
1. In OAuth consent screen, click **"Publish App"**
2. Submit for verification (required for more than 100 users)
3. This process can take days/weeks for Google to review

---

## HubSpot Developer Account Setup

### Step 1: Create HubSpot Account

1. Go to [HubSpot](https://www.hubspot.com/)
2. Sign up for a **free account** if you don't have one
3. Complete the onboarding process

### Step 2: Create a Developer Account

1. Go to [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Click **"Get started"** or **"Sign in"** with your HubSpot account
3. Accept the developer terms

### Step 3: Create a Public App

1. In the developer portal, go to **"Apps"** in the top navigation
2. Click **"Create app"**
3. **App info**:
   - **App name**: `Financial Advisor Agent`
   - **Description**: `AI-powered assistant for financial advisors`
   - **Logo**: Upload a logo (optional)
4. Click **"Create app"**

### Step 4: Configure Auth Settings

1. Go to the **"Auth"** tab in your app
2. **Redirect URLs**:
   - For local dev: `http://localhost:8000/api/auth/hubspot/callback`
   - For production: `https://yourdomain.com/api/auth/hubspot/callback`
3. Click **"Save"**

### Step 5: Select Scopes

1. In the **"Auth"** tab, scroll to **"Scopes"**
2. Select the following scopes:
   - `crm.objects.contacts.read` - Read contacts
   - `crm.objects.contacts.write` - Create/update contacts
   - `crm.schemas.contacts.read` - Read contact properties
   - `crm.objects.companies.read` - Read companies (optional)
   - `crm.objects.deals.read` - Read deals (optional)
   - `timeline` - Create timeline events (for notes)
3. Click **"Save"**

### Step 6: Get Credentials

1. Go to the **"Auth"** tab
2. **IMPORTANT**: Copy and save:
   - **App ID**
   - **Client ID**
   - **Client Secret**
   (You'll need these for your `.env` file)

### Step 7: Install App to Your Account (Testing)

1. Go to the **"Install URL (OAuth)"** section
2. Copy the install URL
3. Open it in a browser
4. Select your HubSpot account
5. Click **"Connect app"**
6. You'll be redirected with an authorization code

---

## Database Setup

### Option 1: Local PostgreSQL Installation

#### On macOS (using Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Install pgvector extension
brew install pgvector

# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE financial_advisor;
CREATE USER fa_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE financial_advisor TO fa_user;

# Connect to the new database
\c financial_advisor

# Enable pgvector extension
CREATE EXTENSION vector;

# Grant permissions
GRANT ALL ON SCHEMA public TO fa_user;

# Exit
\q
```

#### On Windows

1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Open **pgAdmin** (installed with PostgreSQL)
5. Create a new database:
   - Right-click **"Databases"** > **"Create" > "Database..."**
   - Name: `financial_advisor`
   - Owner: `postgres`
6. Install pgvector:
   ```powershell
   # Download pgvector from releases
   # https://github.com/pgvector/pgvector/releases
   # Follow Windows installation instructions in the README
   ```
7. Open SQL Query Tool and run:
   ```sql
   CREATE EXTENSION vector;
   ```

#### On Linux (Ubuntu/Debian)

```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Install build tools for pgvector
sudo apt install build-essential postgresql-server-dev-15

# Install pgvector
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql

CREATE DATABASE financial_advisor;
CREATE USER fa_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE financial_advisor TO fa_user;
\c financial_advisor
CREATE EXTENSION vector;
GRANT ALL ON SCHEMA public TO fa_user;
\q
```

### Option 2: Cloud PostgreSQL (Recommended for Production)

#### Using Neon (Serverless Postgres with pgvector)

1. Go to [Neon](https://neon.tech/)
2. Sign up for a free account
3. Click **"Create a project"**
4. Project name: `financial-advisor-agent`
5. Select a region close to your users
6. Click **"Create project"**
7. Copy the connection string
8. In the Neon console, run:
   ```sql
   CREATE EXTENSION vector;
   ```

#### Using Supabase

1. Go to [Supabase](https://supabase.com/)
2. Sign up and create a new project
3. Copy the database connection string
4. In SQL Editor, run:
   ```sql
   CREATE EXTENSION vector;
   ```

#### Using AWS RDS

1. Go to AWS RDS Console
2. Create a new PostgreSQL 15 database
3. Enable pgvector extension:
   ```sql
   CREATE EXTENSION vector;
   ```

### Step 3: Run Database Migrations

```bash
# From the backend directory
cd backend

# Install alembic if not already installed
pip install alembic

# Initialize alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Run migrations
alembic upgrade head
```

### Step 4: Verify Database Setup

```bash
# Connect to database
psql -h localhost -U fa_user -d financial_advisor

# List tables
\dt

# Verify pgvector extension
SELECT * FROM pg_extension WHERE extname = 'vector';

# Exit
\q
```

---

## Backend Configuration

### Step 1: Clone/Create Project

```bash
# Navigate to your projects directory
cd ~/projects  # or C:\Users\YourName\projects on Windows

# Create directory
mkdir financial-advisor-agent
cd financial-advisor-agent

# Create backend directory
mkdir backend
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pgvector==0.2.4
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6

# DeepAgents & LangChain
deepagents==0.1.0
langchain==0.1.0
langchain-anthropic==0.1.0
langchain-openai==0.0.5
langgraph==0.0.20

# Google APIs
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.115.0

# HubSpot
hubspot-api-client==9.0.0

# Async & Task Queue
asyncpg==0.29.0
apscheduler==3.10.4
celery==5.3.4
redis==5.0.1

# Security
cryptography==42.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Utilities
httpx==0.26.0
python-dateutil==2.8.2
EOF

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Create Environment File

```bash
# Create .env file
cat > .env << EOF
# Application
APP_NAME=Financial Advisor Agent
APP_ENV=development
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database
DATABASE_URL=postgresql://fa_user:your_secure_password@localhost:5432/financial_advisor

# Redis (for caching and Celery)
REDIS_URL=redis://localhost:6379/0

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# HubSpot OAuth
HUBSPOT_CLIENT_ID=your-hubspot-client-id
HUBSPOT_CLIENT_SECRET=your-hubspot-client-secret
HUBSPOT_REDIRECT_URI=http://localhost:8000/api/auth/hubspot/callback

# Anthropic (Claude)
ANTHROPIC_API_KEY=your-anthropic-api-key

# OpenAI (Embeddings)
OPENAI_API_KEY=your-openai-api-key

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Encryption
ENCRYPTION_KEY=your-32-byte-encryption-key-change-this

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
```

### Step 5: Generate Secret Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Replace the placeholder values in .env with generated keys
```

### Step 6: Create Database Models

See the `MVP_PLAN.md` for complete database model definitions.

---

## Frontend Configuration

### Step 1: Create Next.js Project

```bash
# Navigate to project root
cd ~/projects/financial-advisor-agent

# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app --src-dir=false --import-alias="@/*"

# Navigate to frontend
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install @tanstack/react-query axios
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install eventsource-parser
npm install date-fns
```

### Step 3: Create Environment File

```bash
# Create .env.local
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Financial Advisor Agent
EOF
```

### Step 4: Configure Tailwind

```javascript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}

export default config
```

---

## Running Locally

### Step 1: Start Database Services

```bash
# Start PostgreSQL (if not already running)
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Linux

# Start Redis
brew services start redis  # macOS
sudo systemctl start redis # Linux
```

### Step 2: Start Backend

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Run migrations (first time only)
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Step 3: Start Frontend

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Start Next.js dev server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Step 4: Start Background Workers (Optional)

```bash
# In another terminal, start Celery worker
cd backend
source venv/bin/activate
celery -A app.workers.celery_tasks worker --loglevel=info

# In another terminal, start Celery beat (for scheduled tasks)
celery -A app.workers.celery_tasks beat --loglevel=info
```

### Step 5: Initial Setup

1. Open browser to `http://localhost:3000`
2. Click **"Login with Google"**
3. Authorize the application
4. Click **"Connect HubSpot"**
5. Authorize HubSpot
6. Click **"Sync Data"** to trigger initial data import
7. Wait for emails and HubSpot data to be embedded (check backend logs)

---

## Deployment

### Option 1: Docker Deployment

#### Step 1: Create Dockerfiles

**Backend Dockerfile:**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend Dockerfile:**
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

CMD ["npm", "start"]
```

#### Step 2: Create docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: financial_advisor
      POSTGRES_USER: fa_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    env_file: .env
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    env_file: frontend/.env.production
    depends_on:
      - backend
    ports:
      - "3000:3000"

  celery_worker:
    build: ./backend
    command: celery -A app.workers.celery_tasks worker --loglevel=info
    env_file: .env
    depends_on:
      - postgres
      - redis

  celery_beat:
    build: ./backend
    command: celery -A app.workers.celery_tasks beat --loglevel=info
    env_file: .env
    depends_on:
      - redis

volumes:
  postgres_data:
  redis_data:
```

#### Step 3: Deploy with Docker Compose

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Deploy to Vercel (Frontend) + Railway (Backend)

#### Frontend to Vercel

1. Push code to GitHub
2. Go to [Vercel](https://vercel.com/)
3. Click **"Import Project"**
4. Select your GitHub repository
5. Configure:
   - Framework: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
6. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
7. Click **"Deploy"**

#### Backend to Railway

1. Go to [Railway](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your repository
5. Add PostgreSQL database:
   - Click **"+ New"** > **"Database"** > **"PostgreSQL"**
   - Copy `DATABASE_URL` from variables
6. Configure backend service:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add all environment variables from your `.env`
8. Deploy

### Option 3: Deploy to AWS

#### Using AWS Elastic Beanstalk

1. Install EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize EB:
   ```bash
   cd backend
   eb init -p python-3.11 financial-advisor-backend
   ```

3. Create environment:
   ```bash
   eb create financial-advisor-prod
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

#### Using AWS ECS (More scalable)

See AWS ECS documentation for detailed setup.

### Option 4: Deploy to Google Cloud Platform

#### Using Cloud Run

1. Build and push Docker image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/financial-advisor-backend
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy financial-advisor-backend \
     --image gcr.io/YOUR_PROJECT_ID/financial-advisor-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## Post-Deployment Setup

### 1. Update OAuth Redirect URIs

After deploying, update your OAuth applications with production URLs:

**Google Cloud Console:**
1. Go to Credentials
2. Edit your OAuth 2.0 Client ID
3. Add production redirect URI: `https://yourdomain.com/api/auth/google/callback`
4. Save

**HubSpot:**
1. Go to your app in developer portal
2. Add production redirect URI: `https://yourdomain.com/api/auth/hubspot/callback`
3. Save

### 2. Configure Domain & SSL

- Set up your domain to point to your deployment
- Enable SSL/TLS (most platforms do this automatically)
- Update CORS settings in backend to allow your domain

### 3. Set up Monitoring

```bash
# Install monitoring tools
pip install sentry-sdk datadog

# Configure in app/main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

### 4. Database Backups

Set up automated backups:
- **Neon**: Automatic backups included
- **AWS RDS**: Enable automated backups in console
- **Railway**: Automatic backups included
- **Self-hosted**: Set up pg_dump cron job

---

## Troubleshooting

### Common Issues

#### 1. OAuth Redirect URI Mismatch

**Error**: `redirect_uri_mismatch`

**Solution**:
- Verify redirect URIs in Google Cloud Console and HubSpot match exactly
- Check for http vs https
- Check for trailing slashes

#### 2. Database Connection Errors

**Error**: `could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
pg_isready

# Check connection string
psql $DATABASE_URL

# Verify pgvector extension
psql -c "SELECT * FROM pg_extension WHERE extname = 'vector';" $DATABASE_URL
```

#### 3. Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'deepagents'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. CORS Errors

**Error**: `Access-Control-Allow-Origin` errors

**Solution**:
```python
# In backend/app/main.py, add:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5. Gmail API Quota Exceeded

**Error**: `User Rate Limit Exceeded`

**Solution**:
- Implement exponential backoff
- Use batch requests where possible
- Request quota increase in Google Cloud Console

### Getting Help

- **DeepAgents Issues**: [GitHub Issues](https://github.com/deepagents/deepagents/issues)
- **LangChain Docs**: [docs.langchain.com](https://docs.langchain.com/)
- **Google API Support**: [Google Cloud Support](https://cloud.google.com/support)
- **HubSpot Developer Forums**: [developers.hubspot.com](https://developers.hubspot.com/)

---

## Next Steps

After successful setup:

1. ✅ Test OAuth flows with Google and HubSpot
2. ✅ Trigger initial data sync
3. ✅ Test RAG queries in chat interface
4. ✅ Test multi-step task execution
5. ✅ Add ongoing instructions
6. ✅ Monitor logs for errors
7. ✅ Set up monitoring and alerts
8. ✅ Configure backups
9. ✅ Optimize performance based on usage

Congratulations! Your Financial Advisor AI Agent is now set up and ready to use.
