#!/bin/bash
# Start Frontend Development Server
# Usage: ./start-frontend.sh

set -e

echo "🚀 Starting Financial Advisor AI Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "❌ .env.local file not found!"
    echo "Please create frontend/.env.local file. See TESTING_GUIDE.md"
    exit 1
fi

# Start server
echo ""
echo "✅ Starting Next.js server on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""

npm run dev
