#!/bin/bash
# Setup PostgreSQL Database with pgvector
# Usage: ./setup-database.sh

set -e

DB_NAME="financial_advisor"
DB_USER="postgres"

echo "🗄️  Setting up PostgreSQL database..."
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed!"
    echo "Please install PostgreSQL 14+ first"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "❌ PostgreSQL is not running!"
    echo "Please start PostgreSQL first"
    exit 1
fi

echo "✅ PostgreSQL is running"

# Create database if it doesn't exist
echo "📦 Creating database '$DB_NAME'..."
psql -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || {
    psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
    echo "✅ Database created"
}

# Install pgvector extension
echo "🔧 Installing pgvector extension..."
psql -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;"
echo "✅ pgvector extension installed"

# Verify setup
echo ""
echo "🔍 Verifying database setup..."
psql -U $DB_USER -d $DB_NAME -c "\dx vector"

echo ""
echo "✅ Database setup complete!"
echo ""
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Extension: pgvector"
echo ""
echo "Connection string:"
echo "postgresql://$DB_USER:password@localhost:5432/$DB_NAME"
