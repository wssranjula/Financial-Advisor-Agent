# Financial Advisor AI Agent - MVP Implementation Plan

## Overview

This document outlines the 12-day plan for building an MVP of the Financial Advisor AI Agent using the DeepAgents framework. The MVP focuses on core functionality with a polling-based event system for simplicity.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Agent Framework**: LangChain + DeepAgents
- **Database**: PostgreSQL 15+ with pgvector extension
- **LLM**: Anthropic Claude Sonnet 4 (via DeepAgents default)
- **Embeddings**: OpenAI text-embedding-3-small
- **Task Queue**: APScheduler for polling

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Real-time**: Server-Sent Events (SSE)
- **State Management**: React Context + hooks

### Integrations
- **Google OAuth 2.0**: Gmail API + Google Calendar API
- **HubSpot OAuth 2.0**: CRM API (Contacts + Engagements)

## Phase-by-Phase Implementation

---

## Phase 1: Foundation & OAuth (Days 1-2)

### Day 1: Project Setup & Backend Foundation

#### Tasks
1. **Initialize Backend Project**
   ```bash
   mkdir financial-advisor-agent
   cd financial-advisor-agent
   mkdir backend frontend
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
   pip install deepagents langchain langchain-openai
   pip install google-auth google-auth-oauthlib google-auth-httplib2
   pip install google-api-python-client hubspot-api-client
   pip install pgvector asyncpg apscheduler
   ```

2. **Create Project Structure**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── config.py
   │   ├── database.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   ├── user.py
   │   │   ├── conversation.py
   │   │   ├── task.py
   │   │   └── instruction.py
   │   ├── api/
   │   │   ├── __init__.py
   │   │   ├── auth.py
   │   │   ├── chat.py
   │   │   └── settings.py
   │   ├── integrations/
   │   │   ├── __init__.py
   │   │   ├── gmail.py
   │   │   ├── calendar.py
   │   │   └── hubspot.py
   │   ├── agents/
   │   │   ├── __init__.py
   │   │   ├── main_agent.py
   │   │   ├── subagents/
   │   │   │   ├── __init__.py
   │   │   │   ├── email_researcher.py
   │   │   │   ├── calendar_scheduler.py
   │   │   │   └── hubspot_manager.py
   │   │   └── tools/
   │   │       ├── __init__.py
   │   │       ├── gmail_tools.py
   │   │       ├── calendar_tools.py
   │   │       ├── hubspot_tools.py
   │   │       └── rag_tools.py
   │   ├── rag/
   │   │   ├── __init__.py
   │   │   ├── ingestion.py
   │   │   ├── retrieval.py
   │   │   └── embeddings.py
   │   ├── services/
   │   │   ├── __init__.py
   │   │   ├── task_manager.py
   │   │   ├── instruction_manager.py
   │   │   └── polling_service.py
   │   └── schemas/
   │       ├── __init__.py
   │       ├── auth.py
   │       ├── chat.py
   │       └── agent_state.py
   ├── alembic/
   ├── requirements.txt
   ├── .env.example
   └── README.md
   ```

3. **Database Models Setup**
   - Create SQLAlchemy models for:
     - Users (with encrypted OAuth tokens)
     - Conversations
     - Messages
     - Tasks (for multi-step workflows)
     - OngoingInstructions
     - DocumentEmbeddings (with pgvector)

4. **Configuration Management**
   - Create `.env.example` with all required environment variables
   - Set up `config.py` to load from environment

#### Deliverables
- ✅ Backend project structure
- ✅ Database models defined
- ✅ Configuration system in place

---

### Day 2: OAuth Integration

#### Tasks
1. **Google OAuth Setup**
   - Implement OAuth 2.0 flow for Google
   - Request scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.send`
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/calendar.events`
     - `https://www.googleapis.com/auth/calendar.readonly`
   - Store encrypted tokens in database
   - Implement token refresh logic

2. **HubSpot OAuth Setup**
   - Implement OAuth 2.0 flow for HubSpot
   - Request scopes:
     - `crm.objects.contacts.read`
     - `crm.objects.contacts.write`
     - `crm.schemas.contacts.read`
   - Store encrypted tokens

3. **API Endpoints**
   - `/api/auth/google/login` - Initiate Google OAuth
   - `/api/auth/google/callback` - Handle OAuth callback
   - `/api/auth/hubspot/login` - Initiate HubSpot OAuth
   - `/api/auth/hubspot/callback` - Handle OAuth callback
   - `/api/auth/status` - Check authentication status

4. **Integration Service Classes**
   - `GmailClient` - Wrapper for Gmail API
   - `CalendarClient` - Wrapper for Google Calendar API
   - `HubSpotClient` - Wrapper for HubSpot API

#### Deliverables
- ✅ OAuth flows implemented for Google and HubSpot
- ✅ Token storage with encryption
- ✅ Service classes for API interactions

---

## Phase 2: Core DeepAgents Integration (Days 3-4)

### Day 3: Custom Tools Development

