"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="Financial Advisor AI Agent API",
    description="AI-powered assistant for financial advisors",
    version="0.1.0"
)

# CORS Middleware
# Build allowed origins list: include configured ALLOWED_ORIGINS plus FRONTEND_URL
allowed_origins = list(settings.ALLOWED_ORIGINS or [])
if settings.FRONTEND_URL:
    # ensure FRONTEND_URL is present and avoid duplicates
    if settings.FRONTEND_URL not in allowed_origins:
        allowed_origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Financial Advisor AI Agent API",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Import and include routers
from app.api import auth, sync, chat

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
