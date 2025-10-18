# Quick Start Guide

Get the Financial Advisor AI Agent running in under 10 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ with pgvector
- OpenAI API key

## Step 1: Database Setup

### Option A: Automated (Recommended)

**Windows:**
```bash
setup-database.bat
```

**macOS/Linux:**
```bash
chmod +x setup-database.sh
./setup-database.sh
```

### Option B: Manual

```bash
psql -U postgres
CREATE DATABASE financial_advisor;
\c financial_advisor
CREATE EXTENSION vector;
\q
```

## Step 2: Configure Environment

### Backend (.env)

Create `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/financial_advisor
SECRET_KEY=your-secret-key-change-this
ENCRYPTION_KEY=your-fernet-key-here
OPENAI_API_KEY=sk-your-openai-key-here

# Get these after OAuth setup (can skip for now)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
HUBSPOT_CLIENT_ID=your-hubspot-id
HUBSPOT_CLIENT_SECRET=your-hubspot-secret

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

Generate encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Frontend (.env.local)

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 3: Start Backend

### Option A: Automated (Recommended)

**Windows:**
```bash
start-backend.bat
```

**macOS/Linux:**
```bash
chmod +x start-backend.sh
./start-backend.sh
```

### Option B: Manual

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

✅ Backend should be running at: http://localhost:8000

## Step 4: Start Frontend

### Option A: Automated (Recommended)

**Windows:**
```bash
start-frontend.bat
```

**macOS/Linux:**
```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

### Option B: Manual

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend should be running at: http://localhost:3000

## Step 5: Verify Everything Works

1. **Backend Health Check:**
   - Open: http://localhost:8000
   - Should see: `{"status": "ok", ...}`

2. **API Documentation:**
   - Open: http://localhost:8000/docs
   - Should see Swagger UI

3. **Frontend:**
   - Open: http://localhost:3000
   - Should see chat interface

## Step 6: Test Basic Chat (Without OAuth)

Without OAuth configured, you can still test the agent's basic capabilities:

1. Open: http://localhost:3000
2. Type: "Hello, what can you do?"
3. Press Enter

The agent should respond (but won't be able to use Gmail/Calendar/HubSpot tools without OAuth).

## Next Steps

### To Enable Full Functionality:

1. **Setup Google OAuth** (for Gmail and Calendar):
   - Follow: [TESTING_GUIDE.md - Google OAuth Setup](TESTING_GUIDE.md#google-oauth-setup)

2. **Setup HubSpot OAuth** (for CRM):
   - Follow: [TESTING_GUIDE.md - HubSpot OAuth Setup](TESTING_GUIDE.md#hubspot-oauth-setup)

3. **Sync Your Data**:
   ```bash
   # After OAuth, sync your emails and contacts
   curl -X POST http://localhost:8000/api/sync/initial \
     -H "Content-Type: application/json" \
     -d '{"sync_gmail": true, "sync_hubspot": true, "max_emails": 100}'
   ```

4. **Test RAG Search**:
   - Type: "Search my emails for anything about meetings"
   - Agent will use semantic search

### Testing Workflows:

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing scenarios including:
- Email search
- Calendar management
- Contact lookup
- Multi-tool requests
- Streaming responses
- Rich message components

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.10+

# Check virtual environment
which python  # Should point to venv

# Check database connection
psql -U postgres -d financial_advisor -c "SELECT 1;"
```

### Frontend won't start

```bash
# Check Node version
node --version  # Should be v18+

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database connection failed

```bash
# Check PostgreSQL is running
pg_isready

# On macOS:
brew services start postgresql@14

# On Linux:
sudo systemctl start postgresql

# On Windows:
# Check Services app for PostgreSQL service
```

### Can't install dependencies

**Backend:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install wheel
pip install wheel

# Try installing dependencies one by one
pip install fastapi uvicorn sqlalchemy
```

**Frontend:**
```bash
# Use legacy peer deps
npm install --legacy-peer-deps
```

## Directory Structure

```
financial-advisor-agent/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── agents/       # Agent definitions
│   │   ├── integrations/ # OAuth & API clients
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── .env              # Configuration (create this)
│   └── requirements.txt
├── frontend/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── lib/              # Utilities & hooks
│   ├── .env.local        # Configuration (create this)
│   └── package.json
├── TESTING_GUIDE.md      # Detailed testing guide
└── QUICK_START.md        # This file
```

## Useful Commands

### Backend

```bash
# Run tests (when implemented)
pytest

# Check logs
# Watch terminal where backend is running

# Database shell
psql -U postgres -d financial_advisor
```

### Frontend

```bash
# Type check
npm run type-check

# Build for production
npm run build

# Lint
npm run lint
```

### Both

```bash
# Stop all servers
# Press Ctrl+C in each terminal

# Or kill by port (if stuck)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

## Support

For detailed information, see:
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Comprehensive testing guide
- [CLAUDE.md](CLAUDE.md) - Development documentation
- [backend/README.md](backend/README.md) - Backend docs (if exists)
- [frontend/README.md](frontend/README.md) - Frontend docs

## Quick Reference

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:3000 | Chat interface |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health | http://localhost:8000/health | Health check |

Happy coding! 🚀