#### Tasks
1. **Gmail Tools** (`app/agents/tools/gmail_tools.py`)
   ```python
   from langchain_core.tools import tool
   from typing import List, Dict, Any

   @tool
   def search_emails(
       query: str,
       max_results: int = 10,
       user_id: str = None
   ) -> List[Dict[str, Any]]:
       """Search Gmail for emails matching the query"""
       # Implementation
       pass

   @tool
   def send_email(
       to: str,
       subject: str,
       body: str,
       user_id: str = None
   ) -> Dict[str, str]:
       """Send an email via Gmail"""
       pass

   @tool
   def get_email(
       email_id: str,
       user_id: str = None
   ) -> Dict[str, Any]:
       """Get a specific email by ID"""
       pass

   @tool
   def reply_to_email(
       email_id: str,
       body: str,
       user_id: str = None
   ) -> Dict[str, str]:
       """Reply to a specific email"""
       pass
   ```

2. **Calendar Tools** (`app/agents/tools/calendar_tools.py`)
   ```python
   @tool
   def get_calendar_events(
       start_date: str,
       end_date: str,
       user_id: str = None
   ) -> List[Dict[str, Any]]:
       """Get calendar events in a date range"""
       pass

   @tool
   def create_calendar_event(
       title: str,
       start_time: str,
       end_time: str,
       attendees: List[str],
       description: str = "",
       user_id: str = None
   ) -> Dict[str, Any]:
       """Create a new calendar event"""
       pass

   @tool
   def get_free_busy(
       email: str,
       start_date: str,
       end_date: str,
       user_id: str = None
   ) -> Dict[str, List[Dict[str, str]]]:
       """Get free/busy information for a user"""
       pass
   ```

3. **HubSpot Tools** (`app/agents/tools/hubspot_tools.py`)
   ```python
   @tool
   def search_contacts(
       query: str,
       user_id: str = None
   ) -> List[Dict[str, Any]]:
       """Search HubSpot for contacts"""
       pass

   @tool
   def create_contact(
       email: str,
       properties: Dict[str, str],
       user_id: str = None
   ) -> Dict[str, Any]:
       """Create a new contact in HubSpot"""
       pass

   @tool
   def create_note(
       contact_id: str,
       note_text: str,
       user_id: str = None
   ) -> Dict[str, str]:
       """Add a note to a contact in HubSpot"""
       pass

   @tool
   def get_contact_notes(
       contact_id: str,
       user_id: str = None
   ) -> List[Dict[str, Any]]:
       """Get all notes for a contact"""
       pass
   ```

#### Deliverables
- ✅ 10+ custom tools for Gmail, Calendar, and HubSpot
- ✅ Tools integrated with service clients
- ✅ Error handling and validation

---

### Day 4: Main Agent & Subagents Setup

#### Tasks
1. **Create Subagent Definitions**
   ```python
   # app/agents/subagents/__init__.py

   email_researcher_agent = {
       "name": "email-researcher",
       "description": "Search through emails to find specific information about clients, conversations, or topics",
       "prompt": """You are an expert email researcher for a financial advisor.

       Your job is to search through email history to find relevant information about clients,
       conversations, or specific topics. Use both direct email search and RAG search to find
       the most relevant information.

       When you find relevant information, provide:
       - Summary of what you found
       - Key details (dates, names, specific facts)
       - Email IDs or threads for reference

       Be thorough but concise in your responses.""",
       "tools": ["search_emails", "get_email", "rag_search"]
   }

   calendar_scheduler_agent = {
       "name": "calendar-scheduler",
       "description": "Handle scheduling meetings, checking availability, and managing calendar events",
       "prompt": """You are a scheduling assistant for a financial advisor.

       Your job is to:
       - Check calendar availability
       - Propose meeting times
       - Create calendar events
       - Coordinate with clients via email

       When scheduling:
       1. Always check current calendar for availability
       2. Propose 3-4 time slots when possible
       3. Consider business hours (9am-5pm on weekdays)
       4. Create events only after confirmation

       Be professional and helpful in all communications.""",
       "tools": ["get_calendar_events", "create_calendar_event", "get_free_busy", "send_email"]
   }

   hubspot_manager_agent = {
       "name": "hubspot-manager",
       "description": "Manage HubSpot contacts, search CRM data, and create/update notes",
       "prompt": """You are a CRM specialist for a financial advisor.

       Your job is to:
       - Search for contacts in HubSpot
       - Create new contacts when needed
       - Add notes about interactions
       - Retrieve contact information

       When working with contacts:
       - Always search before creating to avoid duplicates
       - Include relevant details in notes (date, topic, outcome)
       - Keep contact information up to date

       Be detail-oriented and organized.""",
       "tools": ["search_contacts", "create_contact", "create_note", "get_contact_notes", "rag_search"]
   }
   ```

