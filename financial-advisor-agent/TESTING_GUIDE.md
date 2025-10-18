# Testing Guide - Financial Advisor AI Agent

This guide walks you through setting up, running, and testing the Financial Advisor AI Agent MVP.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [OAuth Configuration](#oauth-configuration)
7. [Running the Application](#running-the-application)
8. [Testing Workflows](#testing-workflows)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.10+**
   ```bash
   python --version
   # Should show Python 3.10 or higher
   ```

2. **Node.js 18+**
   ```bash
   node --version
   # Should show v18.0.0 or higher
   ```

3. **PostgreSQL 14+** with pgvector extension
   ```bash
   psql --version
   # Should show PostgreSQL 14 or higher
   ```

4. **Git**
   ```bash
   git --version
   ```

### API Keys Needed

- **OpenAI API Key** (for embeddings and LLM)
- **Google OAuth Credentials** (for Gmail and Calendar)
- **HubSpot OAuth Credentials** (for CRM)

---

## Environment Setup

### 1. Clone and Navigate to Project

```bash
cd C:\Users\Admin\Desktop\Suresh\deepagents\financial-advisor-agent
```

### 2. Backend Environment Variables

Create `backend/.env` file:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/financial_advisor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=financial_advisor

# JWT Secret (generate a random string)
SECRET_KEY=your-secret-key-here-change-this-to-something-random

# Encryption Key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
ENCRYPTION_KEY=your-fernet-encryption-key-here

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# HubSpot OAuth
HUBSPOT_CLIENT_ID=your-hubspot-client-id
HUBSPOT_CLIENT_SECRET=your-hubspot-client-secret
HUBSPOT_REDIRECT_URI=http://localhost:8000/api/auth/hubspot/callback

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Environment
ENVIRONMENT=development
```

### 3. Frontend Environment Variables

Create `frontend/.env.local`:

```bash
cd ../frontend
cp .env.local.example .env.local
```

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Database Setup

### 1. Install PostgreSQL with pgvector

**On Windows (using PostgreSQL installer):**

1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install PostgreSQL
3. Install pgvector extension:

```bash
# Open pgAdmin or psql
CREATE EXTENSION vector;
```

**On macOS (using Homebrew):**

```bash
brew install postgresql@14
brew install pgvector

# Start PostgreSQL
brew services start postgresql@14

# Create database
createdb financial_advisor
```

**On Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install postgresql-14-pgvector

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE financial_advisor;

# Connect to the database
\c financial_advisor

# Install pgvector extension
CREATE EXTENSION vector;

# Exit
\q
```

### 3. Run Database Migrations

```bash
cd backend

# Install Python dependencies first (see Backend Setup below)

# Run migrations
alembic upgrade head
```

---

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install fastapi uvicorn sqlalchemy asyncpg alembic
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
pip install httpx requests
pip install openai
pip install langchain langchain-openai langgraph langsmith
pip install pgvector psycopg2-binary
pip install python-dotenv
pip install cryptography
```

### 3. Generate Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and add it to your `.env` file as `ENCRYPTION_KEY`.

### 4. Test Backend Connection

```bash
# Make sure virtual environment is activated
python -c "from app.config import settings; print('Config loaded:', settings.DATABASE_URL)"
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

If you encounter issues, try:

```bash
npm install --legacy-peer-deps
```

### 2. Verify Installation

```bash
npm run dev --help
```

---

## OAuth Configuration

### Google OAuth Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create a Project** (or select existing):
   - Click "Select a project" → "New Project"
   - Name: "Financial Advisor AI"
   - Click "Create"

3. **Enable APIs**:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search and enable:
     - Gmail API
     - Google Calendar API
     - Google People API

4. **Configure OAuth Consent Screen**:
   - Go to "APIs & Services" → "OAuth consent screen"
   - User Type: External
   - App name: "Financial Advisor AI Agent"
   - User support email: your email
   - Developer contact: your email
   - Scopes: Add these scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.send`
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/calendar.events`
   - Test users: Add your Gmail address

5. **Create Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: Web application
   - Name: "Financial Advisor Backend"
   - Authorized redirect URIs:
     - `http://localhost:8000/api/auth/google/callback`
   - Click "Create"
   - Copy Client ID and Client Secret to your `.env` file

### HubSpot OAuth Setup

1. **Create HubSpot Developer Account**: https://developers.hubspot.com/

2. **Create an App**:
   - Go to "Apps" → "Create app"
   - App name: "Financial Advisor AI Agent"
   - Description: "AI-powered assistant for financial advisors"

3. **Configure OAuth**:
   - Go to "Auth" tab
   - Redirect URL: `http://localhost:8000/api/auth/hubspot/callback`
   - Scopes needed:
     - `crm.objects.contacts.read`
     - `crm.objects.contacts.write`
     - `crm.schemas.contacts.read`
     - `crm.objects.companies.read`

4. **Get Credentials**:
   - Copy "Client ID" and "Client Secret"
   - Add to your `.env` file

---

## Running the Application

### Terminal 1: Start Database

Make sure PostgreSQL is running:

```bash
# On Windows (if installed as service, it should auto-start)
# Check in Services app

# On macOS:
brew services start postgresql@14

# On Linux:
sudo systemctl start postgresql
```

### Terminal 2: Start Backend

```bash
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run migrations (first time only)
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test backend is running**:
- Open browser: http://localhost:8000
- You should see: `{"status": "ok", "service": "Financial Advisor AI Agent API", "version": "0.1.0"}`
- API docs: http://localhost:8000/docs

### Terminal 3: Start Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Test frontend is running**:
- Open browser: http://localhost:3000
- You should see the chat interface

---

## Testing Workflows

### Test 1: Basic Backend Health Check

1. **Backend API**:
   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:
   ```json
   {"status": "healthy"}
   ```

2. **API Documentation**:
   - Open: http://localhost:8000/docs
   - You should see FastAPI Swagger UI with all endpoints

### Test 2: Google OAuth Flow

1. **Start OAuth Flow**:
   ```bash
   curl http://localhost:8000/api/auth/google/url
   ```

   Expected response:
   ```json
   {
     "url": "https://accounts.google.com/o/oauth2/v2/auth?..."
   }
   ```

2. **Complete OAuth in Browser**:
   - Copy the URL from the response
   - Paste it in your browser
   - Sign in with your Google account
   - Grant permissions
   - You'll be redirected to callback URL with a code
   - Backend will exchange code for tokens and create user

3. **Verify User Created**:
   - Check database:
   ```bash
   psql -U postgres -d financial_advisor -c "SELECT id, email FROM users;"
   ```

### Test 3: HubSpot OAuth Flow

1. **Start OAuth Flow**:
   ```bash
   curl http://localhost:8000/api/auth/hubspot/url
   ```

2. **Complete OAuth** (same process as Google)

### Test 4: Data Sync (After OAuth)

**Note**: You need to be authenticated. Get your user ID from the database first.

1. **Initial Sync** (via API docs):
   - Go to: http://localhost:8000/docs
   - Find `/api/sync/initial` endpoint
   - Click "Try it out"
   - Enter request body:
   ```json
   {
     "sync_gmail": true,
     "sync_hubspot": true,
     "max_emails": 50
   }
   ```
   - Click "Execute"

2. **Check Sync Status**:
   ```bash
   curl http://localhost:8000/api/sync/status
   ```

3. **Verify Data in Database**:
   ```bash
   psql -U postgres -d financial_advisor

   # Check embeddings
   SELECT COUNT(*) FROM document_embeddings;

   # Check by source type
   SELECT source_type, COUNT(*) FROM document_embeddings GROUP BY source_type;
   ```

### Test 5: Frontend Chat Interface

1. **Open Chat Interface**:
   - Navigate to: http://localhost:3000
   - You should see the chat interface with header and input area

2. **Test Message Input**:
   - Type a message in the input box
   - Press Enter or click Send button
   - You should see your message appear

3. **Test Agent Response** (requires authentication):
   - The agent should respond with streaming
   - You'll see typing indicator
   - Response should appear word by word

### Test 6: RAG Search

Once you have data synced, test RAG search:

1. **Via API**:
   ```bash
   curl -X POST http://localhost:8000/api/chat/message \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Search my emails for anything about baseball",
       "stream": false
     }'
   ```

2. **Via Chat Interface**:
   - Type: "Search my emails for anything about baseball"
   - Send the message
   - Agent should use `rag_search` tool and return relevant results

### Test 7: Tool Execution

Test different agent capabilities:

1. **Gmail Tool**:
   - Message: "Show me my recent emails"
   - Should use `search_emails` tool

2. **Calendar Tool**:
   - Message: "What's on my calendar today?"
   - Should use `get_calendar_events` tool

3. **HubSpot Tool**:
   - Message: "Show me my recent contacts"
   - Should use `search_contacts` tool

4. **Multi-tool Request**:
   - Message: "Find emails from John and check if I have any meetings with him"
   - Should use multiple tools

### Test 8: Streaming Chat

1. **Open Browser Dev Tools**:
   - Press F12
   - Go to Network tab
   - Filter: "Fetch/XHR"

2. **Send a Message**:
   - Type: "Tell me about my recent emails"
   - Click Send

3. **Observe Streaming**:
   - You should see a request to `/api/chat/stream`
   - Response type should be `text/event-stream`
   - Messages should appear incrementally in the UI

4. **Check Events in Console**:
   - You should see SSE events:
     - `message` - User message echo
     - `typing` - Agent is processing
     - `chunk` - Response chunks
     - `tool` - Tool call notifications
     - `tool_result` - Tool execution results
     - `done` - Response complete

### Test 9: Rich Message Components

1. **Test Calendar Event Card**:
   - Message: "Show me my calendar events for tomorrow"
   - Agent should return calendar events
   - You should see rich calendar cards with:
     - Event title
     - Date/time
     - Location
     - Attendees

2. **Test Contact Card**:
   - Message: "Show me contact details for John Smith"
   - Agent should return contact information
   - You should see rich contact cards with:
     - Name and avatar
     - Email and phone
     - Company and title

### Test 10: Error Handling

1. **Test Invalid Message**:
   - Send an empty message
   - Should show validation error

2. **Test Network Error**:
   - Stop the backend server
   - Try sending a message
   - Should show connection error

3. **Test OAuth Expiration**:
   - Wait for token to expire (or manually expire in DB)
   - Try using a tool
   - Should prompt for re-authentication

---

## Common Testing Scenarios

### Scenario 1: Email Search

```
User: "Find emails from last week about the Johnson account"

Expected Flow:
1. Agent uses rag_search tool
2. Searches embeddings for "Johnson account"
3. Filters by date (last week)
4. Returns relevant emails
5. Displays results in chat
```

### Scenario 2: Meeting Scheduling

```
User: "Schedule a meeting with Sarah tomorrow at 2pm"

Expected Flow:
1. Agent uses get_calendar_events to check availability
2. Agent uses create_calendar_event to schedule
3. Returns calendar event card
4. Shows meeting details in rich component
```

### Scenario 3: Contact Lookup

```
User: "Tell me about my contact Michael Chen"

Expected Flow:
1. Agent uses search_contacts tool
2. Finds Michael Chen in HubSpot
3. Agent uses get_contact_notes for additional context
4. Returns contact card with all details
5. Shows notes and last contacted date
```

---

## Troubleshooting

### Backend Issues

**1. Database Connection Error**

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**:
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env`
- Check database exists: `psql -U postgres -l`

**2. pgvector Extension Missing**

```
UndefinedObject: type "vector" does not exist
```

**Solution**:
```bash
psql -U postgres -d financial_advisor -c "CREATE EXTENSION vector;"
```

**3. Import Errors**

```
ModuleNotFoundError: No module named 'app'
```

**Solution**:
- Make sure you're in the `backend` directory
- Virtual environment is activated
- Dependencies installed: `pip install -r requirements.txt`

**4. OpenAI API Error**

```
openai.error.AuthenticationError: Invalid API key
```

**Solution**:
- Check `OPENAI_API_KEY` in `.env`
- Verify key is valid at https://platform.openai.com/api-keys

### Frontend Issues

**1. Cannot Connect to Backend**

```
Error: Network request failed
```

**Solution**:
- Check backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

**2. Module Not Found**

```
Module not found: Can't resolve '@/components/ChatInterface'
```

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**3. TypeScript Errors**

```
Type error: Property 'message' does not exist
```

**Solution**:
- Check type definitions in `lib/types.ts`
- Restart TypeScript server in VS Code
- Run: `npm run build` to see all errors

### OAuth Issues

**1. Redirect URI Mismatch**

```
Error: redirect_uri_mismatch
```

**Solution**:
- Check redirect URI in Google Cloud Console matches exactly:
  `http://localhost:8000/api/auth/google/callback`
- No trailing slashes
- Same for HubSpot

**2. Invalid Scope**

```
Error: invalid_scope
```

**Solution**:
- Verify scopes in OAuth consent screen
- Make sure all required scopes are added
- Re-authenticate after adding new scopes

**3. Token Expired**

```
Error: invalid_grant
```

**Solution**:
- Delete user tokens from database
- Re-authenticate through OAuth flow

### RAG/Embedding Issues

**1. No Search Results**

**Solution**:
- Check data has been synced: `SELECT COUNT(*) FROM document_embeddings;`
- Run initial sync again
- Verify OpenAI embeddings are being created

**2. Embedding Dimension Error**

```
Error: dimension mismatch
```

**Solution**:
- Drop and recreate embeddings table
- Re-run migrations
- Re-sync data

### Chat/Streaming Issues

**1. Messages Not Streaming**

**Solution**:
- Check browser dev tools for SSE connection
- Verify `/api/chat/stream` endpoint is working
- Check for CORS errors
- Try with streaming disabled first

**2. Tool Calls Not Showing**

**Solution**:
- Check agent has access to tools
- Verify tool metadata in response
- Check MessageBubble component is rendering tool_calls

---

## Performance Testing

### Load Testing

1. **Test Multiple Concurrent Users**:
   ```bash
   # Install Apache Bench
   # Windows: Download from https://www.apachelounge.com/
   # macOS: brew install httpd
   # Linux: sudo apt-get install apache2-utils

   # Test endpoint
   ab -n 100 -c 10 http://localhost:8000/health
   ```

2. **Test RAG Search Performance**:
   - Sync 1000+ emails
   - Time search queries
   - Should return results in < 2 seconds

3. **Test Embedding Generation**:
   - Time initial sync
   - Monitor OpenAI API rate limits

### Memory Testing

1. **Monitor Backend Memory**:
   ```bash
   # While backend is running
   ps aux | grep uvicorn
   ```

2. **Monitor Database Size**:
   ```bash
   psql -U postgres -d financial_advisor -c "SELECT pg_size_pretty(pg_database_size('financial_advisor'));"
   ```

---

## Next Steps After Testing

Once basic testing is complete:

1. **Implement Phase 5**: Task Persistence & Memory
2. **Add Error Logging**: Integrate Sentry or similar
3. **Add Monitoring**: Track API usage, response times
4. **Security Audit**: Review authentication, authorization
5. **User Acceptance Testing**: Get feedback from real users
6. **Performance Optimization**: Based on test results
7. **Deployment**: Prepare for production deployment

---

## Useful Commands Reference

### Database

```bash
# Connect to database
psql -U postgres -d financial_advisor

# List tables
\dt

# Describe table
\d users
\d document_embeddings

# Count records
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM document_embeddings;

# View recent embeddings
SELECT id, source_type, created_at FROM document_embeddings ORDER BY created_at DESC LIMIT 10;

# Clear all data (careful!)
TRUNCATE users CASCADE;
TRUNCATE document_embeddings CASCADE;
```

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run with auto-reload
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --reload --port 8001

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test imports
python -c "from app.main import app; print('OK')"
```

### Frontend

```bash
# Development server
npm run dev

# Production build
npm run build
npm run start

# Type checking
npm run type-check

# Linting
npm run lint
```

### Git

```bash
# Check current branch
git branch

# View recent commits
git log --oneline -10

# Check status
git status

# Pull latest changes
git pull origin feature/dev
```

---

## Support and Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **LangChain Docs**: https://python.langchain.com/
- **pgvector Docs**: https://github.com/pgvector/pgvector
- **OpenAI API**: https://platform.openai.com/docs

---

## Quick Start Checklist

- [ ] PostgreSQL installed and running
- [ ] Database created with pgvector extension
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Backend `.env` file configured
- [ ] Frontend `.env.local` file configured
- [ ] Google OAuth credentials configured
- [ ] HubSpot OAuth credentials configured
- [ ] OpenAI API key configured
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Database migrations run
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] OAuth flow tested
- [ ] Data sync tested
- [ ] Chat interface tested
- [ ] RAG search tested

Happy Testing! 🚀
