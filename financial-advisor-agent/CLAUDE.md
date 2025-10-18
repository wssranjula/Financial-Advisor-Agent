# CLAUDE.md - Development Instructions for AI Assistants

This file contains instructions for AI assistants (like Claude) working on the Financial Advisor AI Agent MVP implementation. It includes the complete TODO list and Git workflow guidelines.

---

## 🎯 CURRENT PROGRESS

**Last Updated**: $(date "+%Y-%m-%d")

### ✅ Completed Phases

**Phase 1: Foundation & OAuth (Days 1-2)** - COMPLETE ✅
- ✅ Project setup and structure
- ✅ Database models with pgvector
- ✅ Google OAuth integration
- ✅ HubSpot OAuth integration
- ✅ OAuth API endpoints
- ✅ Integration client wrappers (Gmail, Calendar, HubSpot)

**Phase 2: Core DeepAgents Integration (Days 3-4)** - COMPLETE ✅
- ✅ Gmail tools (4 tools: search_emails, get_email, send_email, reply_to_email)
- ✅ Calendar tools (4 tools: get_calendar_events, create_calendar_event, get_free_busy, find_available_slots)
- ✅ HubSpot tools (6 tools: search_contacts, get_contact_details, create_contact, create_note, get_contact_notes, get_recent_contacts)
- ✅ Subagent definitions (email_researcher, calendar_scheduler, hubspot_manager)
- ✅ Main Financial Advisor agent with orchestration

**Phase 3: RAG System (Days 5-6)** - COMPLETE ✅
- ✅ OpenAI embedding service (text-embedding-3-small, 1536 dimensions)
- ✅ Gmail email ingestion pipeline with batch processing
- ✅ HubSpot data ingestion (contacts + notes)
- ✅ Vector search with pgvector (semantic similarity)
- ✅ RAG search tools (2 tools: rag_search, get_rag_stats)
- ✅ Sync API endpoints (initial, incremental, status)
- ✅ Main agent updated with RAG capabilities

**Phase 4: Chat Interface (Days 7-8)** - COMPLETE ✅
- ✅ Next.js 14 frontend setup with TypeScript and Tailwind CSS
- ✅ Chat UI components (ChatInterface, MessageList, MessageBubble, InputArea)
- ✅ Streaming chat API with Server-Sent Events (SSE)
- ✅ useChat hook for frontend SSE integration
- ✅ Rich message components (CalendarEventCard, ContactCard)
- ✅ Real-time message streaming with tool call tracking
- ✅ Conversation management API endpoints
- ✅ Full integration with DeepAgents backend

**Total Tools Implemented**: 16 tools
**Total Subagents Implemented**: 3 subagents
**RAG System**: Fully operational with semantic search
**Chat Interface**: Complete with SSE streaming and rich components

### 📋 Next Up: Phase 5 - Task Persistence & Memory (Days 9-10)

**Testing Plan Created**: See [docs/TESTING_PLAN.md](docs/TESTING_PLAN.md)

### 🏗️ Current Architecture

```
Financial Advisor AI Agent
├── Backend (FastAPI)
│   ├── OAuth Integration ✅
│   │   ├── Google (Gmail + Calendar) ✅
│   │   └── HubSpot (CRM) ✅
│   ├── Integration Clients ✅
│   │   ├── GmailClient ✅
│   │   ├── CalendarClient ✅
│   │   └── HubSpotClient ✅
│   ├── RAG System ✅
│   │   ├── Embedding Service (OpenAI) ✅
│   │   ├── Ingestion Service (Gmail + HubSpot) ✅
│   │   ├── Retrieval Service (pgvector) ✅
│   │   └── Sync API (initial + incremental) ✅
│   ├── Agent Tools (16 total) ✅
│   │   ├── Gmail Tools (4) ✅
│   │   ├── Calendar Tools (4) ✅
│   │   ├── HubSpot Tools (6) ✅
│   │   └── RAG Tools (2) ✅
│   ├── Subagents ✅
│   │   ├── Email Researcher ✅
│   │   ├── Calendar Scheduler ✅
│   │   └── HubSpot Manager ✅
│   ├── Main Agent (with RAG) ✅
│   └── Chat API ✅
│       ├── Streaming SSE endpoint ✅
│       ├── Conversation management ✅
│       └── Message persistence ✅
├── Frontend (Next.js 14) ✅
│   ├── Chat UI Components ✅
│   │   ├── ChatInterface ✅
│   │   ├── MessageList ✅
│   │   ├── MessageBubble ✅
│   │   └── InputArea ✅
│   ├── Rich Components ✅
│   │   ├── CalendarEventCard ✅
│   │   └── ContactCard ✅
│   ├── Hooks ✅
│   │   └── useChat (SSE integration) ✅
│   └── Styling ✅
│       ├── Tailwind CSS ✅
│       ├── Dark mode support ✅
│       └── Responsive design ✅
├── Database (PostgreSQL + pgvector) ✅
├── Models (including DocumentEmbedding) ✅
└── Security (Token encryption) ✅
```

