# Financial Advisor AI Agent - MVP Development TODO

This is a comprehensive checklist derived from the MVP Implementation Plan. Use this to track your progress during development.

---

## Phase 1: Foundation & OAuth (Days 1-2)

### Day 1: Project Setup & Backend Foundation

- [ ] **Initialize Backend Project**
  - [ ] Create `financial-advisor-agent` directory
  - [ ] Create `backend` subdirectory
  - [ ] Create Python virtual environment (`python -m venv venv`)
  - [ ] Activate virtual environment
  - [ ] Install base dependencies (fastapi, uvicorn, sqlalchemy, psycopg2-binary)
  - [ ] Install DeepAgents and LangChain packages
  - [ ] Install Google API packages
  - [ ] Install HubSpot API client
  - [ ] Create `requirements.txt` file

- [ ] **Create Project Structure**
  - [ ] Create `app/__init__.py`
  - [ ] Create `app/main.py`
  - [ ] Create `app/config.py`
  - [ ] Create `app/database.py`
  - [ ] Create `app/models/` directory with `__init__.py`
  - [ ] Create `app/api/` directory with `__init__.py`
  - [ ] Create `app/integrations/` directory with `__init__.py`
  - [ ] Create `app/agents/` directory with subdirectories
  - [ ] Create `app/rag/` directory with `__init__.py`
  - [ ] Create `app/services/` directory with `__init__.py`
  - [ ] Create `app/schemas/` directory with `__init__.py`

- [ ] **Database Models Setup**
  - [ ] Create `models/user.py` - User model with OAuth tokens
  - [ ] Create `models/conversation.py` - Conversation model
  - [ ] Create `models/message.py` - Message model
  - [ ] Create `models/task.py` - Task model for multi-step workflows
  - [ ] Create `models/instruction.py` - OngoingInstruction model
  - [ ] Create `models/document_embedding.py` - DocumentEmbedding model with pgvector
  - [ ] Initialize Alembic for migrations
  - [ ] Create initial migration
  - [ ] Test migration with local database

- [ ] **Configuration Management**
  - [ ] Create `.env.example` template
  - [ ] Implement `config.py` with Pydantic Settings
  - [ ] Add environment validation
  - [ ] Create `.gitignore` file

---

### Day 2: OAuth Integration

- [ ] **Manual Setup Tasks**
  - [ ] Create Google Cloud Console project
  - [ ] Enable Gmail API
  - [ ] Enable Google Calendar API
  - [ ] Configure OAuth consent screen
  - [ ] Add scopes (gmail, calendar, userinfo)
  - [ ] Add `webshookeng@gmail.com` as test user
  - [ ] Create OAuth 2.0 credentials
  - [ ] Copy Client ID and Client Secret
  - [ ] Create HubSpot developer account
  - [ ] Create HubSpot public app
  - [ ] Configure HubSpot redirect URLs
  - [ ] Select HubSpot scopes (contacts, deals)
  - [ ] Copy HubSpot App ID, Client ID, Client Secret

- [ ] **Google OAuth Implementation**
  - [ ] Create `integrations/google_auth.py`
  - [ ] Implement authorization URL generation
  - [ ] Implement token exchange logic
  - [ ] Implement token refresh logic
  - [ ] Create encryption service for tokens
  - [ ] Test OAuth flow end-to-end

- [ ] **HubSpot OAuth Implementation**
  - [ ] Create `integrations/hubspot_auth.py`
  - [ ] Implement authorization URL generation
  - [ ] Implement token exchange logic
  - [ ] Create token storage logic
  - [ ] Test OAuth flow end-to-end

- [ ] **API Endpoints**
  - [ ] Create `api/auth.py`
  - [ ] Implement `POST /api/auth/google/login`
  - [ ] Implement `GET /api/auth/google/callback`
  - [ ] Implement `POST /api/auth/hubspot/login`
  - [ ] Implement `GET /api/auth/hubspot/callback`
  - [ ] Implement `GET /api/auth/status`
  - [ ] Add authentication middleware
  - [ ] Test all endpoints with Postman/curl

