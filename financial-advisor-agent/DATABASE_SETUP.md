# Database Setup Guide for Neon

## 🎯 Quick Setup (2 minutes)

### Step 1: Open Neon SQL Console

1. Go to: https://console.neon.tech/
2. Log in to your account
3. Select your project: `ep-frosty-dawn-adzjh4au`
4. Click on **"SQL Editor"** in the left sidebar

### Step 2: Run the SQL Script

1. Open the file: `backend/create_tables.sql`
2. **Copy all the contents** (Ctrl+A, Ctrl+C)
3. **Paste into the Neon SQL Editor**
4. Click **"Run"** button (or press Ctrl+Enter)

### Step 3: Verify Success

You should see output showing:

```
table_name            | column_count
----------------------|-------------
conversations         | 5
document_embeddings   | 8
messages              | 5
users                 | 11
```

And:
```
extname | extversion
--------|------------
vector  | 0.5.1 (or similar)
```

✅ **If you see these results, your database is ready!**

## 🔍 What This Script Does

### 1. Enables pgvector Extension
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
Required for storing and searching embeddings.

### 2. Creates 4 Tables

**users** - User accounts
- id, email, full_name
- google_token, hubspot_token (encrypted OAuth tokens)
- last_gmail_sync, last_hubspot_sync (sync timestamps)

**conversations** - Chat conversations
- id, user_id, title
- Links to users table

**messages** - Chat messages
- id, conversation_id, role, content
- message_metadata (for tool calls, sources)
- Links to conversations table

**document_embeddings** - RAG search vectors
- id, user_id, content
- embedding (1536-dimensional vector)
- doc_metadata, source_type, source_id
- Links to users table

### 3. Creates Indexes

For fast queries:
- Email lookups (users)
- Conversation/message queries
- Vector similarity search (HNSW index for embeddings)
- Source document uniqueness

## 🧪 Test the Database

After running the script, you can test with these queries:

### Check Tables
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Check Vector Extension
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Check Indexes
```sql
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

## 🚀 After Database Setup

Once the tables are created, you can:

1. **Start your backend server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Try OAuth login**:
   - Visit: http://localhost:3000/login
   - Click "Continue with Google"
   - Complete authorization
   - User will be created in `users` table!

3. **Verify user created**:
   ```sql
   SELECT id, email, created_at, google_token IS NOT NULL as has_google_token
   FROM users;
   ```

## ⚠️ If Something Goes Wrong

### Error: "extension vector does not exist"

**Solution**: Your Neon database might not support pgvector yet.

1. Check Neon region (some regions don't support pgvector yet)
2. Create a new Neon project in a supported region (us-east-1 recommended)
3. Or contact Neon support to enable pgvector

### Error: "permission denied"

**Solution**: Make sure you're using the owner credentials from your DATABASE_URL.

### Want to Start Fresh?

```sql
-- WARNING: This deletes all data!
DROP TABLE IF EXISTS document_embeddings CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Then run the create_tables.sql script again
```

## 📊 Schema Diagram

```
users
  ├── conversations (user_id)
  │   └── messages (conversation_id)
  └── document_embeddings (user_id)
```

## 🎉 Next Steps

After successful database setup:

1. ✅ Database tables created
2. ✅ pgvector extension enabled
3. ✅ Indexes created
4. → Start backend server
5. → Test OAuth login
6. → Start chatting!

---

**Need help?** Check the verification queries in `create_tables.sql` to see what should appear after running the script.