2. **Main Agent Setup** (`app/agents/main_agent.py`)
   ```python
   from deepagents import create_deep_agent
   from langchain.checkpoint.postgres import PostgresSaver
   from app.agents.tools.gmail_tools import *
   from app.agents.tools.calendar_tools import *
   from app.agents.tools.hubspot_tools import *
   from app.agents.tools.rag_tools import *
   from app.agents.subagents import (
       email_researcher_agent,
       calendar_scheduler_agent,
       hubspot_manager_agent
   )

   FINANCIAL_ADVISOR_INSTRUCTIONS = """You are an AI assistant for a financial advisor.

   Your role is to help manage client communications, scheduling, and CRM tasks efficiently.
   You have access to Gmail, Google Calendar, and HubSpot CRM.

   ## Key Capabilities

   1. **Answer Questions**: Use RAG search and subagents to find information from emails and CRM
      - Example: "Who mentioned their kid plays baseball?"
      - Example: "Why did Greg say he wanted to sell AAPL stock?"

   2. **Execute Tasks**: Handle multi-step workflows using tools and subagents
      - Example: "Schedule an appointment with Sara Smith"
      - Example: "Send a follow-up email to all clients I met with this week"

   3. **Proactive Actions**: Execute ongoing instructions
      - Check if any ongoing instructions apply to the current situation
      - Take appropriate actions based on those instructions

   ## Guidelines

   - Always be professional and accurate
   - Verify information before taking actions (sending emails, creating events)
   - Use subagents for complex, focused tasks (email research, scheduling, CRM)
   - Keep the user informed of progress on multi-step tasks
   - When uncertain, ask clarifying questions

   ## Available Subagents

   - **email-researcher**: For deep email searches and information retrieval
   - **calendar-scheduler**: For scheduling and calendar management
   - **hubspot-manager**: For CRM operations and contact management

   Use the `write_todos` tool for complex multi-step tasks to track progress.
   """

   def create_financial_advisor_agent(user_id: str, checkpointer):
       """Create the main financial advisor agent"""

       all_tools = [
           # Gmail tools
           search_emails, send_email, get_email, reply_to_email,
           # Calendar tools
           get_calendar_events, create_calendar_event, get_free_busy,
           # HubSpot tools
           search_contacts, create_contact, create_note, get_contact_notes,
           # RAG tools
           rag_search
       ]

       agent = create_deep_agent(
           tools=all_tools,
           instructions=FINANCIAL_ADVISOR_INSTRUCTIONS,
           subagents=[
               email_researcher_agent,
               calendar_scheduler_agent,
               hubspot_manager_agent
           ],
           checkpointer=checkpointer
       )

       return agent
   ```

#### Deliverables
- ✅ Three specialized subagents defined
- ✅ Main agent with comprehensive instructions
- ✅ Agent factory function for creating instances

---

## Phase 3: RAG System (Days 5-6)

### Day 5: Data Ingestion Pipeline

#### Tasks
1. **Embedding Service** (`app/rag/embeddings.py`)
   ```python
   from openai import OpenAI
   from typing import List

   class EmbeddingService:
       def __init__(self, api_key: str):
           self.client = OpenAI(api_key=api_key)

       def embed_text(self, text: str) -> List[float]:
           """Generate embedding for a single text"""
           response = self.client.embeddings.create(
               model="text-embedding-3-small",
               input=text
           )
           return response.data[0].embedding

       def embed_batch(self, texts: List[str]) -> List[List[float]]:
           """Generate embeddings for multiple texts"""
           response = self.client.embeddings.create(
               model="text-embedding-3-small",
               input=texts
           )
           return [item.embedding for item in response.data]
   ```

2. **Gmail Ingestion** (`app/rag/ingestion.py`)
   ```python
   async def ingest_gmail_emails(user_id: str, gmail_client, embedding_service, db):
       """Ingest all Gmail emails for a user"""

       # Fetch all emails (paginated)
       emails = []
       page_token = None

       while True:
           response = gmail_client.list_messages(max_results=500, page_token=page_token)
           emails.extend(response.get('messages', []))
           page_token = response.get('nextPageToken')
           if not page_token:
               break

       # Process in batches
       batch_size = 100
       for i in range(0, len(emails), batch_size):
           batch = emails[i:i+batch_size]

           # Get full email data
           email_data = [gmail_client.get_message(email['id']) for email in batch]

           # Create documents
           documents = []
           for email in email_data:
               # Extract content
               subject = get_header(email, 'Subject')
               sender = get_header(email, 'From')
               date = get_header(email, 'Date')
               body = extract_email_body(email)

               # Combine for embedding
               content = f"Subject: {subject}\nFrom: {sender}\nDate: {date}\n\n{body}"

               documents.append({
                   'user_id': user_id,
                   'content': content,
                   'source_type': 'email',
                   'source_id': email['id'],
                   'metadata': {
                       'subject': subject,
                       'sender': sender,
                       'date': date,
                       'thread_id': email.get('threadId')
                   }
               })

           # Generate embeddings
           texts = [doc['content'] for doc in documents]
           embeddings = embedding_service.embed_batch(texts)

           # Store in database
           for doc, embedding in zip(documents, embeddings):
               await store_document_embedding(db, doc, embedding)

   async def ingest_hubspot_data(user_id: str, hubspot_client, embedding_service, db):
       """Ingest HubSpot contacts and notes"""

       # Fetch all contacts
       contacts = hubspot_client.get_all_contacts()

       documents = []
       for contact in contacts:
           # Get contact notes
           notes = hubspot_client.get_contact_notes(contact['id'])

           # Combine contact info + notes
           content = f"""Contact: {contact.get('properties', {}).get('firstname', '')} {contact.get('properties', {}).get('lastname', '')}
   Email: {contact.get('properties', {}).get('email', '')}
   Company: {contact.get('properties', {}).get('company', '')}

   Notes:
   """
           for note in notes:
               content += f"\n- {note.get('properties', {}).get('hs_note_body', '')}"

           documents.append({
               'user_id': user_id,
               'content': content,
               'source_type': 'hubspot',
               'source_id': contact['id'],
               'metadata': {
                   'contact_name': f"{contact.get('properties', {}).get('firstname', '')} {contact.get('properties', {}).get('lastname', '')}",
                   'email': contact.get('properties', {}).get('email', ''),
                   'contact_id': contact['id']
               }
           })

       # Generate embeddings and store
       if documents:
           texts = [doc['content'] for doc in documents]
           embeddings = embedding_service.embed_batch(texts)

           for doc, embedding in zip(documents, embeddings):
               await store_document_embedding(db, doc, embedding)
   ```