- [ ] **Integration Service Classes**
  - [ ] Create `integrations/gmail.py` - GmailClient wrapper
  - [ ] Implement list_messages, get_message, send_message
  - [ ] Implement search_messages
  - [ ] Create `integrations/calendar.py` - CalendarClient wrapper
  - [ ] Implement list_events, create_event, get_free_busy
  - [ ] Create `integrations/hubspot.py` - HubSpotClient wrapper
  - [ ] Implement get_contacts, create_contact, get_notes, create_note
  - [ ] Add error handling and retry logic

---

## Phase 2: Core DeepAgents Integration (Days 3-4)

### Day 3: Custom Tools Development

- [ ] **Gmail Tools**
  - [ ] Create `agents/tools/gmail_tools.py`
  - [ ] Implement `search_emails(query, max_results, user_id)` tool
  - [ ] Implement `send_email(to, subject, body, user_id)` tool
  - [ ] Implement `get_email(email_id, user_id)` tool
  - [ ] Implement `reply_to_email(email_id, body, user_id)` tool
  - [ ] Add proper type annotations
  - [ ] Add comprehensive docstrings
  - [ ] Test each tool individually

- [ ] **Calendar Tools**
  - [ ] Create `agents/tools/calendar_tools.py`
  - [ ] Implement `get_calendar_events(start_date, end_date, user_id)` tool
  - [ ] Implement `create_calendar_event(title, start, end, attendees, user_id)` tool
  - [ ] Implement `get_free_busy(email, start, end, user_id)` tool
  - [ ] Add date/time parsing utilities
  - [ ] Add timezone handling
  - [ ] Test each tool individually

- [ ] **HubSpot Tools**
  - [ ] Create `agents/tools/hubspot_tools.py`
  - [ ] Implement `search_contacts(query, user_id)` tool
  - [ ] Implement `create_contact(email, properties, user_id)` tool
  - [ ] Implement `create_note(contact_id, note_text, user_id)` tool
  - [ ] Implement `get_contact_notes(contact_id, user_id)` tool
  - [ ] Add HubSpot API error handling
  - [ ] Test each tool individually

- [ ] **Tool Testing**
  - [ ] Create test script for Gmail tools
  - [ ] Create test script for Calendar tools
  - [ ] Create test script for HubSpot tools
  - [ ] Verify all tools work with real APIs

---

### Day 4: Main Agent & Subagents Setup

- [ ] **Subagent Definitions**
  - [ ] Create `agents/subagents/__init__.py`
  - [ ] Define email_researcher_agent configuration
  - [ ] Write email researcher prompt
  - [ ] Define calendar_scheduler_agent configuration
  - [ ] Write calendar scheduler prompt
  - [ ] Define hubspot_manager_agent configuration
  - [ ] Write HubSpot manager prompt

- [ ] **Main Agent Setup**
  - [ ] Create `agents/main_agent.py`
  - [ ] Write FINANCIAL_ADVISOR_INSTRUCTIONS prompt
  - [ ] Implement `create_financial_advisor_agent()` function
  - [ ] Configure all tools for main agent
  - [ ] Add all subagents to configuration
  - [ ] Set up PostgresSaver checkpointer
  - [ ] Test agent initialization

- [ ] **Agent Testing**
  - [ ] Create test script for main agent
  - [ ] Test subagent invocation
  - [ ] Test tool calling from main agent
  - [ ] Test conversation persistence with checkpointer
  - [ ] Verify agent can use write_todos tool

---

## Phase 3: RAG System (Days 5-6)

### Day 5: Data Ingestion Pipeline

- [ ] **Embedding Service**
  - [ ] Create `rag/embeddings.py`
  - [ ] Implement EmbeddingService class
  - [ ] Implement `embed_text(text)` method
  - [ ] Implement `embed_batch(texts)` method
  - [ ] Test with sample texts
  - [ ] Measure embedding performance

- [ ] **Gmail Ingestion**
  - [ ] Create `rag/ingestion.py`
  - [ ] Implement `ingest_gmail_emails(user_id, gmail_client, embedding_service, db)`
  - [ ] Add pagination for large inboxes
  - [ ] Implement email body extraction logic
  - [ ] Add batching for embedding calls
  - [ ] Implement storage in document_embeddings table
  - [ ] Test with real Gmail account

