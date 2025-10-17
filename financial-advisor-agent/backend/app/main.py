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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
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
from app.api import auth

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# TODO: Add more routers as they are implemented
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