### 🎯 System Capabilities

The system now provides comprehensive AI-powered assistance:
1. ✅ OAuth authentication for Google and HubSpot
2. ✅ 16 tools across Gmail, Calendar, HubSpot, and RAG
3. ✅ 3 specialized subagents with domain expertise
4. ✅ Semantic search over all historical data
5. ✅ Data ingestion with automatic embedding
6. ✅ Vector similarity search with pgvector
7. ✅ Main agent orchestration with memory persistence
8. ✅ Real-time chat interface with SSE streaming
9. ✅ Rich message components for events and contacts
10. ✅ Full-stack integration (Next.js + FastAPI)

**Next Step**: Implement Phase 5 (Task Persistence & Memory) or follow the [Testing Plan](docs/TESTING_PLAN.md).

---

## Project Overview

**Project**: Financial Advisor AI Agent
**Framework**: DeepAgents (LangChain + LangGraph)
**MVP Timeline**: 12 days
**Architecture**: FastAPI backend + Next.js frontend + PostgreSQL (pgvector)

**Key Documentation**:
- [MVP Plan](../docs/MVP_PLAN.md) - Detailed implementation roadmap
- [Setup Guide](../docs/SETUP_GUIDE.md) - Manual setup instructions
- [Full Implementation](../docs/FULL_IMPLEMENTATION.md) - Production features
- [MVP TODO](../docs/MVP_TODO.md) - Complete task checklist

---

## Git Workflow & Branch Strategy

### Branch Naming Convention

Use descriptive branch names following this pattern:

```
<type>/<short-description>

Types:
- feature/  : New features or functionality
- fix/      : Bug fixes
- refactor/ : Code refactoring
- docs/     : Documentation updates
- test/     : Adding or updating tests
- chore/    : Maintenance tasks
```

**Examples**:
- `feature/oauth-google-integration`
- `feature/gmail-tools`
- `feature/rag-search-implementation`
- `fix/token-refresh-logic`
- `refactor/database-models`

### Development Workflow

#### 1. Starting a New Feature

```bash
# Always start from the latest master
git checkout master
git pull origin master

# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Example: Starting OAuth integration
git checkout -b feature/oauth-google-integration
```

#### 2. Working on the Feature

```bash
# Make your changes
# ... edit files ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Implement Google OAuth authorization flow

- Add OAuth URL generation
- Implement token exchange
- Add token encryption
- Create callback endpoint"

# Push to remote
git push origin feature/your-feature-name
```

#### 3. Creating a Pull Request

```bash
# Push your branch if not already pushed
git push origin feature/your-feature-name

# Create PR via GitHub CLI (if available)
gh pr create --title "Implement Google OAuth Integration" \
  --body "Implements Phase 1, Day 2 - Google OAuth

## Changes
- OAuth authorization URL generation
- Token exchange logic
- Token encryption service
- Callback endpoint implementation

## Testing
- [x] OAuth flow works end-to-end
- [x] Tokens encrypted and stored
- [x] Test user webshookeng@gmail.com can authenticate

## Related
- Closes #1
- Part of MVP Phase 1"

# Or create PR manually on GitHub
# 1. Go to repository on GitHub
# 2. Click "Pull Requests" > "New Pull Request"
# 3. Select your branch
# 4. Fill in title and description
# 5. Click "Create Pull Request"
```

