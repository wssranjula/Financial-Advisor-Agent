"""
Initialize the database by importing models and creating tables.
Run this with the project's virtualenv active. It will use DATABASE_URL from .env.

Usage:
    python backend/scripts/init_db.py
"""
from app.database import init_db
# Import models so they are registered with Base
import app.models  # noqa: F401

if __name__ == "__main__":
    print("Initializing database tables...")
    init_db()
    print("Done.")
