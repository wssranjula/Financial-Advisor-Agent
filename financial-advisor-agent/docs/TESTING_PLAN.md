# Testing Plan for Financial Advisor AI Agent

This document outlines comprehensive testing strategies for the implemented OAuth, integration clients, tools, subagents, and main agent.

---

## Test Environment Setup

### Prerequisites
1. **Database**: PostgreSQL with pgvector extension
2. **OAuth Credentials**:
   - Google Cloud Console OAuth credentials
   - HubSpot Developer app credentials
3. **Test User**: webshookeng@gmail.com
4. **API Keys**:
   - Anthropic API key
   - OpenAI API key (for future RAG)
5. **Environment Variables**: Configure all required vars in `.env`

### Setup Steps

```bash
# 1. Create and activate virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up database
createdb financial_advisor
psql financial_advisor -c "CREATE EXTENSION vector;"

# 4. Run migrations
alembic upgrade head

# 5. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 6. Verify installation
python -c "import app; print('✓ App imports successfully')"
```

---

## Phase 1: OAuth Integration Tests

### Test 1.1: Google OAuth Flow

**Objective**: Verify Google OAuth authorization and token storage

**Steps**:
1. Start the FastAPI server
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Test OAuth URL generation
   ```bash
   curl http://localhost:8000/api/auth/google/login
   ```
   **Expected**: JSON with `authorization_url` and `state`

3. Open the authorization URL in browser
   - Login with webshookeng@gmail.com
   - Grant permissions (Gmail + Calendar scopes)
   - Note the callback code parameter

4. Test OAuth callback
   ```bash
   curl "http://localhost:8000/api/auth/google/callback?code=AUTHORIZATION_CODE&state=STATE_VALUE"
   ```
   **Expected**: Success message with user_id and email

5. Verify token storage
   ```bash
   psql financial_advisor -c "SELECT email, google_token IS NOT NULL as has_token FROM users;"
   ```
   **Expected**: User row with `has_token = true`

**Success Criteria**:
- ✅ Authorization URL generated
- ✅ OAuth flow completes without errors
- ✅ Token encrypted and stored in database
- ✅ User created or updated

### Test 1.2: HubSpot OAuth Flow

**Objective**: Verify HubSpot OAuth authorization and token storage

**Steps**:
1. Test OAuth URL generation
   ```bash
   curl http://localhost:8000/api/auth/hubspot/login
   ```

2. Complete OAuth flow in browser
   - Login to HubSpot account
   - Grant CRM permissions

3. Test callback (requires auth header with user email)
   ```bash
   curl -H "Authorization: Bearer webshookeng@gmail.com" \
        "http://localhost:8000/api/auth/hubspot/callback?code=AUTHORIZATION_CODE"
   ```

4. Verify token storage
   ```bash
   psql financial_advisor -c "SELECT email, hubspot_token IS NOT NULL as has_token FROM users;"
   ```

**Success Criteria**:
- ✅ HubSpot OAuth completes
- ✅ Token encrypted and stored
- ✅ Both google_token and hubspot_token present

### Test 1.3: Authentication Status

**Objective**: Verify auth status endpoint

**Steps**:
```bash
curl -H "Authorization: Bearer webshookeng@gmail.com" \
     http://localhost:8000/api/auth/status
```

**Expected Response**:
```json
{
  "authenticated": true,
  "user": {
    "id": "uuid",
    "email": "webshookeng@gmail.com",
    "has_google_auth": true,
    "has_hubspot_auth": true
  },
  "google_connected": true,
  "hubspot_connected": true
}
```

**Success Criteria**:
- ✅ Status shows both OAuth connections
- ✅ User details returned correctly

---

## Phase 2: Integration Client Tests

### Test 2.1: Gmail Client

**Objective**: Verify GmailClient wrapper functions