#### 4. PR Review & Merge

```bash
# After PR is approved, merge to master
# (Do this via GitHub UI with "Squash and merge" or "Merge pull request")

# After merge, update local master
git checkout master
git pull origin master

# Delete the feature branch locally
git branch -d feature/your-feature-name

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/your-feature-name
```

### Commit Message Guidelines

**Format**:
```
<Short summary (50 chars or less)>

<Detailed description if needed>

- Bullet points for changes
- Be specific about what changed
- Reference issues/PRs if applicable
```

**Good Examples**:
```
Add Gmail tools implementation

Implements search_emails, send_email, get_email, and reply_to_email tools
for the DeepAgents framework.

- Add GmailClient wrapper
- Implement 4 core Gmail tools
- Add error handling and retries
- Add comprehensive docstrings

Relates to Phase 2, Day 3 of MVP Plan
```

```
Fix token refresh logic for expired Google tokens

- Check token expiration before API calls
- Automatically refresh when needed
- Update stored token in database
- Add error handling for refresh failures

Fixes #12
```

### Feature Branch Strategy for MVP Phases

Organize your branches by MVP phases:

**Phase 1 (Days 1-2): Foundation & OAuth**
- `feature/project-setup`
- `feature/database-models`
- `feature/oauth-google`
- `feature/oauth-hubspot`
- `feature/integration-clients`

**Phase 2 (Days 3-4): DeepAgents Integration**
- `feature/gmail-tools`
- `feature/calendar-tools`
- `feature/hubspot-tools`
- `feature/subagent-definitions`
- `feature/main-agent`

**Phase 3 (Days 5-6): RAG System**
- `feature/embedding-service`
- `feature/gmail-ingestion`
- `feature/hubspot-ingestion`
- `feature/vector-search`
- `feature/rag-tools`

**Phase 4 (Days 7-8): Chat Interface**
- `feature/nextjs-setup`
- `feature/chat-ui-components`
- `feature/streaming-api`
- `feature/rich-message-components`

**Phase 5 (Days 9-10): Task Persistence**
- `feature/task-manager`
- `feature/instruction-manager`
- `feature/polling-service`

**Phase 6 (Days 11-12): Testing & Polish**
- `test/rag-queries`
- `test/multi-step-tasks`
- `test/ongoing-instructions`
- `fix/error-handling`
- `docs/deployment`

---

## MVP Development TODO List

### Phase 1: Foundation & OAuth (Days 1-2)

#### Day 1: Project Setup & Backend Foundation

**Branch**: `feature/project-setup`

- [ ] Initialize Backend Project
  - [ ] Create `financial-advisor-agent` directory
  - [ ] Create `backend` subdirectory
  - [ ] Create Python virtual environment
  - [ ] Install dependencies
  - [ ] Create `requirements.txt`
- [ ] Create Project Structure (all directories)
- [ ] Commit: "Initialize backend project structure"

**Branch**: `feature/database-models`

- [ ] Database Models Setup
  - [ ] Create `models/user.py`
  - [ ] Create `models/conversation.py`
  - [ ] Create `models/message.py`
  - [ ] Create `models/task.py`
  - [ ] Create `models/instruction.py`
  - [ ] Create `models/document_embedding.py`
  - [ ] Initialize Alembic
  - [ ] Create initial migration
- [ ] Commit: "Add database models with pgvector support"
- [ ] Create PR: "Database Models Implementation"

**Branch**: `feature/configuration`

- [ ] Configuration Management
  - [ ] Create `.env.example`
  - [ ] Implement `config.py`
  - [ ] Create `.gitignore`
- [ ] Commit: "Add configuration management"
- [ ] Create PR: "Configuration and Environment Setup"

---

#### Day 2: OAuth Integration

**Branch**: `feature/oauth-google`

- [ ] Manual Setup (documented in PR description)
  - [ ] Create Google Cloud Console project
  - [ ] Enable APIs
  - [ ] Configure OAuth consent screen
  - [ ] Create credentials
- [ ] Google OAuth Implementation
  - [ ] Create `integrations/google_auth.py`
  - [ ] Implement authorization URL generation
  - [ ] Implement token exchange
  - [ ] Implement token refresh
  - [ ] Create encryption service
