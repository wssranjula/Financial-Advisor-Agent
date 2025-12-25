#!/bin/bash

# Deployment script to set fly.io secrets
# Run this script after updating the values below with your actual credentials

echo "Setting fly.io secrets for Financial Advisor AI Agent backend..."

# IMPORTANT: Update these values before running!
FRONTEND_URL="https://financial-advisor-agent-kgqs.vercel.app"
BACKEND_URL="https://financial-advisor-agent-be.fly.dev"

# Set FRONTEND_URL (CRITICAL for OAuth redirect)
echo "Setting FRONTEND_URL..."
fly secrets set FRONTEND_URL="$FRONTEND_URL"

# Set OAuth redirect URIs
echo "Setting OAuth redirect URIs..."
fly secrets set GOOGLE_REDIRECT_URI="${BACKEND_URL}/api/auth/google/callback"
fly secrets set HUBSPOT_REDIRECT_URI="${BACKEND_URL}/api/auth/hubspot/callback"

# Set CORS allowed origins
echo "Setting ALLOWED_ORIGINS..."
fly secrets set ALLOWED_ORIGINS='["'$FRONTEND_URL'"]'

# Set environment
echo "Setting environment variables..."
fly secrets set APP_ENV="production"
fly secrets set ENVIRONMENT="production"
fly secrets set DEBUG="False"

echo ""
echo "✅ Basic deployment secrets set!"
echo ""
echo "⚠️  IMPORTANT: You still need to set these secrets manually:"
echo "   - SECRET_KEY"
echo "   - DATABASE_URL"
echo "   - GOOGLE_CLIENT_ID"
echo "   - GOOGLE_CLIENT_SECRET"
echo "   - HUBSPOT_CLIENT_ID"
echo "   - HUBSPOT_CLIENT_SECRET"
echo "   - ANTHROPIC_API_KEY"
echo "   - OPENAI_API_KEY"
echo "   - ENCRYPTION_KEY"
echo ""
echo "You can set them with:"
echo "  fly secrets set SECRET_KEY=your-secret-key"
echo ""
echo "After setting all secrets, restart the app:"
echo "  fly apps restart"
echo ""
echo "📚 See DEPLOYMENT_CONFIG.md for complete instructions"
