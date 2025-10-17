# Financial Advisor AI Agent - Full Implementation Guide

## Overview

This document outlines the complete system architecture for the Financial Advisor AI Agent, including advanced features beyond the MVP. This serves as a reference for building a production-grade, enterprise-ready solution.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web App    │  │  Mobile App  │  │  Voice UI    │          │
│  │  (Next.js)   │  │ (React Native│  │   (Alexa/    │          │
│  │              │  │  /Flutter)   │  │   Google)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Gateway     │
                    │  (Load Balancer)  │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FastAPI Application Server                   │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │  Auth API  │  │  Chat API  │  │ Admin API  │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       Agent Layer                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         DeepAgents Framework (LangChain)                  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │    Main    │  │   Email    │  │  Calendar  │         │   │
│  │  │   Agent    │  │ Researcher │  │ Scheduler  │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │  HubSpot   │  │   Task     │  │  Analytics │         │   │
│  │  │  Manager   │  │  Executor  │  │   Agent    │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     RAG      │  │     Task     │  │  Webhook     │          │
│  │   Service    │  │   Manager    │  │   Handler    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Instruction  │  │   Analytics  │  │  Email Queue │          │
│  │   Manager    │  │   Service    │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Gmail     │  │   Calendar   │  │   HubSpot    │          │
│  │     API      │  │     API      │  │     API      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Outlook    │  │    Slack     │  │  Salesforce  │          │
│  │     API      │  │     API      │  │     API      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │     Redis    │  │   S3/Blob    │          │
│  │  (pgvector)  │  │    (Cache)   │  │   Storage    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │  Elasticsearch│  │  ClickHouse  │                            │
│  │  (Search)    │  │  (Analytics) │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Anthropic  │  │    OpenAI    │  │   Pub/Sub    │          │
│  │    Claude    │  │  Embeddings  │  │  (Webhooks)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Sentry     │  │  DataDog     │  │   Auth0      │          │
│  │  (Monitoring)│  │  (Logging)   │  │    (SSO)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Advanced Features

### 1. Real-Time Webhook System

#### Gmail Webhooks (Google Pub/Sub)

**Setup:**
```python
# app/integrations/gmail_webhooks.py
from google.cloud import pubsub_v1
from google.oauth2 import service_account

class GmailWebhookManager:
    def __init__(self, project_id: str, credentials_path: str):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
        self.project_id = project_id

    def watch_mailbox(self, user_id: str, gmail_token: dict):
        """Set up Gmail push notifications"""
        gmail_client = GmailClient(gmail_token)

        request = {
            'labelIds': ['INBOX'],
            'topicName': f'projects/{self.project_id}/topics/gmail-notifications'
        }

        gmail_client.users().watch(userId='me', body=request).execute()

    def handle_notification(self, message: dict):
        """Handle incoming Gmail notification"""
        # Decode message
        email_address = message.get('emailAddress')
        history_id = message.get('historyId')

        # Process new emails
        user = get_user_by_email(email_address)
        gmail_client = GmailClient(user.google_token)

        # Get changes since last history_id
        history = gmail_client.users().history().list(
            userId='me',
            startHistoryId=user.last_history_id
        ).execute()

        for change in history.get('history', []):
            if 'messagesAdded' in change:
                for msg_added in change['messagesAdded']:
                    await process_new_email(user.id, msg_added['message'])

        # Update last history ID
        user.last_history_id = history_id
        db.commit()
```

**Webhook Endpoint:**
```python
# app/api/webhooks.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhooks/gmail")
async def gmail_webhook(request: Request):
    """Receive Gmail push notifications"""

    # Verify webhook authenticity
    # Google sends Pub/Sub messages with specific headers

    message = await request.json()
    message_data = base64.b64decode(message['message']['data'])
    notification = json.loads(message_data)

    # Process notification
    await webhook_manager.handle_gmail_notification(notification)

    return {"status": "processed"}
```

#### HubSpot Webhooks

**Setup:**
```python
# app/integrations/hubspot_webhooks.py

class HubSpotWebhookManager:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret

    def verify_signature(self, request_body: str, signature: str) -> bool:
        """Verify HubSpot webhook signature"""
        computed_signature = hmac.new(
            self.app_secret.encode(),
            request_body.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(computed_signature, signature)

    async def handle_contact_update(self, event: dict):
        """Handle contact update event"""
        user_id = event.get('userId')  # Map portal ID to user
        contact_id = event.get('objectId')

        # Re-embed contact data
        await incremental_sync_hubspot_contact(user_id, contact_id)

        # Check if any ongoing instruction applies
        await evaluate_hubspot_event(user_id, event)
```