- [ ] Commit: "Implement Google OAuth integration"
- [ ] Create PR: "Google OAuth Integration (Gmail + Calendar)"

**Branch**: `feature/oauth-hubspot`

- [ ] Manual Setup (documented in PR description)
  - [ ] Create HubSpot developer account
  - [ ] Create app
  - [ ] Configure OAuth
- [ ] HubSpot OAuth Implementation
  - [ ] Create `integrations/hubspot_auth.py`
  - [ ] Implement authorization flow
  - [ ] Implement token exchange
- [ ] Commit: "Implement HubSpot OAuth integration"
- [ ] Create PR: "HubSpot OAuth Integration"

**Branch**: `feature/auth-api`

- [ ] API Endpoints
  - [ ] Create `api/auth.py`
  - [ ] Implement all OAuth endpoints
  - [ ] Add authentication middleware
- [ ] Commit: "Add OAuth API endpoints"
- [ ] Create PR: "OAuth API Endpoints"

**Branch**: `feature/integration-clients`

- [ ] Integration Service Classes
  - [ ] Create `integrations/gmail.py`
  - [ ] Create `integrations/calendar.py`
  - [ ] Create `integrations/hubspot.py`
  - [ ] Add error handling
- [ ] Commit: "Add integration client wrappers"
- [ ] Create PR: "Integration Client Services"

---

### Phase 2: Core DeepAgents Integration (Days 3-4)

#### Day 3: Custom Tools Development

**Branch**: `feature/gmail-tools`

- [ ] Gmail Tools Implementation
  - [ ] Create `agents/tools/gmail_tools.py`
  - [ ] Implement `search_emails` tool
  - [ ] Implement `send_email` tool
  - [ ] Implement `get_email` tool
  - [ ] Implement `reply_to_email` tool
  - [ ] Add tests
- [ ] Commit: "Implement Gmail tools for DeepAgents"
- [ ] Create PR: "Gmail Tools Implementation"

**Branch**: `feature/calendar-tools`

- [ ] Calendar Tools Implementation
  - [ ] Create `agents/tools/calendar_tools.py`
  - [ ] Implement `get_calendar_events` tool
  - [ ] Implement `create_calendar_event` tool
  - [ ] Implement `get_free_busy` tool
  - [ ] Add date/time utilities
  - [ ] Add tests
- [ ] Commit: "Implement Calendar tools for DeepAgents"
- [ ] Create PR: "Calendar Tools Implementation"

**Branch**: `feature/hubspot-tools`

- [ ] HubSpot Tools Implementation
  - [ ] Create `agents/tools/hubspot_tools.py`
  - [ ] Implement `search_contacts` tool
  - [ ] Implement `create_contact` tool
  - [ ] Implement `create_note` tool
  - [ ] Implement `get_contact_notes` tool
  - [ ] Add tests
- [ ] Commit: "Implement HubSpot tools for DeepAgents"
- [ ] Create PR: "HubSpot Tools Implementation"

---

#### Day 4: Main Agent & Subagents Setup

**Branch**: `feature/subagent-definitions`

- [ ] Subagent Definitions
  - [ ] Create `agents/subagents/__init__.py`
  - [ ] Define email_researcher_agent
  - [ ] Define calendar_scheduler_agent
  - [ ] Define hubspot_manager_agent
- [ ] Commit: "Add subagent definitions and prompts"
- [ ] Create PR: "Subagent Definitions"

**Branch**: `feature/main-agent`

- [ ] Main Agent Setup
  - [ ] Create `agents/main_agent.py`
  - [ ] Write financial advisor instructions
  - [ ] Implement agent factory function
  - [ ] Configure checkpointer
  - [ ] Add all tools and subagents
  - [ ] Add tests
- [ ] Commit: "Implement main financial advisor agent"
- [ ] Create PR: "Main Agent Implementation"

---

### Phase 3: RAG System (Days 5-6)

#### Day 5: Data Ingestion Pipeline

**Branch**: `feature/embedding-service`

- [ ] Embedding Service
  - [ ] Create `rag/embeddings.py`
  - [ ] Implement EmbeddingService class
  - [ ] Implement batch embedding
  - [ ] Add tests
