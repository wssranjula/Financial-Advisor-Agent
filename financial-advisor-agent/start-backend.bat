@echo off
REM Start Backend Development Server (Windows)
REM Usage: start-backend.bat

echo 🚀 Starting Financial Advisor AI Backend...
echo.

cd "%~dp0backend"

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create backend\.env file. See TESTING_GUIDE.md
    exit /b 1
)

REM Install dependencies
echo 📥 Checking dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    exit /b 1
)

REM Run migrations
echo 🔄 Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo ⚠️  Migration failed, but continuing...
)

REM Start server
echo.
echo ✅ Starting FastAPI server on http://localhost:8000
echo 📚 API docs available at http://localhost:8000/docs
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