**Webhook Endpoint:**
```python
@router.post("/webhooks/hubspot")
async def hubspot_webhook(request: Request):
    """Receive HubSpot webhooks"""

    body = await request.body()
    signature = request.headers.get('X-HubSpot-Signature')

    # Verify signature
    if not webhook_manager.verify_hubspot_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    events = json.loads(body)

    for event in events:
        if event['subscriptionType'] == 'contact.creation':
            await webhook_manager.handle_contact_creation(event)
        elif event['subscriptionType'] == 'contact.propertyChange':
            await webhook_manager.handle_contact_update(event)

    return {"status": "processed"}
```

#### Calendar Webhooks

**Setup:**
```python
# app/integrations/calendar_webhooks.py

class CalendarWebhookManager:
    def setup_watch(self, user_id: str, calendar_token: dict):
        """Set up Calendar push notifications"""
        calendar_client = CalendarClient(calendar_token)

        request_body = {
            'id': f'calendar-watch-{user_id}',
            'type': 'web_hook',
            'address': f'{WEBHOOK_BASE_URL}/webhooks/calendar',
            'expiration': int((datetime.utcnow() + timedelta(days=7)).timestamp() * 1000)
        }

        calendar_client.events().watch(
            calendarId='primary',
            body=request_body
        ).execute()
```

---

### 2. Advanced Proactive Behaviors

#### Intelligent Instruction Matching

```python
# app/services/proactive_agent.py

class ProactiveAgent:
    def __init__(self, agent, db):
        self.agent = agent
        self.db = db

    async def evaluate_event(
        self,
        user_id: str,
        event_type: str,
        event_data: dict
    ):
        """Evaluate if proactive action is needed for an event"""

        # Get ongoing instructions
        instructions = get_active_instructions(self.db, user_id)

        if not instructions:
            return

        # Create evaluation prompt
        prompt = f"""
        Event Type: {event_type}
        Event Data:
        {json.dumps(event_data, indent=2)}

        Active Instructions:
        {chr(10).join(f'{i+1}. {inst}' for i, inst in enumerate(instructions))}

        Analyze this event and determine if any of the instructions apply.
        If yes, execute the appropriate action(s).
        If multiple instructions apply, execute all of them.
        If no instructions apply, respond with "NO_ACTION_NEEDED".

        You have access to all your normal tools (email, calendar, HubSpot, etc.).
        """

        # Run agent
        result = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": prompt}],
            "user_id": user_id,
            "event_type": event_type,
            "event_data": event_data
        })

        # Log proactive action if taken
        if result['messages'][-1].content != "NO_ACTION_NEEDED":
            log_proactive_action(
                self.db,
                user_id=user_id,
                event_type=event_type,
                action_taken=result['messages'][-1].content
            )

        return result
```

#### Scheduled Proactive Tasks

```python
# app/services/scheduled_tasks.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class ScheduledTaskService:
    def __init__(self, agent_factory, db):
        self.agent_factory = agent_factory
        self.db = db
        self.scheduler = AsyncIOScheduler()

    def schedule_daily_summary(self, user_id: str, time_str: str):
        """Schedule daily summary email"""

        hour, minute = map(int, time_str.split(':'))

        self.scheduler.add_job(
            self.send_daily_summary,
            'cron',
            hour=hour,
            minute=minute,
            args=[user_id]
        )

    async def send_daily_summary(self, user_id: str):
        """Generate and send daily summary"""

        agent = self.agent_factory(user_id)

        prompt = """
        Please prepare a daily summary for the user including:
        1. Meetings scheduled for today
        2. Important emails received today
        3. Pending tasks and follow-ups
        4. Any ongoing instructions that need attention

        Send this summary via email to the user.
        """

        await agent.ainvoke({
            "messages": [{"role": "user", "content": prompt}],
            "user_id": user_id
        })

    def schedule_meeting_reminder(
        self,
        user_id: str,
        event_id: str,
        minutes_before: int
    ):
        """Schedule meeting reminder"""

        event = get_calendar_event(user_id, event_id)
        reminder_time = event.start_time - timedelta(minutes=minutes_before)

        self.scheduler.add_job(
            self.send_meeting_reminder,
            'date',
            run_date=reminder_time,
            args=[user_id, event_id]
        )
```