3. **Initial Sync Endpoint**
   ```python
   # app/api/settings.py

   @router.post("/sync/initial")
   async def trigger_initial_sync(
       current_user: User = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       """Trigger initial data sync for all integrations"""

       # Start background task for ingestion
       background_tasks.add_task(
           run_initial_sync,
           user_id=current_user.id,
           db=db
       )

       return {"status": "sync_started"}
   ```

#### Deliverables
- ✅ Embedding service with OpenAI integration
- ✅ Gmail email ingestion
- ✅ HubSpot data ingestion
- ✅ Initial sync endpoint

---

### Day 6: Retrieval Implementation

#### Tasks
1. **Vector Search** (`app/rag/retrieval.py`)
   ```python
   from pgvector.sqlalchemy import Vector
   from sqlalchemy import select, func

   async def semantic_search(
       db,
       query: str,
       user_id: str,
       embedding_service,
       top_k: int = 5,
       source_type: str = None,
       metadata_filter: dict = None
   ) -> List[Dict]:
       """Perform semantic search over embedded documents"""

       # Generate query embedding
       query_embedding = embedding_service.embed_text(query)

       # Build query
       stmt = select(DocumentEmbedding).where(
           DocumentEmbedding.user_id == user_id
       )

       # Filter by source type if specified
       if source_type:
           stmt = stmt.where(DocumentEmbedding.source_type == source_type)

       # Add metadata filters
       if metadata_filter:
           for key, value in metadata_filter.items():
               stmt = stmt.where(
                   DocumentEmbedding.metadata[key].astext == value
               )

       # Order by cosine similarity
       stmt = stmt.order_by(
           DocumentEmbedding.embedding.cosine_distance(query_embedding)
       ).limit(top_k)

       result = await db.execute(stmt)
       documents = result.scalars().all()

       return [
           {
               'content': doc.content,
               'source_type': doc.source_type,
               'source_id': doc.source_id,
               'metadata': doc.metadata,
               'similarity': 1 - cosine_distance(query_embedding, doc.embedding)
           }
           for doc in documents
       ]
   ```

2. **RAG Tool** (`app/agents/tools/rag_tools.py`)
   ```python
   from langchain_core.tools import tool
   from langchain.tools.tool_node import InjectedState
   from typing import Annotated, List, Dict, Any

   @tool
   def rag_search(
       query: str,
       source_type: str = None,
       top_k: int = 5,
       state: Annotated[dict, InjectedState] = None
   ) -> List[Dict[str, Any]]:
       """Search across emails and HubSpot data using semantic search.

       Args:
           query: The search query (natural language)
           source_type: Optional filter - 'email' or 'hubspot'
           top_k: Number of results to return (default 5)

       Returns:
           List of relevant documents with content and metadata
       """
       user_id = state.get('user_id')
       db = state.get('db')
       embedding_service = state.get('embedding_service')

       results = semantic_search(
           db=db,
           query=query,
           user_id=user_id,
           embedding_service=embedding_service,
           top_k=top_k,
           source_type=source_type
       )

       return results
   ```

3. **Incremental Update Logic**
   ```python
   # app/rag/ingestion.py

   async def incremental_sync_gmail(user_id: str, gmail_client, embedding_service, db):
       """Sync new emails since last sync"""

       # Get last sync time
       last_sync = await get_last_sync_time(db, user_id, 'gmail')

       # Query for new emails
       query = f"after:{last_sync.strftime('%Y/%m/%d')}"
       new_emails = gmail_client.search_messages(query=query)

       # Ingest new emails (same logic as initial sync)
       ...

   async def incremental_sync_hubspot(user_id: str, hubspot_client, embedding_service, db):
       """Sync updated HubSpot contacts"""

       last_sync = await get_last_sync_time(db, user_id, 'hubspot')

       # Get recently modified contacts
       contacts = hubspot_client.get_recently_modified_contacts(since=last_sync)

       # Re-embed and update
       ...
   ```

#### Deliverables
- ✅ Semantic search with pgvector
- ✅ RAG tool for agent use
- ✅ Incremental sync logic
- ✅ Metadata filtering capabilities

---

## Phase 4: Chat Interface (Days 7-8)

### Day 7: Frontend Setup & Basic Chat UI

#### Tasks
1. **Initialize Next.js Project**
   ```bash
   cd frontend
   npx create-next-app@latest . --typescript --tailwind --app
   npm install @tanstack/react-query axios eventsource-parser
   npm install lucide-react class-variance-authority clsx tailwind-merge
   ```

