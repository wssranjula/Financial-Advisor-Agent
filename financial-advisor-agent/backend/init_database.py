#!/usr/bin/env python3
"""
Database Initialization Script

This script creates all database tables using SQLAlchemy's create_all() method.
Run this before starting the application for the first time.
"""

import sys
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, '.')

from app.config import settings
from app.database import Base
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.document_embedding import DocumentEmbedding


def create_tables_sync():
    """Create all tables using synchronous engine (for Neon/regular PostgreSQL)"""

    print("🗄️  Initializing Database...")
    print(f"📍 Database URL: {settings.DATABASE_URL[:50]}...")

    # Create synchronous engine
    engine = create_engine(settings.DATABASE_URL)

    try:
        # Test connection
        print("\n✓ Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Connected to: {version[:80]}...")

        # Check/create pgvector extension
        print("\n✓ Checking pgvector extension...")
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            print("✓ pgvector extension ready")

        # Create all tables
        print("\n✓ Creating database tables...")
        Base.metadata.create_all(bind=engine)

        # Verify tables were created
        print("\n✓ Verifying tables...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]

            print(f"✓ Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")

        print("\n✅ Database initialization complete!")
        print("\nYou can now start the application with:")
        print("  uvicorn app.main:app --reload")

        return True

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\nPlease check:")
        print("  1. DATABASE_URL in .env is correct")
        print("  2. Database exists and is accessible")
        print("  3. pgvector extension is available")
        return False

    finally:
        engine.dispose()


if __name__ == "__main__":
    print("=" * 70)
    print("Database Initialization Script")
    print("=" * 70)

    success = create_tables_sync()

    sys.exit(0 if success else 1)