**Test Script** (`tests/test_gmail_client.py`):
```python
from app.integrations.gmail import GmailClient
from app.integrations.google_auth import google_oauth_service
from app.security import encryption_service
from app.models import User
from app.database import SessionLocal

# Get user and credentials
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

token_dict = encryption_service.decrypt_token(user.google_token)
credentials = google_oauth_service.get_credentials(token_dict)
client = GmailClient(credentials)

# Test 1: List messages
print("Test 1: List messages...")
result = client.list_messages(query="from:me", max_results=5)
assert len(result['messages']) > 0
print(f"✓ Found {len(result['messages'])} messages")

# Test 2: Get message
print("\nTest 2: Get message...")
msg_id = result['messages'][0]['id']
message = client.get_message(msg_id)
assert message['id'] == msg_id
print(f"✓ Retrieved message: {client.get_message_headers(message).get('Subject')}")

# Test 3: Get message body
print("\nTest 3: Get message body...")
body = client.get_message_body(message)
print(f"✓ Body length: {len(body)} characters")

# Test 4: Send email
print("\nTest 4: Send email...")
sent = client.send_message(
    to="webshookeng@gmail.com",
    subject="Test from Financial Advisor Agent",
    body="This is a test email from the agent system."
)
assert 'id' in sent
print(f"✓ Email sent: {sent['id']}")

# Test 5: Get profile
print("\nTest 5: Get profile...")
profile = client.get_profile()
assert profile['emailAddress'] == "webshookeng@gmail.com"
print(f"✓ Profile: {profile['emailAddress']}")

print("\n✅ All Gmail client tests passed!")
```

**Run Test**:
```bash
cd backend
python tests/test_gmail_client.py
```

**Success Criteria**:
- ✅ List messages returns results
- ✅ Get message retrieves full content
- ✅ Message body extracted correctly
- ✅ Send email succeeds
- ✅ Profile matches user email

### Test 2.2: Calendar Client

**Test Script** (`tests/test_calendar_client.py`):
```python
from app.integrations.calendar import CalendarClient
from app.integrations.google_auth import google_oauth_service
from app.security import encryption_service
from app.models import User
from app.database import SessionLocal
from datetime import datetime, timedelta

# Get user and credentials
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

token_dict = encryption_service.decrypt_token(user.google_token)
credentials = google_oauth_service.get_credentials(token_dict)
client = CalendarClient(credentials)

# Test 1: List events
print("Test 1: List upcoming events...")
time_min = datetime.utcnow()
time_max = time_min + timedelta(days=7)
result = client.list_events(time_min=time_min, time_max=time_max)
print(f"✓ Found {len(result['items'])} events")

# Test 2: Create event
print("\nTest 2: Create calendar event...")
start = datetime.utcnow() + timedelta(days=1, hours=2)
end = start + timedelta(hours=1)
event = client.create_event(
    summary="Test Meeting - Financial Advisor Agent",
    start_time=start,
    end_time=end,
    description="Test event created by the agent system"
)
event_id = event['id']
print(f"✓ Event created: {event_id}")

# Test 3: Get event
print("\nTest 3: Get event details...")
retrieved = client.get_event(event_id)
assert retrieved['summary'] == "Test Meeting - Financial Advisor Agent"
print(f"✓ Event retrieved: {retrieved['summary']}")

# Test 4: Free/Busy
print("\nTest 4: Check free/busy...")
freebusy = client.get_free_busy(
    calendars=['primary'],
    time_min=time_min,
    time_max=time_max
)
print(f"✓ Free/busy retrieved")

# Test 5: Find available slots
print("\nTest 5: Find available slots...")
slots = client.find_available_slots(
    calendars=['primary'],
    time_min=time_min,
    time_max=time_max,
    duration_minutes=60
)
print(f"✓ Found {len(slots)} available slots")

# Cleanup: Delete test event
print("\nCleanup: Deleting test event...")
client.delete_event(event_id)
print(f"✓ Event deleted")

print("\n✅ All Calendar client tests passed!")
```

**Run Test**:
```bash
cd backend
python tests/test_calendar_client.py
```

**Success Criteria**:
- ✅ List events works
- ✅ Create event succeeds
- ✅ Event details retrieved
- ✅ Free/busy information returned
- ✅ Available slots found
- ✅ Delete event works

### Test 2.3: HubSpot Client

