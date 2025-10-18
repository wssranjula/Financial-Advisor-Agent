@echo off
REM Start Frontend Development Server (Windows)
REM Usage: start-frontend.bat

echo 🚀 Starting Financial Advisor AI Frontend...
echo.

cd "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📥 Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        exit /b 1
    )
    echo ✅ Dependencies installed
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo ❌ .env.local file not found!
    echo Please create frontend\.env.local file. See TESTING_GUIDE.md
    exit /b 1
)

REM Start server
echo.
echo ✅ Starting Next.js server on http://localhost:3000
echo Press Ctrl+C to stop
echo.

npm run dev