- [ ] Commit: "Add OpenAI embedding service"
- [ ] Create PR: "Embedding Service Implementation"

**Branch**: `feature/gmail-ingestion`

- [ ] Gmail Ingestion
  - [ ] Create `rag/ingestion.py`
  - [ ] Implement `ingest_gmail_emails`
  - [ ] Add pagination
  - [ ] Add email body extraction
  - [ ] Add batching
  - [ ] Test with real account
- [ ] Commit: "Implement Gmail email ingestion pipeline"
- [ ] Create PR: "Gmail Ingestion Pipeline"

**Branch**: `feature/hubspot-ingestion`

- [ ] HubSpot Ingestion
  - [ ] Implement `ingest_hubspot_data`
  - [ ] Fetch contacts and notes
  - [ ] Combine for embedding
  - [ ] Test with real account
- [ ] Commit: "Implement HubSpot data ingestion pipeline"
- [ ] Create PR: "HubSpot Ingestion Pipeline"

**Branch**: `feature/sync-endpoint`

- [ ] Initial Sync Endpoint
  - [ ] Create `api/settings.py`
  - [ ] Implement `/api/sync/initial`
  - [ ] Add background tasks
  - [ ] Add progress tracking
- [ ] Commit: "Add initial data sync endpoint"
- [ ] Create PR: "Data Sync API"

---

#### Day 6: Retrieval Implementation

**Branch**: `feature/vector-search`

- [ ] Vector Search Implementation
  - [ ] Create `rag/retrieval.py`
  - [ ] Implement `semantic_search`
  - [ ] Add pgvector integration
  - [ ] Add filtering
  - [ ] Add database indexes
  - [ ] Test performance
- [ ] Commit: "Implement semantic search with pgvector"
- [ ] Create PR: "Vector Search Implementation"

**Branch**: `feature/rag-tools`

- [ ] RAG Tool
  - [ ] Create `agents/tools/rag_tools.py`
  - [ ] Implement `rag_search` tool
  - [ ] Integrate with semantic search
  - [ ] Add to main agent
  - [ ] Test from agent
- [ ] Commit: "Add RAG search tool for agents"
- [ ] Create PR: "RAG Search Tool"

**Branch**: `feature/incremental-sync`

- [ ] Incremental Sync
  - [ ] Implement `incremental_sync_gmail`
  - [ ] Implement `incremental_sync_hubspot`
  - [ ] Store last sync timestamps
  - [ ] Test updates
- [ ] Commit: "Add incremental data sync"
- [ ] Create PR: "Incremental Sync Implementation"

---

### Phase 4: Chat Interface (Days 7-8)

#### Day 7: Frontend Setup & Basic Chat UI

**Branch**: `feature/nextjs-setup`

- [ ] Initialize Next.js Project
  - [ ] Run create-next-app
  - [ ] Install dependencies
  - [ ] Configure Tailwind
  - [ ] Create project structure
  - [ ] Create `.env.local`
- [ ] Commit: "Initialize Next.js frontend"
- [ ] Create PR: "Next.js Frontend Setup"

**Branch**: `feature/chat-ui-components`

- [ ] Basic Chat Interface Components
  - [ ] Create `ChatInterface.tsx`
  - [ ] Create `MessageList.tsx`
  - [ ] Create `MessageBubble.tsx`
  - [ ] Create `InputArea.tsx`
  - [ ] Style to match ui.png
  - [ ] Add responsive design
- [ ] Commit: "Implement chat UI components"
- [ ] Create PR: "Chat Interface Components"

---

#### Day 8: API Integration & Rich Messages

**Branch**: `feature/streaming-api`

- [ ] Chat API Endpoint
  - [ ] Create `api/chat.py`
  - [ ] Implement SSE streaming
  - [ ] Integrate with DeepAgents
  - [ ] Add error handling
- [ ] Frontend SSE Integration
  - [ ] Implement `useChat.ts` hook
  - [ ] Parse SSE chunks
  - [ ] Update UI real-time
  - [ ] Add reconnection logic
- [ ] Commit: "Implement streaming chat API and SSE client"
- [ ] Create PR: "Streaming Chat API"

**Branch**: `feature/rich-message-components`