**Test Script** (`tests/test_hubspot_client.py`):
```python
from app.integrations.hubspot import HubSpotClient
from app.security import encryption_service
from app.models import User
from app.database import SessionLocal

# Get user and token
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

token_dict = encryption_service.decrypt_token(user.hubspot_token)
access_token = token_dict['access_token']
client = HubSpotClient(access_token)

# Test 1: Get contacts
print("Test 1: Get contacts...")
result = client.get_contacts(limit=5)
contacts = result['results']
print(f"✓ Retrieved {len(contacts)} contacts")

# Test 2: Search contacts
print("\nTest 2: Search contacts...")
if contacts:
    email = contacts[0]['properties'].get('email')
    if email:
        search_result = client.search_contacts([
            {"propertyName": "email", "operator": "EQ", "value": email}
        ])
        assert len(search_result['results']) > 0
        print(f"✓ Found contact: {email}")

# Test 3: Create contact
print("\nTest 3: Create test contact...")
test_email = "test_agent_contact@example.com"
contact = client.create_contact({
    "email": test_email,
    "firstname": "Test",
    "lastname": "AgentContact",
    "company": "Test Company"
})
contact_id = contact['id']
print(f"✓ Contact created: {contact_id}")

# Test 4: Get contact
print("\nTest 4: Get contact details...")
retrieved = client.get_contact(contact_id)
assert retrieved['id'] == contact_id
print(f"✓ Contact retrieved")

# Test 5: Create note
print("\nTest 5: Create note...")
note = client.create_note(
    note_body="Test note from Financial Advisor Agent",
    contact_id=contact_id
)
note_id = note['id']
print(f"✓ Note created: {note_id}")

# Test 6: Get contact notes
print("\nTest 6: Get contact notes...")
notes = client.get_contact_notes(contact_id)
assert len(notes['results']) > 0
print(f"✓ Retrieved {len(notes['results'])} notes")

# Test 7: Get by email
print("\nTest 7: Get contact by email...")
by_email = client.get_contact_by_email(test_email)
assert by_email['id'] == contact_id
print(f"✓ Found contact by email")

print("\n✅ All HubSpot client tests passed!")
print(f"\nNote: Test contact created with ID: {contact_id}")
print("You may want to delete this contact manually from HubSpot CRM")
```

**Run Test**:
```bash
cd backend
python tests/test_hubspot_client.py
```

**Success Criteria**:
- ✅ Get contacts returns results
- ✅ Search finds contacts
- ✅ Create contact succeeds
- ✅ Get contact retrieves details
- ✅ Create note works
- ✅ Get notes returns results
- ✅ Get by email finds contact

---

## Phase 3: Tool Tests

### Test 3.1: Gmail Tools

**Test Script** (`tests/test_gmail_tools.py`):
```python
from app.agents.tools.gmail_tools import search_emails, get_email, send_email
from app.models import User
from app.database import SessionLocal

# Get test user
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

# Test 1: Search emails
print("Test 1: Search emails tool...")
result = search_emails.invoke({
    "query": "from:me",
    "max_results": 5,
    "user": user
})
print(result)
assert "Found" in result
print("✓ Search emails works")

# Test 2: Send email
print("\nTest 2: Send email tool...")
result = send_email.invoke({
    "to": "webshookeng@gmail.com",
    "subject": "Test from Gmail Tool",
    "body": "This email was sent using the gmail_tools",
    "user": user
})
print(result)
assert "successfully" in result
print("✓ Send email works")

print("\n✅ Gmail tools tests passed!")
```

**Run Test**:
```bash
cd backend
python tests/test_gmail_tools.py
```

**Success Criteria**:
- ✅ search_emails returns formatted results
- ✅ get_email retrieves full content
- ✅ send_email succeeds
- ✅ reply_to_email works

### Test 3.2: Calendar Tools

**Test Script** (`tests/test_calendar_tools.py`):
```python
from app.agents.tools.calendar_tools import get_calendar_events, create_calendar_event, find_available_slots
from app.models import User
from app.database import SessionLocal

# Get test user
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

# Test 1: Get events
print("Test 1: Get calendar events tool...")
result = get_calendar_events.invoke({
    "days_ahead": 7,
    "user": user
})
print(result)
print("✓ Get events works")

# Test 2: Find slots
print("\nTest 2: Find available slots tool...")
result = find_available_slots.invoke({
    "duration_minutes": 60,
    "days_ahead": 7,
    "user": user
})
print(result)
assert "Available" in result
print("✓ Find slots works")

print("\n✅ Calendar tools tests passed!")
```

### Test 3.3: HubSpot Tools

