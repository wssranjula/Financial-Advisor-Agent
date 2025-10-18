# Financial Advisor AI Agent MVP

AI-powered assistant for financial advisors built with DeepAgents, LangChain, FastAPI, and Next.js.

## 🎯 Overview

The Financial Advisor AI Agent helps financial advisors manage their daily tasks by integrating with Gmail, Google Calendar, and HubSpot CRM. It uses RAG (Retrieval-Augmented Generation) to search through historical data and provide intelligent assistance through a conversational chat interface.

## ✨ Key Features

- **🤖 Multi-Agent System**: 16 tools and 3 specialized subagents
- **📧 Gmail Integration**: Search, read, send, and reply to emails
- **📅 Calendar Management**: View, schedule, and manage meetings
- **👥 CRM Integration**: HubSpot contact and note management
- **🔍 RAG Search**: Semantic search with pgvector embeddings
- **💬 Real-time Chat**: SSE streaming with rich message components
- **🎨 Modern UI**: Next.js 14 with Tailwind CSS and dark mode

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ with pgvector
- OpenAI API key

### Automated Setup

**1. Setup Database (Windows):**
```bash
setup-database.bat
```

**macOS/Linux:**
```bash
chmod +x setup-database.sh && ./setup-database.sh
```

**2. Start Backend (Windows):**
```bash
start-backend.bat
```

**macOS/Linux:**
```bash
chmod +x start-backend.sh && ./start-backend.sh
```

**3. Start Frontend (Windows):**
```bash
start-frontend.bat
```

**macOS/Linux:**
```bash
chmod +x start-frontend.sh && ./start-frontend.sh
```

**4. Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

See **[QUICK_START.md](QUICK_START.md)** for detailed setup instructions.

## 📚 Documentation

### Local Development
- **[QUICK_START.md](QUICK_START.md)** - Get running in 10 minutes
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing guide
- **[CLAUDE.md](CLAUDE.md)** - Development documentation

### Deployment
- **[QUICK_START_DEPLOYMENT.md](QUICK_START_DEPLOYMENT.md)** - Deploy to production in 3 steps ⭐ START HERE
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Verify your deployment
- **[DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md)** - Complete deployment guide
- **[DEPLOYMENT_FIXES_SUMMARY.md](DEPLOYMENT_FIXES_SUMMARY.md)** - Technical details of deployment fixes

## 🏗️ Architecture

- **Backend**: FastAPI + LangChain + pgvector
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL with pgvector extension
- **AI**: OpenAI GPT-4 + text-embedding-3-small
- **Integrations**: Google (Gmail, Calendar) + HubSpot

## 📖 Full Documentation

For complete information, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

Built with ❤️ using DeepAgents, LangChain, and Next.js