- [ ] Rich Message Components
  - [ ] Create `CalendarEventCard.tsx`
  - [ ] Create `ContactCard.tsx`
  - [ ] Add markdown parsing
  - [ ] Create `ContextSelector.tsx`
  - [ ] Implement message persistence
- [ ] Commit: "Add rich message components and context selector"
- [ ] Create PR: "Rich Message Components"

---

### Phase 5: Task Persistence & Memory (Days 9-10)

#### Day 9: Task Management System

**Branch**: `feature/task-manager`

- [ ] Task Manager Service
  - [ ] Create `services/task_manager.py`
  - [ ] Implement TaskManager class
  - [ ] Implement all methods
  - [ ] Add task resumption logic
- [ ] Agent Task Tools
  - [ ] Create `agents/tools/task_tools.py`
  - [ ] Implement `create_waiting_task` tool
  - [ ] Add to main agent
  - [ ] Test task creation
- [ ] Commit: "Implement task management system"
- [ ] Create PR: "Task Management and Persistence"

---

#### Day 10: Ongoing Instructions & Polling Service

**Branch**: `feature/instruction-manager`

- [ ] Instruction Manager
  - [ ] Create `services/instruction_manager.py`
  - [ ] Implement InstructionManager class
  - [ ] Create API endpoints
  - [ ] Create frontend UI
- [ ] Commit: "Implement ongoing instructions manager"
- [ ] Create PR: "Ongoing Instructions Management"

**Branch**: `feature/polling-service`

- [ ] Polling Service
  - [ ] Create `services/polling_service.py`
  - [ ] Implement PollingService class
  - [ ] Implement Gmail polling
  - [ ] Implement instruction evaluation
  - [ ] Set up APScheduler
  - [ ] Test polling
- [ ] Commit: "Implement polling service for proactive actions"
- [ ] Create PR: "Polling Service Implementation"

---

### Phase 6: Testing & Refinement (Days 11-12)

#### Day 11: Core Workflow Testing

**Branch**: `test/end-to-end`

- [ ] RAG Query Testing
  - [ ] Test baseball question
  - [ ] Test stock question
  - [ ] Test various filters
  - [ ] Measure accuracy
- [ ] Multi-Step Task Testing
  - [ ] Test meeting scheduling
  - [ ] Test follow-ups
  - [ ] Test error handling
- [ ] Ongoing Instruction Testing
  - [ ] Test HubSpot contact creation
  - [ ] Test calendar event emails
  - [ ] Test polling cycle
- [ ] Commit: "Add end-to-end tests for core workflows"
- [ ] Create PR: "End-to-End Testing"

---

#### Day 12: Polish & Documentation

**Branch**: `fix/error-handling`

- [ ] Error Handling
  - [ ] Add try-catch to all endpoints
  - [ ] Add retry logic
  - [ ] Add user-friendly messages
  - [ ] Add error logging
- [ ] Commit: "Improve error handling across application"
- [ ] Create PR: "Error Handling Improvements"

**Branch**: `feature/token-refresh`

- [ ] OAuth Token Refresh
  - [ ] Implement auto-refresh for Google
  - [ ] Implement auto-refresh for HubSpot
  - [ ] Handle expiration gracefully
  - [ ] Add re-auth UI prompt
- [ ] Commit: "Implement automatic OAuth token refresh"
- [ ] Create PR: "OAuth Token Refresh"

**Branch**: `feature/ui-polish`

- [ ] UI Polish
  - [ ] Add loading states
  - [ ] Add skeleton loaders
  - [ ] Create empty states
  - [ ] Improve responsiveness
  - [ ] Add keyboard shortcuts
  - [ ] Add accessibility
- [ ] Commit: "Polish UI with loading states and accessibility"
- [ ] Create PR: "UI Polish and Improvements"

**Branch**: `feature/deployment`

- [ ] Deployment Preparation
  - [ ] Create backend Dockerfile
  - [ ] Create frontend Dockerfile
  - [ ] Create docker-compose.yml
  - [ ] Test Docker build
  - [ ] Update documentation
- [ ] Commit: "Add Docker deployment configuration"
- [ ] Create PR: "Deployment Configuration"

---

## Best Practices for AI Assistants