---

### 3. Multi-User & Team Features

#### Team Workspaces

```python
# app/models/team.py

class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role = Column(String)  # 'admin', 'member', 'viewer'

class SharedInstruction(Base):
    __tablename__ = "shared_instructions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))
    instruction = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    active = Column(Boolean, default=True)
```

#### Shared Context & Knowledge

```python
# app/services/team_service.py

class TeamService:
    def share_contact_with_team(
        self,
        contact_id: str,
        team_id: str,
        shared_by: str
    ):
        """Share a HubSpot contact with team"""

        # Get contact data
        contact = get_hubspot_contact(contact_id)

        # Create shared knowledge entry
        shared_knowledge = TeamKnowledge(
            team_id=team_id,
            type='contact',
            data=contact,
            shared_by=shared_by
        )

        self.db.add(shared_knowledge)
        self.db.commit()

        # Embed for all team members
        team_members = get_team_members(team_id)
        for member in team_members:
            embed_shared_knowledge(member.user_id, shared_knowledge)

    def get_team_context(self, team_id: str) -> str:
        """Get shared context for team"""

        knowledge = self.db.query(TeamKnowledge).filter(
            TeamKnowledge.team_id == team_id
        ).all()

        context = "Shared Team Knowledge:\n\n"
        for item in knowledge:
            context += f"- {item.type}: {item.data['summary']}\n"

        return context
```

---

### 4. Analytics & Insights

#### Usage Analytics

```python
# app/models/analytics.py

class AgentInteraction(Base):
    __tablename__ = "agent_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'))
    query_type = Column(String)  # 'rag_query', 'task_execution', 'proactive'
    tools_used = Column(JSON)
    tokens_used = Column(Integer)
    latency_ms = Column(Integer)
    success = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

class ToolUsageMetric(Base):
    __tablename__ = "tool_usage_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    tool_name = Column(String)
    execution_time_ms = Column(Integer)
    success = Column(Boolean)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Analytics Service

```python
# app/services/analytics_service.py