2. **Project Structure**
   ```
   frontend/
   ├── app/
   │   ├── (auth)/
   │   │   └── login/
   │   │       └── page.tsx
   │   ├── (app)/
   │   │   ├── layout.tsx
   │   │   ├── chat/
   │   │   │   └── page.tsx
   │   │   └── settings/
   │   │       └── page.tsx
   │   ├── api/
   │   │   └── proxy/
   │   │       └── [...path]/route.ts
   │   └── layout.tsx
   ├── components/
   │   ├── ui/
   │   │   ├── button.tsx
   │   │   ├── input.tsx
   │   │   └── card.tsx
   │   ├── chat/
   │   │   ├── ChatInterface.tsx
   │   │   ├── MessageList.tsx
   │   │   ├── MessageBubble.tsx
   │   │   ├── InputArea.tsx
   │   │   └── ContextSelector.tsx
   │   ├── layout/
   │   │   ├── Sidebar.tsx
   │   │   └── Header.tsx
   │   └── auth/
   │       └── OAuthButton.tsx
   ├── lib/
   │   ├── api.ts
   │   ├── auth.ts
   │   └── utils.ts
   ├── hooks/
   │   ├── useChat.ts
   │   └── useAuth.ts
   └── types/
       ├── chat.ts
       └── auth.ts
   ```

3. **Basic Chat Interface Component**
   ```tsx
   // components/chat/ChatInterface.tsx
   'use client';

   import { useState } from 'react';
   import { MessageList } from './MessageList';
   import { InputArea } from './InputArea';
   import { ContextSelector } from './ContextSelector';

   export function ChatInterface() {
     const [messages, setMessages] = useState([]);
     const [context, setContext] = useState('all');
     const [isLoading, setIsLoading] = useState(false);

     const handleSendMessage = async (content: string) => {
       // Add user message
       const userMessage = {
         id: Date.now().toString(),
         role: 'user',
         content,
         timestamp: new Date()
       };
       setMessages(prev => [...prev, userMessage]);
       setIsLoading(true);

       // Stream response from backend
       try {
         const response = await fetch('/api/chat/stream', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
             message: content,
             context: context,
             conversation_id: conversationId
           })
         });

         const reader = response.body?.getReader();
         const decoder = new TextDecoder();

         let assistantMessage = {
           id: (Date.now() + 1).toString(),
           role: 'assistant',
           content: '',
           timestamp: new Date()
         };

         setMessages(prev => [...prev, assistantMessage]);

         while (true) {
           const { done, value } = await reader!.read();
           if (done) break;

           const chunk = decoder.decode(value);
           const lines = chunk.split('\n');

           for (const line of lines) {
             if (line.startsWith('data: ')) {
               const data = JSON.parse(line.slice(6));
               assistantMessage.content += data.content;
               setMessages(prev => {
                 const updated = [...prev];
                 updated[updated.length - 1] = { ...assistantMessage };
                 return updated;
               });
             }
           }
         }
       } catch (error) {
         console.error('Chat error:', error);
       } finally {
         setIsLoading(false);
       }
     };

     return (
       <div className="flex flex-col h-screen">
         <div className="border-b p-4 flex items-center justify-between">
           <div className="flex items-center gap-4">
             <h1 className="text-xl font-semibold">Ask Anything</h1>
             <ContextSelector value={context} onChange={setContext} />
           </div>
         </div>

         <MessageList messages={messages} />

         <InputArea
           onSend={handleSendMessage}
           disabled={isLoading}
         />
       </div>
     );
   }
   ```

4. **Message Components**
   ```tsx
   // components/chat/MessageBubble.tsx
   export function MessageBubble({ message }) {
     const isUser = message.role === 'user';

     return (
       <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
         <div className={`max-w-[70%] rounded-lg p-4 ${
           isUser
             ? 'bg-blue-600 text-white'
             : 'bg-gray-100 text-gray-900'
         }`}>
           <div className="prose prose-sm">
             {message.content}
           </div>
         </div>
       </div>
     );
   }
   ```

#### Deliverables
- ✅ Next.js project initialized
- ✅ Basic chat interface layout
- ✅ Message display components
- ✅ Streaming message support

---

### Day 8: API Integration & Rich Messages

#### Tasks
1. **Chat API Endpoint** (`backend/app/api/chat.py`)
   ```python
   from fastapi import APIRouter, Depends
   from fastapi.responses import StreamingResponse
   from app.agents.main_agent import create_financial_advisor_agent

   router = APIRouter()

   @router.post("/chat/stream")
   async def chat_stream(
       request: ChatRequest,
       current_user: User = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       """Stream chat responses from the agent"""

       async def generate():
           # Get or create conversation
           conversation = get_or_create_conversation(
               db, current_user.id, request.conversation_id
           )

           # Create agent
           checkpointer = PostgresSaver(db_conn)
           agent = create_financial_advisor_agent(
               user_id=current_user.id,
               checkpointer=checkpointer
           )

           # Prepare state
           config = {"configurable": {"thread_id": conversation.id}}
           state = {
               "messages": [{"role": "user", "content": request.message}],
               "user_id": current_user.id,
               "db": db,
               "embedding_service": embedding_service
           }

           # Stream response
           async for chunk in agent.astream(state, config=config, stream_mode="values"):
               if "messages" in chunk:
                   last_message = chunk["messages"][-1]
                   if last_message.type == "ai":
                       yield f"data: {json.dumps({'content': last_message.content})}\n\n"

           yield "data: [DONE]\n\n"

       return StreamingResponse(generate(), media_type="text/event-stream")
   ```