### When Implementing Features

1. **Always create a feature branch first**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Work on ONE feature at a time**
   - Don't mix multiple features in one branch
   - Keep PRs focused and reviewable

3. **Commit frequently with good messages**
   - Commit after each logical unit of work
   - Write descriptive commit messages

4. **Test before creating PR**
   - Run the code locally
   - Test the specific feature
   - Check for errors

5. **Create detailed PRs**
   - Explain what was implemented
   - List testing done
   - Reference related issues/docs

### When User Asks to Implement Something

**Good Flow**:
```
User: "Implement the Gmail tools"

AI Assistant:
1. Check current branch (should be on master)
2. Create feature branch: git checkout -b feature/gmail-tools
3. Implement the Gmail tools in agents/tools/gmail_tools.py
4. Test the implementation
5. Commit: "Implement Gmail tools for DeepAgents"
6. Push: git push origin feature/gmail-tools
7. Create PR with detailed description
8. Respond to user: "Gmail tools implemented in feature/gmail-tools branch. PR created."
```

**Bad Flow** (Don't do this):
```
User: "Implement the Gmail tools"

AI Assistant:
❌ Implements directly on master branch
❌ Commits without testing
❌ No PR created
❌ Implements multiple unrelated features together
```

### When Asked to Fix a Bug

```bash
# Create fix branch
git checkout -b fix/token-expiration-error

# Fix the bug
# ... make changes ...

# Test the fix
# ... verify it works ...

# Commit with descriptive message
git commit -m "Fix token expiration error in Google OAuth

- Add expiration check before API calls
- Implement automatic refresh
- Add error handling for refresh failures

Fixes #42"

# Push and create PR
git push origin fix/token-expiration-error
gh pr create --title "Fix: Token expiration error in Google OAuth"
```

### When Asked to Add Tests

```bash
# Create test branch
git checkout -b test/gmail-tools-unit-tests

# Add tests
# ... create test files ...

# Run tests
pytest tests/

# Commit
git commit -m "Add unit tests for Gmail tools

- Test search_emails with various queries
- Test send_email success and error cases
- Test get_email with valid/invalid IDs
- Mock Gmail API responses"

# Push and create PR
git push origin test/gmail-tools-unit-tests
```

---

## Common Scenarios & Solutions

### Scenario 1: Multiple Related Changes

**Question**: "I need to implement OAuth for both Google and HubSpot. Should I use one branch or two?"

**Answer**: Create **separate branches** for each OAuth provider:
- `feature/oauth-google` - Google OAuth implementation
- `feature/oauth-hubspot` - HubSpot OAuth implementation

Why? Each can be reviewed, tested, and merged independently. If one has issues, it doesn't block the other.

### Scenario 2: Discovered a Bug While Implementing Feature

**Question**: "I'm implementing calendar tools but found a bug in the database models. What do I do?"

**Answer**:
1. Note the bug in your current work
2. Stash or commit current work: `git stash` or `git commit -m "WIP: calendar tools"`
3. Go back to master: `git checkout master`
4. Create fix branch: `git checkout -b fix/database-model-bug`
5. Fix the bug, test, commit, push, create PR
6. Go back to feature branch: `git checkout feature/calendar-tools`
7. Apply stashed changes if needed: `git stash pop`
8. Continue feature work

### Scenario 3: Feature Depends on Another Feature

**Question**: "I'm working on RAG tools, but it depends on the embedding service which isn't merged yet. What do I do?"

**Answer**:
**Option 1** (Recommended): Wait for dependency to be merged
- Implement embedding service first (feature/embedding-service)
- Get it reviewed and merged to master
- Then start RAG tools branch from latest master

**Option 2**: Branch from feature branch
```bash
# If embedding-service branch exists but not merged
git checkout feature/embedding-service
git checkout -b feature/rag-tools

# Note in PR: "Depends on #PR_NUMBER (embedding-service)"
```

### Scenario 4: User Asks for Multiple Features at Once

**Question**: User says: "Implement Gmail tools, Calendar tools, and HubSpot tools"

**Answer**: Create **three separate branches** and work on them sequentially or in parallel:
```bash
# Approach 1: Sequential (one at a time)
git checkout -b feature/gmail-tools
# Implement, test, commit, push, PR
# After merged, move to next:
git checkout master && git pull
git checkout -b feature/calendar-tools
# Repeat...

# Approach 2: Parallel (if independent)
git checkout -b feature/gmail-tools
# Implement, commit, push, PR (don't wait for merge)
git checkout master
git checkout -b feature/calendar-tools
# Implement, commit, push, PR
# Continue for HubSpot tools
```

Inform user: "I'll create three separate PRs for better code review: Gmail tools, Calendar tools, and HubSpot tools."

---

## Code Quality Checklist

Before creating a PR, ensure:

- [ ] Code follows Python PEP 8 style guide (backend)
- [ ] Code follows TypeScript/React best practices (frontend)
- [ ] All functions have docstrings/JSDoc comments
- [ ] Type hints/types are added (Python type hints, TypeScript types)
- [ ] Error handling is implemented
- [ ] No hardcoded credentials or secrets
- [ ] Environment variables used for configuration
- [ ] Tests added (or explain why not needed)
- [ ] Code tested locally and works
- [ ] No commented-out code (remove or explain)
- [ ] Console.log/print statements removed (or use proper logging)
- [ ] Imports organized and unused imports removed

---

## PR Template

Use this template when creating pull requests:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation
- [ ] Testing

## Changes Made
- Bullet point 1
- Bullet point 2
- Bullet point 3

## Testing Done
- [x] Tested locally
- [x] Unit tests added/updated
- [x] Integration tests pass
- [ ] Manual testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
- Closes #issue_number
- Related to #issue_number
- Part of Phase X, Day Y of MVP Plan

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)
- [ ] Tests pass locally
```

---

## Emergency Procedures

### If You Accidentally Committed to Master

```bash
# STOP! Don't push to master if you can avoid it