- [ ] **HubSpot Ingestion**
  - [ ] Implement `ingest_hubspot_data(user_id, hubspot_client, embedding_service, db)`
  - [ ] Fetch all contacts
  - [ ] Fetch contact notes
  - [ ] Combine contact info with notes for embedding
  - [ ] Store in document_embeddings table
  - [ ] Test with real HubSpot account

- [ ] **Initial Sync Endpoint**
  - [ ] Create `api/settings.py`
  - [ ] Implement `POST /api/sync/initial` endpoint
  - [ ] Add background task for ingestion
  - [ ] Add progress tracking
  - [ ] Add sync status endpoint
  - [ ] Test full sync workflow

- [ ] **Incremental Sync Logic**
  - [ ] Implement `incremental_sync_gmail(user_id, ...)`
  - [ ] Use "after:" query for new emails
  - [ ] Implement `incremental_sync_hubspot(user_id, ...)`
  - [ ] Use "recently modified" filter for contacts
  - [ ] Store last sync timestamp per user/source
  - [ ] Test incremental updates

---

### Day 6: Retrieval Implementation

- [ ] **Vector Search**
  - [ ] Create `rag/retrieval.py`
  - [ ] Implement `semantic_search(db, query, user_id, embedding_service, top_k)`
  - [ ] Use pgvector cosine distance for similarity
  - [ ] Add source_type filtering
  - [ ] Add metadata filtering
  - [ ] Test search with various queries

- [ ] **RAG Tool**
  - [ ] Create `agents/tools/rag_tools.py`
  - [ ] Implement `rag_search(query, source_type, top_k, state)` tool
  - [ ] Integrate with semantic_search function
  - [ ] Format results for agent consumption
  - [ ] Add to main agent tools
  - [ ] Test RAG search from agent

- [ ] **Search Optimization**
  - [ ] Create database indexes for performance
  - [ ] Test search performance with 1000+ documents
  - [ ] Implement caching for common queries
  - [ ] Add query preprocessing (lowercasing, etc.)

---

## Phase 4: Chat Interface (Days 7-8)

### Day 7: Frontend Setup & Basic Chat UI

- [ ] **Initialize Next.js Project**
  - [ ] Run `create-next-app` with TypeScript and Tailwind
  - [ ] Install @tanstack/react-query
  - [ ] Install axios
  - [ ] Install lucide-react for icons
  - [ ] Install eventsource-parser for SSE
  - [ ] Configure Tailwind with custom colors

- [ ] **Project Structure**
  - [ ] Create `app/(auth)/login/page.tsx`
  - [ ] Create `app/(app)/layout.tsx`
  - [ ] Create `app/(app)/chat/page.tsx`
  - [ ] Create `app/(app)/settings/page.tsx`
  - [ ] Create `components/chat/` directory
  - [ ] Create `components/ui/` directory
  - [ ] Create `lib/api.ts` for API utilities
  - [ ] Create `hooks/useChat.ts`

- [ ] **Basic Chat Interface**
  - [ ] Create `components/chat/ChatInterface.tsx`
  - [ ] Create `components/chat/MessageList.tsx`
  - [ ] Create `components/chat/MessageBubble.tsx`
  - [ ] Create `components/chat/InputArea.tsx`
  - [ ] Add textarea with auto-resize
  - [ ] Add send button
  - [ ] Implement local message state management

- [ ] **Styling**
  - [ ] Match ui.png design for chat interface
  - [ ] Style message bubbles (user vs assistant)
  - [ ] Add timestamp display
  - [ ] Make interface responsive
  - [ ] Add loading indicators

---

### Day 8: API Integration & Rich Messages

- [ ] **Chat API Endpoint**
  - [ ] Create `api/chat.py` in backend
  - [ ] Implement `POST /api/chat/stream` endpoint
  - [ ] Add Server-Sent Events (SSE) streaming
  - [ ] Integrate with DeepAgents
  - [ ] Pass user_id to agent
  - [ ] Stream agent responses in real-time
  - [ ] Handle errors gracefully