2. **Rich Message Components**
   ```tsx
   // components/chat/CalendarEventCard.tsx
   export function CalendarEventCard({ event }) {
     return (
       <div className="border rounded-lg p-4 bg-white shadow-sm">
         <div className="flex items-start justify-between">
           <div>
             <h3 className="font-semibold text-lg">{event.title}</h3>
             <p className="text-sm text-gray-600 mt-1">
               {formatDateTime(event.start)} - {formatTime(event.end)}
             </p>
           </div>
           <CalendarIcon className="w-5 h-5 text-blue-600" />
         </div>

         {event.attendees && event.attendees.length > 0 && (
           <div className="mt-3 flex items-center gap-2">
             <Users className="w-4 h-4 text-gray-400" />
             <div className="flex -space-x-2">
               {event.attendees.map((attendee, i) => (
                 <div key={i} className="w-8 h-8 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs">
                   {attendee.name[0]}
                 </div>
               ))}
             </div>
           </div>
         )}
       </div>
     );
   }

   // components/chat/ContactCard.tsx
   export function ContactCard({ contact }) {
     return (
       <div className="border rounded-lg p-4 bg-white shadow-sm">
         <div className="flex items-center gap-3">
           <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
             <User className="w-5 h-5 text-blue-600" />
           </div>
           <div>
             <h3 className="font-semibold">{contact.name}</h3>
             <p className="text-sm text-gray-600">{contact.email}</p>
             {contact.company && (
               <p className="text-sm text-gray-500">{contact.company}</p>
             )}
           </div>
         </div>
       </div>
     );
   }
   ```

3. **Context Selector**
   ```tsx
   // components/chat/ContextSelector.tsx
   export function ContextSelector({ value, onChange }) {
     const contexts = [
       { value: 'all', label: 'All data', icon: Database },
       { value: 'emails', label: 'Emails only', icon: Mail },
       { value: 'calendar', label: 'Calendar only', icon: Calendar },
       { value: 'hubspot', label: 'HubSpot only', icon: Users },
     ];

     return (
       <div className="relative">
         <button className="flex items-center gap-2 px-3 py-1.5 border rounded-md text-sm hover:bg-gray-50">
           <Filter className="w-4 h-4" />
           Context: {contexts.find(c => c.value === value)?.label}
           <ChevronDown className="w-4 h-4" />
         </button>

         {/* Dropdown menu */}
       </div>
     );
   }
   ```

#### Deliverables
- ✅ Streaming chat API endpoint
- ✅ Rich message components (calendar, contacts)
- ✅ Context selector for filtering
- ✅ Message persistence

---

## Phase 5: Task Persistence & Memory (Days 9-10)

### Day 9: Task Management System

#### Tasks
1. **Task Manager Service** (`app/services/task_manager.py`)
   ```python
   from sqlalchemy.orm import Session
   from app.models.task import Task, TaskStatus
   from typing import Dict, Any, List

   class TaskManager:
       def __init__(self, db: Session):
           self.db = db

       def create_task(
           self,
           user_id: str,
           description: str,
           context: Dict[str, Any]
       ) -> Task:
           """Create a new task"""
           task = Task(
               user_id=user_id,
               description=description,
               status=TaskStatus.PENDING,
               context=context
           )
           self.db.add(task)
           self.db.commit()
           return task

       def update_task_status(
           self,
           task_id: str,
           status: TaskStatus,
           context: Dict[str, Any] = None
       ):
           """Update task status and optionally context"""
           task = self.db.query(Task).filter(Task.id == task_id).first()
           if task:
               task.status = status
               if context:
                   task.context = {**task.context, **context}
               self.db.commit()

       def get_waiting_tasks(self, user_id: str) -> List[Task]:
           """Get all tasks waiting for external events"""
           return self.db.query(Task).filter(
               Task.user_id == user_id,
               Task.status == TaskStatus.WAITING
           ).all()

       def find_task_for_email(
           self,
           user_id: str,
           email_from: str,
           email_subject: str
       ) -> Task:
           """Find a task waiting for an email from specific sender"""
           tasks = self.get_waiting_tasks(user_id)

           for task in tasks:
               if task.context.get('waiting_for') == 'email_reply':
                   expected_from = task.context.get('expected_from', '').lower()
                   if expected_from in email_from.lower():
                       return task

           return None
   ```

2. **Agent Task Tools** (`app/agents/tools/task_tools.py`)
   ```python
   from langchain_core.tools import tool
   from langchain.tools.tool_node import InjectedState
   from typing import Annotated, Dict, Any

   @tool
   def create_waiting_task(
       description: str,
       waiting_for: str,
       expected_from: str = None,
       context: Dict[str, Any] = None,
       state: Annotated[dict, InjectedState] = None
   ) -> Dict[str, str]:
       """Create a task that waits for an external event.

       Args:
           description: What this task is about
           waiting_for: What we're waiting for ('email_reply', 'calendar_response', etc.)
           expected_from: Email address we're expecting response from
           context: Additional context to store with the task

       Returns:
           Task ID and status
       """
       task_manager = state.get('task_manager')
       user_id = state.get('user_id')

       task_context = {
           'waiting_for': waiting_for,
           'expected_from': expected_from,
           **(context or {})
       }

       task = task_manager.create_task(
           user_id=user_id,
           description=description,
           context=task_context
       )

       return {
           'task_id': task.id,
           'status': 'created',
           'message': f'Task created and waiting for {waiting_for}'
       }
   ```

