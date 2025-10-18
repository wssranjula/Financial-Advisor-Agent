@echo off
REM Setup PostgreSQL Database with pgvector (Windows)
REM Usage: setup-database.bat

set DB_NAME=financial_advisor
set DB_USER=postgres

echo 🗄️  Setting up PostgreSQL database...
echo.

REM Check if psql is in PATH
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL is not installed or not in PATH!
    echo Please install PostgreSQL 14+ and add it to PATH
    exit /b 1
)

echo ✅ PostgreSQL found

REM Create database
echo 📦 Creating database '%DB_NAME%'...
psql -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Database created
) else (
    echo ℹ️  Database might already exist
)

REM Install pgvector extension
echo 🔧 Installing pgvector extension...
psql -U %DB_USER% -d %DB_NAME% -c "CREATE EXTENSION IF NOT EXISTS vector;"
if %errorlevel% neq 0 (
    echo ❌ Failed to install pgvector extension
    echo Please install pgvector manually
    exit /b 1
)
echo ✅ pgvector extension installed

REM Verify setup
echo.
echo 🔍 Verifying database setup...
psql -U %DB_USER% -d %DB_NAME% -c "\dx vector"

echo.
echo ✅ Database setup complete!
echo.
echo Database: %DB_NAME%
echo User: %DB_USER%
echo Extension: pgvector
echo.
echo Connection string:
echo postgresql://%DB_USER%:password@localhost:5432/%DB_NAME%

pause