# Option 1: Reset and create proper branch
git reset --soft HEAD~1  # Undo commit, keep changes
git checkout -b feature/proper-branch-name
git commit -m "Your commit message"
git push origin feature/proper-branch-name

# Option 2: If already pushed to master (emergency)
# Contact team lead/maintainer immediately
# They may need to revert the commit
```

### If You Need to Update a PR with Master Changes

```bash
# Your feature branch is behind master
git checkout feature/your-feature
git fetch origin
git rebase origin/master  # or git merge origin/master

# Resolve conflicts if any
# Then push (may need force push if rebased)
git push origin feature/your-feature --force-with-lease
```

### If Tests Fail in CI/CD

```bash
# Pull latest PR changes
git checkout feature/your-feature
git pull

# Run tests locally
pytest  # or npm test

# Fix issues
# Commit and push fix
git add .
git commit -m "Fix failing tests"
git push origin feature/your-feature

# CI/CD will re-run automatically
```

---

## Tips for Success

1. **Read the MVP Plan before starting** - Understand the full context
2. **Follow the TODO list sequentially** - Each task builds on previous ones
3. **Keep PRs small** - Easier to review, faster to merge
4. **Write good commit messages** - Future you will thank you
5. **Test thoroughly** - Don't assume it works
6. **Ask questions** - If unclear, ask before implementing
7. **Document as you go** - Update docs with your changes
8. **Review your own PR first** - Catch obvious issues
9. **Be patient with reviews** - Give reviewers time
10. **Learn from feedback** - PR comments are learning opportunities

---

## Resources

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **DeepAgents Docs**: See project README
- **LangChain Docs**: https://docs.langchain.com/
- **MVP Plan**: [../docs/MVP_PLAN.md](../docs/MVP_PLAN.md)
- **Setup Guide**: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)

---

## Summary

This CLAUDE.md file provides:
1. ✅ Complete MVP TODO list organized by phases and branches
2. ✅ Git workflow guidelines (branching, committing, PRs)
3. ✅ Branch naming conventions
4. ✅ Commit message guidelines
5. ✅ PR creation instructions
6. ✅ Best practices for AI assistants
7. ✅ Common scenarios and solutions
8. ✅ Code quality checklist
9. ✅ Emergency procedures

**Remember**: Always create a feature branch, never commit directly to master, and create PRs for all changes!

Good luck building the Financial Advisor AI Agent MVP! 🚀