3. **Task Resumption Logic**
   ```python
   # app/services/task_manager.py

   async def resume_task(
       task: Task,
       event_data: Dict[str, Any],
       agent,
       db: Session
   ):
       """Resume a waiting task with new event data"""

       # Update task status
       task.status = TaskStatus.IN_PROGRESS
       db.commit()

       # Prepare state for agent
       config = {"configurable": {"thread_id": task.context.get('conversation_id')}}

       # Create continuation message
       continuation_message = f"""
       Continuing task: {task.description}

       New event received:
       {json.dumps(event_data, indent=2)}

       Previous context:
       {json.dumps(task.context, indent=2)}

       Please continue with the appropriate next step.
       """

       state = {
           "messages": [{"role": "user", "content": continuation_message}],
           "user_id": task.user_id,
           "task_id": task.id,
           "db": db
       }

       # Run agent
       result = await agent.ainvoke(state, config=config)

       # Check if task is complete
       if is_task_complete(result):
           task.status = TaskStatus.COMPLETED
       else:
           task.status = TaskStatus.WAITING

       db.commit()

       return result
   ```

#### Deliverables
- ✅ Task management service
- ✅ Task creation/update tools for agent
- ✅ Task resumption logic
- ✅ Database persistence for tasks

---

### Day 10: Ongoing Instructions & Polling Service

#### Tasks
1. **Instruction Manager** (`app/services/instruction_manager.py`)
   ```python
   class InstructionManager:
       def __init__(self, db: Session):
           self.db = db

       def add_instruction(self, user_id: str, instruction: str):
           """Add an ongoing instruction"""
           inst = OngoingInstruction(
               user_id=user_id,
               instruction=instruction,
               active=True
           )
           self.db.add(inst)
           self.db.commit()
           return inst

       def get_active_instructions(self, user_id: str) -> List[str]:
           """Get all active instructions for a user"""
           instructions = self.db.query(OngoingInstruction).filter(
               OngoingInstruction.user_id == user_id,
               OngoingInstruction.active == True
           ).all()

           return [inst.instruction for inst in instructions]

       def deactivate_instruction(self, instruction_id: str):
           """Deactivate an instruction"""
           inst = self.db.query(OngoingInstruction).filter(
               OngoingInstruction.id == instruction_id
           ).first()
           if inst:
               inst.active = False
               self.db.commit()
   ```

2. **Polling Service** (`app/services/polling_service.py`)
   ```python
   from apscheduler.schedulers.asyncio import AsyncIOScheduler
   from datetime import datetime, timedelta

   class PollingService:
       def __init__(self, db, agent_factory):
           self.db = db
           self.agent_factory = agent_factory
           self.scheduler = AsyncIOScheduler()

       async def poll_gmail(self, user_id: str):
           """Poll Gmail for new emails"""
           user = get_user(self.db, user_id)
           gmail_client = GmailClient(user.google_token)

           # Get emails from last 5 minutes
           since = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y/%m/%d %H:%M')
           query = f"after:{since}"

           new_emails = gmail_client.search_messages(query=query)

           for email in new_emails:
               await self.process_new_email(user_id, email)

       async def process_new_email(self, user_id: str, email: Dict):
           """Process a new email - check tasks and ongoing instructions"""

           # Check if any task is waiting for this email
           task_manager = TaskManager(self.db)
           task = task_manager.find_task_for_email(
               user_id=user_id,
               email_from=email['from'],
               email_subject=email['subject']
           )

           if task:
               # Resume the task
               agent = self.agent_factory(user_id)
               await resume_task(task, email, agent, self.db)
               return

           # Check ongoing instructions
           instruction_manager = InstructionManager(self.db)
           instructions = instruction_manager.get_active_instructions(user_id)

           if instructions:
               # Ask agent if any instruction applies
               await self.evaluate_instructions(user_id, email, instructions)

       async def evaluate_instructions(
           self,
           user_id: str,
           email: Dict,
           instructions: List[str]
       ):
           """Let agent decide if any instruction applies to this email"""

           agent = self.agent_factory(user_id)

           prompt = f"""
           New email received:
           From: {email['from']}
           Subject: {email['subject']}

           Active ongoing instructions:
           {chr(10).join(f'- {inst}' for inst in instructions)}

           Do any of these instructions apply to this email?
           If yes, execute the appropriate action.
           If no, respond with "NO_ACTION_NEEDED".
           """

           result = await agent.ainvoke({
               "messages": [{"role": "user", "content": prompt}],
               "user_id": user_id
           })

           # Agent will use tools to take action if needed

       def start(self):
           """Start polling scheduler"""
           # Poll every 2 minutes for all active users
           self.scheduler.add_job(
               self.poll_all_users,
               'interval',
               minutes=2
           )
           self.scheduler.start()

       async def poll_all_users(self):
           """Poll for all active users"""
           users = get_active_users(self.db)
           for user in users:
               try:
                   await self.poll_gmail(user.id)
                   # Also poll Calendar and HubSpot
               except Exception as e:
                   logger.error(f"Error polling for user {user.id}: {e}")
   ```