- [ ] **Frontend Integration**
  - [ ] Implement SSE client in `useChat.ts`
  - [ ] Parse streamed chunks
  - [ ] Update UI in real-time
  - [ ] Handle connection errors
  - [ ] Add reconnection logic

- [ ] **Rich Message Components**
  - [ ] Create `components/chat/CalendarEventCard.tsx`
  - [ ] Display event title, time, attendees
  - [ ] Create `components/chat/ContactCard.tsx`
  - [ ] Display contact name, email, company
  - [ ] Parse markdown in messages
  - [ ] Add syntax highlighting for code blocks

- [ ] **Context Selector**
  - [ ] Create `components/chat/ContextSelector.tsx`
  - [ ] Add dropdown with options (all, emails, calendar, hubspot)
  - [ ] Pass context to backend
  - [ ] Filter RAG results based on context
  - [ ] Show selected context in UI

- [ ] **Message Persistence**
  - [ ] Save messages to database after each exchange
  - [ ] Load conversation history on page load
  - [ ] Implement conversation list sidebar
  - [ ] Add "New chat" button
  - [ ] Implement conversation deletion

---

## Phase 5: Task Persistence & Memory (Days 9-10)

### Day 9: Task Management System

- [ ] **Task Manager Service**
  - [ ] Create `services/task_manager.py`
  - [ ] Implement TaskManager class
  - [ ] Implement `create_task(user_id, description, context)`
  - [ ] Implement `update_task_status(task_id, status, context)`
  - [ ] Implement `get_waiting_tasks(user_id)`
  - [ ] Implement `find_task_for_email(user_id, email_from, email_subject)`

- [ ] **Agent Task Tools**
  - [ ] Create `agents/tools/task_tools.py`
  - [ ] Implement `create_waiting_task(description, waiting_for, expected_from, context)` tool
  - [ ] Add tool to main agent
  - [ ] Add TaskManager to agent state
  - [ ] Test task creation from agent

- [ ] **Task Resumption Logic**
  - [ ] Implement `resume_task(task, event_data, agent, db)` in task_manager.py
  - [ ] Load task context from database
  - [ ] Create continuation message for agent
  - [ ] Invoke agent with task context
  - [ ] Update task status based on result
  - [ ] Test task resumption

- [ ] **Example Workflow Testing**
  - [ ] Test "Schedule meeting with Sara Smith" workflow
  - [ ] Verify agent creates waiting task
  - [ ] Manually send reply email
  - [ ] Verify task resumes correctly
  - [ ] Verify final actions (calendar creation, notification)

---

### Day 10: Ongoing Instructions & Polling Service

- [ ] **Instruction Manager**
  - [ ] Create `services/instruction_manager.py`
  - [ ] Implement InstructionManager class
  - [ ] Implement `add_instruction(user_id, instruction)`
  - [ ] Implement `get_active_instructions(user_id)`
  - [ ] Implement `deactivate_instruction(instruction_id)`

- [ ] **Polling Service**
  - [ ] Create `services/polling_service.py`
  - [ ] Implement PollingService class
  - [ ] Implement `poll_gmail(user_id)` method
  - [ ] Implement `process_new_email(user_id, email)` method
  - [ ] Implement `evaluate_instructions(user_id, email, instructions)` method
  - [ ] Set up APScheduler to poll every 2 minutes
  - [ ] Test polling with real Gmail account

- [ ] **Instruction Evaluation**
  - [ ] Create prompt for instruction evaluation
  - [ ] Pass ongoing instructions to agent
  - [ ] Let agent decide if instructions apply
  - [ ] Execute actions if instructions match
  - [ ] Log all proactive actions

- [ ] **Instruction Management API**
  - [ ] Implement `GET /api/instructions` endpoint
  - [ ] Implement `POST /api/instructions` endpoint
  - [ ] Implement `DELETE /api/instructions/:id` endpoint
  - [ ] Create frontend UI for managing instructions

- [ ] **Frontend for Instructions**
  - [ ] Create `app/(app)/settings/instructions/page.tsx`
  - [ ] Add form to create new instruction
  - [ ] Display list of active instructions
  - [ ] Add delete button for each instruction
  - [ ] Test instruction CRUD operations

---