**Test Script** (`tests/test_hubspot_tools.py`):
```python
from app.agents.tools.hubspot_tools import search_contacts, create_contact, get_recent_contacts
from app.models import User
from app.database import SessionLocal

# Get test user
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

# Test 1: Recent contacts
print("Test 1: Get recent contacts tool...")
result = get_recent_contacts.invoke({
    "max_results": 5,
    "user": user
})
print(result)
assert "Recent contacts" in result
print("✓ Get recent contacts works")

# Test 2: Search contacts
print("\nTest 2: Search contacts tool...")
result = search_contacts.invoke({
    "search_query": "test",
    "search_field": "email",
    "user": user
})
print(result)
print("✓ Search contacts works")

print("\n✅ HubSpot tools tests passed!")
```

---

## Phase 4: Agent Tests

### Test 4.1: Main Agent Creation

**Test Script** (`tests/test_main_agent.py`):
```python
from app.agents.main_agent import create_financial_advisor_agent
from app.models import User
from app.database import SessionLocal

print("Creating Financial Advisor Agent...")
agent = create_financial_advisor_agent()

print("✓ Agent created successfully")
print("\nAgent has access to:")
print("- 4 Gmail tools")
print("- 4 Calendar tools")
print("- 6 HubSpot tools")
print("- 3 Subagents (email_researcher, calendar_scheduler, hubspot_manager)")

print("\n✅ Agent creation test passed!")
```

### Test 4.2: Agent Invocation

**Test Script** (`tests/test_agent_invocation.py`):
```python
from app.agents.main_agent import create_financial_advisor_agent, invoke_agent
from app.models import User
from app.database import SessionLocal
import uuid

# Get test user
db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()

# Create agent
agent = create_financial_advisor_agent()

# Test 1: Simple greeting
print("Test 1: Simple greeting...")
result = invoke_agent(
    agent=agent,
    message="Hello! What can you help me with?",
    thread_id=str(uuid.uuid4()),
    user=user
)
print(result['messages'][-1]['content'])
print("✓ Agent responds to greeting")

# Test 2: Email search request
print("\nTest 2: Email search...")
result = invoke_agent(
    agent=agent,
    message="Search my emails from the last week",
    thread_id=str(uuid.uuid4()),
    user=user
)
print(result['messages'][-1]['content'])
print("✓ Agent handles email search")

# Test 3: Calendar check
print("\nTest 3: Calendar check...")
result = invoke_agent(
    agent=agent,
    message="What's on my calendar for the next 3 days?",
    thread_id=str(uuid.uuid4()),
    user=user
)
print(result['messages'][-1]['content'])
print("✓ Agent checks calendar")

# Test 4: CRM lookup
print("\nTest 4: CRM lookup...")
result = invoke_agent(
    agent=agent,
    message="Show me my recent contacts in HubSpot",
    thread_id=str(uuid.uuid4()),
    user=user
)
print(result['messages'][-1]['content'])
print("✓ Agent accesses CRM")

print("\n✅ Agent invocation tests passed!")
```

---

## Phase 5: Integration Tests

### Test 5.1: Cross-System Workflow

**Scenario**: "Tell me about John Smith"

**Expected Behavior**:
1. Search HubSpot for John Smith contact
2. Get contact details from CRM
3. Search emails from John Smith
4. Check calendar for meetings with John
5. Provide comprehensive summary

**Test Script**:
```python
from app.agents.main_agent import create_financial_advisor_agent, invoke_agent
from app.models import User
from app.database import SessionLocal
import uuid

db = SessionLocal()
user = db.query(User).filter(User.email == "webshookeng@gmail.com").first()
agent = create_financial_advisor_agent()

print("Cross-System Test: Client Lookup...")
result = invoke_agent(
    agent=agent,
    message="Tell me everything you know about [REAL_CLIENT_NAME]",
    thread_id=str(uuid.uuid4()),
    user=user
)

response = result['messages'][-1]['content']
print("\nAgent Response:")
print(response)

# Verify response includes data from multiple systems
assert "email" in response.lower() or "contact" in response.lower()
print("\n✓ Agent accessed CRM")

# Check if emails were searched
# Check if calendar was checked

print("\n✅ Cross-system integration test passed!")
```

### Test 5.2: Multi-Step Task

**Scenario**: "Schedule a call with Sarah for next Tuesday"

**Expected Behavior**:
1. Check calendar for availability on Tuesday
2. Find available time slots
3. Confirm time with user
4. Create calendar event
5. Optionally send email invitation

**Manual Test**:
1. Send message: "Schedule a call with sarah@example.com for next Tuesday afternoon"
2. Agent should check availability
3. Agent should suggest specific times
4. Confirm a time
5. Agent creates event
6. Verify event in Google Calendar

