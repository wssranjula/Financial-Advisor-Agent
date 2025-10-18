-- ============================================================
-- Financial Advisor AI Agent - Database Schema
-- ============================================================
-- Run this script in your Neon SQL Console
-- https://console.neon.tech/
-- ============================================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- Table: users
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    google_token TEXT,
    hubspot_token TEXT,
    last_gmail_sync TIMESTAMP,
    last_gmail_history_id VARCHAR(255),
    last_hubspot_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================================
-- Table: conversations
-- ============================================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);

-- ============================================================
-- Table: messages
-- ============================================================
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    message_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on conversation_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);

-- ============================================================
-- Table: document_embeddings
-- ============================================================
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    doc_metadata JSONB,
    source_type VARCHAR(50) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_document_embeddings_user_id ON document_embeddings(user_id);
CREATE INDEX IF NOT EXISTS idx_document_embeddings_source_type ON document_embeddings(source_type);
CREATE INDEX IF NOT EXISTS idx_document_embeddings_source_id ON document_embeddings(source_id);

-- Create vector similarity search index (HNSW for better performance)
CREATE INDEX IF NOT EXISTS idx_document_embeddings_vector
ON document_embeddings USING hnsw (embedding vector_cosine_ops);

-- Create composite index for unique source documents
CREATE UNIQUE INDEX IF NOT EXISTS idx_document_embeddings_unique_source
ON document_embeddings(user_id, source_type, source_id);

-- ============================================================
-- Verification Queries
-- ============================================================

-- Check that all tables were created
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_name IN ('users', 'conversations', 'messages', 'document_embeddings')
ORDER BY table_name;

-- Check pgvector extension
SELECT * FROM pg_extension WHERE extname = 'vector';

-- ============================================================
-- Sample Test Data (Optional - for testing)
-- ============================================================

-- Uncomment to insert a test user:
-- INSERT INTO users (email, full_name, is_active)
-- VALUES ('test@example.com', 'Test User', true)
-- ON CONFLICT (email) DO NOTHING;

-- ============================================================
-- Success!
-- ============================================================
-- If you see results from the verification queries above,
-- your database is ready!
--
-- Next steps:
-- 1. Start your backend server
-- 2. Try the Google OAuth login
-- ============================================================