class AnalyticsService:
    def track_interaction(
        self,
        user_id: str,
        conversation_id: str,
        query_type: str,
        tools_used: List[str],
        tokens_used: int,
        latency_ms: int,
        success: bool
    ):
        """Track an agent interaction"""

        interaction = AgentInteraction(
            user_id=user_id,
            conversation_id=conversation_id,
            query_type=query_type,
            tools_used=tools_used,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
            success=success
        )

        self.db.add(interaction)
        self.db.commit()

    def get_usage_stats(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get usage statistics for a user"""

        interactions = self.db.query(AgentInteraction).filter(
            AgentInteraction.user_id == user_id,
            AgentInteraction.created_at >= start_date,
            AgentInteraction.created_at <= end_date
        ).all()

        return {
            'total_interactions': len(interactions),
            'total_tokens': sum(i.tokens_used for i in interactions),
            'avg_latency_ms': sum(i.latency_ms for i in interactions) / len(interactions) if interactions else 0,
            'success_rate': sum(1 for i in interactions if i.success) / len(interactions) if interactions else 0,
            'most_used_tools': self.get_most_used_tools(interactions),
            'query_type_breakdown': self.get_query_type_breakdown(interactions)
        }
```

#### Analytics Dashboard UI

```tsx
// components/analytics/UsageDashboard.tsx
export function UsageDashboard() {
  const { data: stats } = useQuery(['usage-stats'], fetchUsageStats);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatsCard
        title="Total Queries"
        value={stats.total_interactions}
        icon={MessageSquare}
      />
      <StatsCard
        title="Tokens Used"
        value={formatNumber(stats.total_tokens)}
        icon={Zap}
      />
      <StatsCard
        title="Avg Response Time"
        value={`${stats.avg_latency_ms}ms`}
        icon={Clock}
      />
      <StatsCard
        title="Success Rate"
        value={`${(stats.success_rate * 100).toFixed(1)}%`}
        icon={CheckCircle}
      />

      <div className="col-span-2">
        <Card>
          <CardHeader>
            <CardTitle>Query Types</CardTitle>
          </CardHeader>
          <CardContent>
            <PieChart data={stats.query_type_breakdown} />
          </CardContent>
        </Card>
      </div>

      <div className="col-span-2">
        <Card>
          <CardHeader>
            <CardTitle>Most Used Tools</CardTitle>
          </CardHeader>
          <CardContent>
            <BarChart data={stats.most_used_tools} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

---

### 5. Advanced RAG Features

#### Hybrid Search (Semantic + Keyword)

```python
# app/rag/hybrid_search.py

class HybridSearchService:
    def __init__(self, db, embedding_service, elasticsearch_client):
        self.db = db
        self.embedding_service = embedding_service
        self.es = elasticsearch_client

    async def hybrid_search(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        semantic_weight: float = 0.7
    ) -> List[Dict]:
        """Combine semantic and keyword search"""

        # Semantic search with pgvector
        semantic_results = await self.semantic_search(
            query=query,
            user_id=user_id,
            top_k=top_k * 2
        )

        # Keyword search with Elasticsearch
        keyword_results = await self.keyword_search(
            query=query,
            user_id=user_id,
            top_k=top_k * 2
        )

        # Merge and rerank results
        merged = self.rerank_results(
            semantic_results=semantic_results,
            keyword_results=keyword_results,
            semantic_weight=semantic_weight,
            keyword_weight=1 - semantic_weight,
            top_k=top_k
        )

        return merged

    async def keyword_search(
        self,
        query: str,
        user_id: str,
        top_k: int
    ) -> List[Dict]:
        """Elasticsearch keyword search"""

        es_query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": query}},
                        {"term": {"user_id": user_id}}
                    ]
                }
            },
            "size": top_k
        }

        results = self.es.search(index="documents", body=es_query)

        return [
            {
                'content': hit['_source']['content'],
                'source_type': hit['_source']['source_type'],
                'source_id': hit['_source']['source_id'],
                'metadata': hit['_source']['metadata'],
                'score': hit['_score']
            }
            for hit in results['hits']['hits']
        ]
```

#### Contextual Compression

```python
# app/rag/contextual_compression.py
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

class CompressedRetrieval:
    def __init__(self, base_retriever, llm):
        self.compressor = LLMChainExtractor.from_llm(llm)
        self.retriever = ContextualCompressionRetriever(
            base_compressor=self.compressor,
            base_retriever=base_retriever
        )

    async def retrieve_compressed(
        self,
        query: str
    ) -> List[Document]:
        """Retrieve and compress documents relevant to query"""

        # Get relevant docs
        docs = await self.retriever.aget_relevant_documents(query)

        return docs
```

#### Reranking with Cross-Encoder

```python
# app/rag/reranking.py
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_k: int
    ) -> List[Dict]:
        """Rerank documents using cross-encoder"""

        # Prepare pairs
        pairs = [[query, doc['content']] for doc in documents]

        # Get scores
        scores = self.model.predict(pairs)

        # Combine scores with documents
        for doc, score in zip(documents, scores):
            doc['rerank_score'] = float(score)

        # Sort and return top-k
        ranked = sorted(documents, key=lambda x: x['rerank_score'], reverse=True)
        return ranked[:top_k]
```

---

### 6. Security & Compliance

#### Data Encryption

```python
# app/security/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

class EncryptionService:
    def __init__(self, master_key: str):
        # Derive encryption key from master key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'static_salt',  # Use per-user salt in production
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.cipher = Fernet(key)

    def encrypt_token(self, token: dict) -> str:
        """Encrypt OAuth token"""
        token_json = json.dumps(token)
        encrypted = self.cipher.encrypt(token_json.encode())
        return encrypted.decode()

    def decrypt_token(self, encrypted_token: str) -> dict:
        """Decrypt OAuth token"""
        decrypted = self.cipher.decrypt(encrypted_token.encode())
        return json.loads(decrypted.decode())
```

#### Audit Logging

```python
# app/models/audit.py

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    action = Column(String)  # 'email_sent', 'contact_created', 'calendar_event_created'
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# app/services/audit_service.py

class AuditService:
    def log_action(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: dict,
        request: Request
    ):
        """Log an auditable action"""

        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.client.host,
            user_agent=request.headers.get('user-agent')
        )

        self.db.add(audit_entry)
        self.db.commit()
```

#### GDPR Compliance

```python
# app/api/privacy.py

@router.post("/privacy/export")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export all user data (GDPR compliance)"""

    data = {
        'user_info': get_user_info(current_user),
        'conversations': get_all_conversations(current_user.id, db),
        'tasks': get_all_tasks(current_user.id, db),
        'instructions': get_all_instructions(current_user.id, db),
        'audit_logs': get_audit_logs(current_user.id, db),
        'embeddings': get_document_count(current_user.id, db)
    }

    # Create ZIP file
    zip_path = create_export_archive(data)

    return FileResponse(zip_path, filename=f"data_export_{current_user.id}.zip")

@router.delete("/privacy/delete-account")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account and all data"""

    # Delete all user data
    delete_user_embeddings(current_user.id, db)
    delete_user_conversations(current_user.id, db)
    delete_user_tasks(current_user.id, db)
    delete_user_instructions(current_user.id, db)
    delete_user_audit_logs(current_user.id, db)

    # Delete user
    db.delete(current_user)
    db.commit()

    return {"status": "account_deleted"}
```

---

### 7. Scalability & Performance

#### Caching Strategy

```python
# app/cache/redis_cache.py
import redis
import pickle

class RedisCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    def get(self, key: str):
        """Get cached value"""
        value = self.redis.get(key)
        if value:
            return pickle.loads(value)
        return None

    def set(self, key: str, value: any, ttl: int = 3600):
        """Set cached value with TTL"""
        self.redis.setex(key, ttl, pickle.dumps(value))

    def cache_user_context(self, user_id: str, context: dict, ttl: int = 1800):
        """Cache user context for faster retrieval"""
        key = f"user_context:{user_id}"
        self.set(key, context, ttl)

    def get_user_context(self, user_id: str) -> dict:
        """Get cached user context"""
        key = f"user_context:{user_id}"
        return self.get(key)
```

#### Rate Limiting

```python
# app/middleware/rate_limiter.py
from fastapi import HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/chat")
@limiter.limit("60/minute")
async def chat_endpoint(request: Request):
    # Endpoint logic
    pass
```

#### Async Processing

```python
# app/workers/celery_tasks.py
from celery import Celery

celery_app = Celery('financial_advisor_agent', broker='redis://localhost:6379/0')

@celery_app.task
def process_email_batch(user_id: str, email_ids: List[str]):
    """Process batch of emails asynchronously"""
    for email_id in email_ids:
        embed_email(user_id, email_id)

@celery_app.task
def generate_daily_report(user_id: str):
    """Generate daily report in background"""
    agent = create_agent(user_id)
    report = agent.invoke({"messages": [{"role": "user", "content": "Generate daily summary"}]})
    send_email(user_id, "Daily Summary", report)
```

---

## Deployment Architecture

### Production Infrastructure

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl

  backend:
    build: ./backend
    env_file: .env.production
    depends_on:
      - postgres
      - redis
    deploy:
      replicas: 3

  frontend:
    build: ./frontend
    env_file: .env.production
    depends_on:
      - backend

  postgres:
    image: pgvector/pgvector:pg15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: financial_advisor
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  celery_worker:
    build: ./backend
    command: celery -A app.workers.celery_tasks worker
    depends_on:
      - redis
      - postgres

  celery_beat:
    build: ./backend
    command: celery -A app.workers.celery_tasks beat
    depends_on:
      - redis

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: financial-advisor-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: financial-advisor-backend:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

---

## Monitoring & Observability

### Logging with DataDog

```python
# app/logging/datadog_logger.py
from ddtrace import tracer
import logging

# Configure DataDog APM
@tracer.wrap(service="financial-advisor-agent", resource="chat_endpoint")
def chat_handler(message: str, user_id: str):
    with tracer.trace("process_message", service="agent"):
        # Process message
        pass

# Structured logging
logger = logging.getLogger(__name__)
logger.info("User query received", extra={
    "user_id": user_id,
    "query_length": len(message),
    "timestamp": datetime.utcnow().isoformat()
})
```

### Error Tracking with Sentry

```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

---

## Summary

This full implementation guide covers:

1. **Real-time Webhooks** for instant event processing
2. **Advanced Proactive Behaviors** with intelligent instruction matching
3. **Multi-User & Team Features** for collaboration
4. **Analytics & Insights** for usage tracking
5. **Advanced RAG** with hybrid search and reranking
6. **Security & Compliance** (encryption, audit logs, GDPR)
7. **Scalability** (caching, rate limiting, async processing)
8. **Production Deployment** (Docker, Kubernetes)
9. **Monitoring** (logging, error tracking, APM)

These features extend the MVP into a production-grade, enterprise-ready system suitable for financial advisors and professional services firms.