## Phase 6: Testing & Refinement (Days 11-12)

### Day 11: Core Workflow Testing

- [ ] **RAG Query Testing**
  - [ ] Test: "Who mentioned their kid plays baseball?"
  - [ ] Verify relevant emails are retrieved
  - [ ] Test: "Why did Greg say he wanted to sell AAPL stock?"
  - [ ] Test with various date ranges
  - [ ] Test filtering by source (emails vs HubSpot)
  - [ ] Measure search accuracy and relevance

- [ ] **Multi-Step Task Testing**
  - [ ] Test: "Schedule an appointment with Sara Smith"
    - [ ] Verify HubSpot/email search occurs
    - [ ] Verify calendar availability check
    - [ ] Verify email sent with time options
    - [ ] Verify waiting task created
    - [ ] Send manual reply and verify task resumes
    - [ ] Verify calendar event created
    - [ ] Verify HubSpot note added
  - [ ] Test: "Send follow-up to everyone I met with this week"
    - [ ] Verify calendar queried for week's meetings
    - [ ] Verify emails sent to all attendees
  - [ ] Test error handling (contact not found, etc.)

- [ ] **Ongoing Instruction Testing**
  - [ ] Add instruction: "When someone emails me not in HubSpot, create a contact"
  - [ ] Send test email from new address
  - [ ] Wait for polling cycle (2-5 min)
  - [ ] Verify contact created in HubSpot
  - [ ] Verify note added about email
  - [ ] Test: "When I add calendar event, email attendees"
  - [ ] Create calendar event manually
  - [ ] Verify polling detects new event
  - [ ] Verify emails sent to attendees

- [ ] **Subagent Testing**
  - [ ] Test email-researcher subagent directly
  - [ ] Test calendar-scheduler subagent directly
  - [ ] Test hubspot-manager subagent directly
  - [ ] Verify subagent results returned to main agent
  - [ ] Verify main agent uses subagent results correctly

- [ ] **End-to-End Testing**
  - [ ] Complete full user journey: OAuth → Sync → Chat → Tasks
  - [ ] Test with multiple users
  - [ ] Test concurrent requests
  - [ ] Monitor performance metrics
  - [ ] Check database for data integrity

---

### Day 12: Polish & Documentation

- [ ] **Error Handling**
  - [ ] Add try-catch to all API endpoints
  - [ ] Add retry logic for API calls (Gmail, Calendar, HubSpot)
  - [ ] Add user-friendly error messages in UI
  - [ ] Implement error logging (file or service like Sentry)
  - [ ] Test error scenarios (network failure, invalid tokens, etc.)

- [ ] **OAuth Token Refresh**
  - [ ] Implement automatic token refresh for Google
  - [ ] Implement automatic token refresh for HubSpot
  - [ ] Handle token expiration gracefully
  - [ ] Add UI prompt for re-authentication when needed
  - [ ] Test token refresh logic

- [ ] **UI Polish**
  - [ ] Add loading states for all async operations
  - [ ] Add skeleton loaders for message list
  - [ ] Create empty state for no conversations
  - [ ] Create empty state for no messages
  - [ ] Make UI fully responsive (mobile, tablet, desktop)
  - [ ] Add keyboard shortcuts (Enter to send, etc.)
  - [ ] Add accessibility attributes (ARIA labels, etc.)
  - [ ] Test on different browsers (Chrome, Firefox, Safari)

- [ ] **Environment Setup**
  - [ ] Create comprehensive `.env.example` file
  - [ ] Document each environment variable
  - [ ] Add validation for required variables
  - [ ] Add setup instructions to README

- [ ] **Deployment Preparation**
  - [ ] Create `Dockerfile` for backend
  - [ ] Create `Dockerfile` for frontend
  - [ ] Create `docker-compose.yml` for local dev
  - [ ] Create `docker-compose.prod.yml` for production
  - [ ] Add database migration script to Docker entrypoint
  - [ ] Test Docker build and run locally

- [ ] **Documentation**
  - [ ] Update README with quick start guide
  - [ ] Add API documentation (Swagger/OpenAPI)
  - [ ] Document agent prompts and their purpose
  - [ ] Add troubleshooting section
  - [ ] Create architecture diagram
  - [ ] Document deployment process