3. **Instruction Management API**
   ```python
   # app/api/settings.py

   @router.get("/instructions")
   async def get_instructions(
       current_user: User = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       """Get all ongoing instructions"""
       manager = InstructionManager(db)
       instructions = manager.get_active_instructions(current_user.id)
       return {"instructions": instructions}

   @router.post("/instructions")
   async def add_instruction(
       request: AddInstructionRequest,
       current_user: User = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       """Add a new ongoing instruction"""
       manager = InstructionManager(db)
       inst = manager.add_instruction(current_user.id, request.instruction)
       return {"instruction_id": inst.id, "status": "added"}
   ```

#### Deliverables
- ✅ Instruction management service
- ✅ Polling service for Gmail/Calendar/HubSpot
- ✅ Task resumption on incoming events
- ✅ Proactive instruction evaluation

---

## Phase 6: Testing & Refinement (Days 11-12)

### Day 11: Core Workflow Testing

#### Tasks
1. **Test RAG Queries**
   - "Who mentioned their kid plays baseball?"
   - "Why did Greg say he wanted to sell AAPL stock?"
   - Verify semantic search returns relevant results
   - Test with various email and CRM data

2. **Test Multi-Step Tasks**
   - "Schedule an appointment with Sara Smith"
     - Verify: searches HubSpot/emails
     - Verify: checks calendar availability
     - Verify: sends email with time options
     - Verify: creates waiting task
     - Manually send reply and verify task resumes
   - "Send a follow-up to everyone I met with this week"
     - Verify: queries calendar
     - Verify: composes emails
     - Verify: sends to correct recipients

3. **Test Ongoing Instructions**
   - Add instruction: "When someone emails me not in HubSpot, create a contact"
   - Send test email from new address
   - Wait for polling cycle
   - Verify contact created in HubSpot
   - Verify note added about email

4. **Test Subagents**
   - Verify email-researcher subagent properly searches
   - Verify calendar-scheduler handles scheduling
   - Verify hubspot-manager manages CRM correctly

#### Test Checklist
- [ ] OAuth flows work for Google and HubSpot
- [ ] Initial data sync completes successfully
- [ ] Incremental sync updates new data
- [ ] RAG search returns relevant results
- [ ] Chat interface displays messages correctly
- [ ] Streaming responses work
- [ ] Multi-step tasks create and resume correctly
- [ ] Ongoing instructions are evaluated
- [ ] Polling service runs without errors
- [ ] Error handling works gracefully

---

### Day 12: Polish & Documentation

#### Tasks
1. **Error Handling**
   - Add try-catch blocks for all API calls
   - Implement retry logic for transient failures
   - Add user-friendly error messages
   - Log errors for debugging

2. **OAuth Token Refresh**
   - Implement automatic token refresh
   - Handle expired token errors
   - Prompt user to re-authenticate if needed

3. **UI Polish**
   - Loading states for all async operations
   - Empty states (no messages, no conversations)
   - Responsive design for mobile
   - Accessibility improvements

4. **Environment Setup Documentation**
   - Create `.env.example` with all variables
   - Document each configuration option
   - Add setup instructions to README

5. **Deployment Preparation**
   - Dockerfiles for backend and frontend
   - docker-compose.yml for local development
   - Environment-specific configurations
   - Database migration scripts

#### Deliverables
- ✅ Comprehensive error handling
- ✅ Polished UI with loading/empty states
- ✅ Complete documentation
- ✅ Deployment-ready code

---

## Success Criteria

The MVP is complete when:

1. ✅ User can authenticate with Google (Gmail + Calendar) and HubSpot
2. ✅ Chat interface works with streaming responses
3. ✅ RAG queries return accurate results from emails and HubSpot
4. ✅ Agent can execute multi-step tasks (e.g., scheduling meetings)
5. ✅ Tasks persist and resume when events occur
6. ✅ Ongoing instructions are stored and evaluated
7. ✅ Polling service monitors for new emails/events
8. ✅ All core workflows tested and working
9. ✅ Documentation complete for setup and deployment
10. ✅ Application is deployment-ready

---

## Next Steps After MVP

After completing the MVP, consider these enhancements:

1. **Real-time Webhooks** - Replace polling with webhooks for instant notifications
2. **Advanced Proactive Behaviors** - More sophisticated instruction matching
3. **Email Templates** - Reusable templates for common emails
4. **Analytics Dashboard** - Track agent usage and effectiveness
5. **Mobile App** - Native iOS/Android applications
6. **Voice Interface** - Voice commands and responses
7. **Multi-language Support** - Support for languages beyond English
8. **Team Features** - Shared agents for teams
9. **Advanced Calendar Features** - Recurring meetings, timezone handling
10. **CRM Workflow Automation** - Deal tracking, pipeline management

See [FULL_IMPLEMENTATION.md](./FULL_IMPLEMENTATION.md) for details on these advanced features.