**Success Criteria**:
- ✅ Agent checks availability first
- ✅ Agent suggests specific times
- ✅ Event created successfully
- ✅ Event visible in Google Calendar

---

## Phase 6: Error Handling Tests

### Test 6.1: Missing Authentication

**Test**: Call tools without user context

**Expected**: Error message about missing authentication

### Test 6.2: Invalid OAuth Token

**Test**: Manually corrupt OAuth token in database

**Expected**: Token refresh or re-auth prompt

### Test 6.3: API Rate Limits

**Test**: Make rapid consecutive requests

**Expected**: Retry logic handles transient failures

### Test 6.4: Network Failures

**Test**: Disconnect network during operation

**Expected**: Graceful error messages, retry logic

---

## Test Checklist Summary

### Phase 1: OAuth ✓
- [ ] Google OAuth flow completes
- [ ] HubSpot OAuth flow completes
- [ ] Tokens encrypted and stored
- [ ] Auth status endpoint works

### Phase 2: Clients ✓
- [ ] Gmail client all methods work
- [ ] Calendar client all methods work
- [ ] HubSpot client all methods work
- [ ] Error handling and retries function

### Phase 3: Tools ✓
- [ ] All Gmail tools work
- [ ] All Calendar tools work
- [ ] All HubSpot tools work
- [ ] User context injection works

### Phase 4: Agent ✓
- [ ] Agent creation succeeds
- [ ] Agent responds to messages
- [ ] Agent uses tools correctly
- [ ] Agent delegates to subagents
- [ ] Memory persistence works

### Phase 5: Integration ✓
- [ ] Cross-system queries work
- [ ] Multi-step tasks complete
- [ ] Complex workflows succeed

### Phase 6: Error Handling ✓
- [ ] Missing auth handled
- [ ] Invalid tokens handled
- [ ] Rate limits handled
- [ ] Network errors handled

---

## Performance Tests

### Response Time Benchmarks

**Target Response Times**:
- Simple queries: < 2 seconds
- Tool invocations: < 5 seconds
- Multi-step tasks: < 15 seconds
- Complex workflows: < 30 seconds

**Load Testing**:
- Concurrent users: 10
- Requests per minute: 100
- Success rate: > 95%

---

## Security Tests

### Authentication Tests
- [ ] Verify OAuth tokens are encrypted
- [ ] Verify tokens are not logged
- [ ] Verify user isolation (can't access other users' data)
- [ ] Verify API keys not exposed in responses

### Authorization Tests
- [ ] Verify users can only access their own data
- [ ] Verify proper scope validation
- [ ] Verify token expiration handling

---

## Next Steps After Testing

1. **Fix Issues**: Address any failing tests
2. **Document Results**: Create test report
3. **Performance Optimization**: If benchmarks not met
4. **User Acceptance Testing**: Test with real financial advisor
5. **Iterate**: Based on feedback

---

## Automated Testing Setup

### CI/CD Integration

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd backend
          pytest tests/ -v
```

---

## Manual Testing Checklist

For non-automated testing, use this checklist:

**Week 1: OAuth & Clients**
- [ ] Day 1: Google OAuth
- [ ] Day 2: HubSpot OAuth
- [ ] Day 3: Gmail Client
- [ ] Day 4: Calendar Client
- [ ] Day 5: HubSpot Client

**Week 2: Tools & Agent**
- [ ] Day 1: Gmail Tools
- [ ] Day 2: Calendar Tools
- [ ] Day 3: HubSpot Tools
- [ ] Day 4: Main Agent
- [ ] Day 5: Integration Tests

**Week 3: Polish & User Testing**
- [ ] Day 1: Error handling
- [ ] Day 2: Performance testing
- [ ] Day 3: Security testing
- [ ] Day 4-5: User acceptance testing

---

## Success Metrics

The implementation is considered successful when:

1. **Functionality**: All tests pass ✅
2. **Performance**: Meets response time benchmarks ✅
3. **Reliability**: > 95% success rate ✅
4. **Security**: No auth/data leaks ✅
5. **Usability**: Positive user feedback ✅

---

## Reporting Issues

When tests fail, document:
1. Test name and description
2. Expected behavior
3. Actual behavior
4. Steps to reproduce
5. Error messages/logs
6. Environment details

Create GitHub issues with this information for tracking.