---

## MVP Completion Checklist

- [ ] **Authentication**
  - [ ] Users can authenticate with Google (Gmail + Calendar)
  - [ ] Users can connect HubSpot account
  - [ ] OAuth test user `webshookeng@gmail.com` works
  - [ ] Tokens are encrypted and stored securely

- [ ] **Data Sync**
  - [ ] Initial sync imports all Gmail emails
  - [ ] Initial sync imports all HubSpot contacts and notes
  - [ ] Data is embedded with OpenAI embeddings
  - [ ] Embeddings stored in pgvector database
  - [ ] Incremental sync updates new data

- [ ] **Chat Interface**
  - [ ] ChatGPT-like interface works
  - [ ] Messages stream in real-time
  - [ ] Conversation history persists
  - [ ] New conversation creation works
  - [ ] Interface matches ui.png design
  - [ ] Mobile responsive

- [ ] **RAG Queries**
  - [ ] Can ask questions about clients (e.g., "Who mentioned baseball?")
  - [ ] Semantic search returns relevant results
  - [ ] Can filter by source (emails, HubSpot, all)
  - [ ] Results include proper context and metadata

- [ ] **Multi-Step Tasks**
  - [ ] Can schedule appointments via natural language
  - [ ] Agent searches contacts and emails
  - [ ] Agent checks calendar availability
  - [ ] Agent sends emails
  - [ ] Tasks wait for responses and resume automatically
  - [ ] Calendar events created after confirmation
  - [ ] HubSpot notes added for interactions

- [ ] **Ongoing Instructions**
  - [ ] Can add ongoing instructions via settings
  - [ ] Instructions stored in database
  - [ ] Polling service checks for new events (2-5 min interval)
  - [ ] Agent evaluates if instructions apply to events
  - [ ] Proactive actions executed based on instructions
  - [ ] Example: "Create HubSpot contact for new emailers" works

- [ ] **Tools & Subagents**
  - [ ] All Gmail tools work (search, send, get, reply)
  - [ ] All Calendar tools work (events, create, free/busy)
  - [ ] All HubSpot tools work (search, create, notes)
  - [ ] RAG search tool works
  - [ ] Email researcher subagent works
  - [ ] Calendar scheduler subagent works
  - [ ] HubSpot manager subagent works

- [ ] **Deployment Ready**
  - [ ] All environment variables documented
  - [ ] Docker setup works
  - [ ] Database migrations run correctly
  - [ ] Application runs in Docker containers
  - [ ] README has deployment instructions

---

## Post-MVP Enhancements (Optional)

Once MVP is complete, consider these improvements:

- [ ] Replace polling with real-time webhooks (Gmail Pub/Sub, HubSpot webhooks)
- [ ] Add analytics dashboard for usage tracking
- [ ] Implement advanced RAG (hybrid search, reranking)
- [ ] Add email templates for common scenarios
- [ ] Add voice interface
- [ ] Multi-language support
- [ ] Team collaboration features

See [FULL_IMPLEMENTATION.md](./FULL_IMPLEMENTATION.md) for details on advanced features.

---

## Notes & Tips

- **Use DeepAgents Virtual Filesystem**: Store draft emails, reports in agent's virtual filesystem
- **Leverage Subagents**: Use subagents for focused, complex tasks to keep main context clean
- **Test Incrementally**: Test each component as you build (don't wait until end)
- **Monitor Token Usage**: Keep an eye on LLM costs during development
- **Commit Often**: Git commit after each completed task
- **Ask for Help**: Use docs, forums, and GitHub issues when stuck

---

## Success Metrics

MVP is successful when:
- ✅ User can complete OAuth flows without errors
- ✅ Data sync completes for 100+ emails and 10+ contacts
- ✅ RAG queries return accurate results >80% of the time
- ✅ Multi-step task (meeting scheduling) completes end-to-end
- ✅ Ongoing instruction triggers proactive action correctly
- ✅ Application runs without crashes for 1+ hour
- ✅ All tests pass
- ✅ Application is deployment-ready

Good luck with your MVP development! 🚀
