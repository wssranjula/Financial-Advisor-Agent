#!/bin/bash
# Start Backend Development Server
# Usage: ./start-backend.sh

set -e

echo "🚀 Starting Financial Advisor AI Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create backend/.env file. See TESTING_GUIDE.md"
    exit 1
fi

# Check if database is accessible
echo "🗄️  Checking database connection..."
python -c "from app.database import engine; print('✅ Database connection OK')" || {
    echo "❌ Database connection failed!"
    echo "Please check your DATABASE_URL in .env"
    exit 1
}

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Start server
echo ""
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
