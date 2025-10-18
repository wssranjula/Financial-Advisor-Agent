# Deployment Configuration Guide

## Overview
This guide explains how to configure environment variables for the deployed application.

**Deployed URLs:**
- Frontend (Vercel): `https://financial-advisor-agent-kgqs.vercel.app`
- Backend (fly.io): `https://financial-advisor-agent-be.fly.dev`

---

## Backend Configuration (fly.io)

### Critical Environment Variables to Update

You need to update these environment variables on fly.io to fix the OAuth redirect issue:

#### 1. **FRONTEND_URL** (CRITICAL)
```bash
FRONTEND_URL=https://financial-advisor-agent-kgqs.vercel.app
```
This is used by the backend to redirect users back to the frontend after OAuth authentication.

#### 2. **GOOGLE_REDIRECT_URI** (CRITICAL)
```bash
GOOGLE_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/google/callback
```
This must also be updated in your Google Cloud Console OAuth settings.

#### 3. **HUBSPOT_REDIRECT_URI** (if using HubSpot)
```bash
HUBSPOT_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback
```
This must also be updated in your HubSpot Developer Portal OAuth settings.

#### 4. **ALLOWED_ORIGINS** (CORS)
```bash
ALLOWED_ORIGINS=["https://financial-advisor-agent-kgqs.vercel.app"]
```
Note: The FRONTEND_URL is automatically added to allowed origins by the backend code, but you can explicitly include it here too.

### How to Set Environment Variables on fly.io

#### Option 1: Using fly.io CLI
```bash
# Set FRONTEND_URL
fly secrets set FRONTEND_URL=https://financial-advisor-agent-kgqs.vercel.app

# Set Google OAuth redirect
fly secrets set GOOGLE_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/google/callback

# Set HubSpot OAuth redirect (if needed)
fly secrets set HUBSPOT_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback

# Set ALLOWED_ORIGINS
fly secrets set ALLOWED_ORIGINS='["https://financial-advisor-agent-kgqs.vercel.app"]'
```

After setting secrets, restart your app:
```bash
fly apps restart
```

#### Option 2: Using fly.io Dashboard
1. Go to https://fly.io/dashboard
2. Select your app: `financial-advisor-agent-be`
3. Go to "Secrets" section
4. Add/update the following secrets:
   - `FRONTEND_URL` = `https://financial-advisor-agent-kgqs.vercel.app`
   - `GOOGLE_REDIRECT_URI` = `https://financial-advisor-agent-be.fly.dev/api/auth/google/callback`
   - `HUBSPOT_REDIRECT_URI` = `https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback`
   - `ALLOWED_ORIGINS` = `["https://financial-advisor-agent-kgqs.vercel.app"]`

---

## Frontend Configuration (Vercel)

The frontend environment variables are already updated in `.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://financial-advisor-agent-be.fly.dev/api/chat
NEXT_PUBLIC_BACKEND_URL=https://financial-advisor-agent-be.fly.dev
```

### How to Set Environment Variables on Vercel

#### Option 1: Using Vercel CLI
```bash
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://financial-advisor-agent-be.fly.dev/api/chat

vercel env add NEXT_PUBLIC_BACKEND_URL
# Enter: https://financial-advisor-agent-be.fly.dev
```

Then redeploy:
```bash
vercel --prod
```

#### Option 2: Using Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Select your project: `financial-advisor-agent`
3. Go to "Settings" → "Environment Variables"
4. Add/update:
   - `NEXT_PUBLIC_API_URL` = `https://financial-advisor-agent-be.fly.dev/api/chat`
   - `NEXT_PUBLIC_BACKEND_URL` = `https://financial-advisor-agent-be.fly.dev`
5. Redeploy the application

---

## OAuth Configuration Updates

### Google Cloud Console

You need to update your OAuth redirect URIs in Google Cloud Console:

1. Go to https://console.cloud.google.com/
2. Select your project
3. Go to "APIs & Services" → "Credentials"
4. Click on your OAuth 2.0 Client ID
5. Under "Authorized redirect URIs", add:
   ```
   https://financial-advisor-agent-be.fly.dev/api/auth/google/callback
   ```
6. Keep the localhost URI for local development:
   ```
   http://localhost:8000/api/auth/google/callback
   ```
7. Click "Save"

### HubSpot Developer Portal (if using)

1. Go to https://developers.hubspot.com/
2. Go to your app
3. Go to "Auth" settings
4. Update "Redirect URL" to:
   ```
   https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback
   ```
5. Keep the localhost URL for local development:
   ```
   http://localhost:8000/api/auth/hubspot/callback
   ```

---

## Testing After Configuration

After updating all environment variables and OAuth settings:

1. **Test OAuth Flow:**
   - Go to `https://financial-advisor-agent-kgqs.vercel.app`
   - Click "Continue with Google"
   - Complete OAuth consent
   - Verify you're redirected back to `https://financial-advisor-agent-kgqs.vercel.app/auth/callback`
   - Verify you're then redirected to the chat interface

2. **Test Route Protection:**
   - Logout from the application
   - Try to access `https://financial-advisor-agent-kgqs.vercel.app/` directly
   - Verify you're redirected to `/login`

3. **Test Logout:**
   - Login to the application
   - Click the "Logout" button in the chat interface
   - Verify you're redirected to the login page

---

## Complete Environment Variables Checklist

### Backend (fly.io)
- [ ] `FRONTEND_URL` = `https://financial-advisor-agent-kgqs.vercel.app`
- [ ] `GOOGLE_REDIRECT_URI` = `https://financial-advisor-agent-be.fly.dev/api/auth/google/callback`
- [ ] `HUBSPOT_REDIRECT_URI` = `https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback`
- [ ] `ALLOWED_ORIGINS` = `["https://financial-advisor-agent-kgqs.vercel.app"]`
- [ ] All other variables from `.env.example` (DATABASE_URL, API keys, etc.)

### Frontend (Vercel)
- [ ] `NEXT_PUBLIC_API_URL` = `https://financial-advisor-agent-be.fly.dev/api/chat`
- [ ] `NEXT_PUBLIC_BACKEND_URL` = `https://financial-advisor-agent-be.fly.dev`

### OAuth Providers
- [ ] Google Cloud Console redirect URI updated
- [ ] HubSpot Developer Portal redirect URI updated (if using)

---

## Troubleshooting

### Issue: Still redirecting to localhost after OAuth

**Solution:**
1. Double-check `FRONTEND_URL` is set correctly on fly.io
2. Restart the fly.io app: `fly apps restart`
3. Clear your browser cache and cookies
4. Try the OAuth flow again

### Issue: CORS errors in browser console

**Solution:**
1. Check `ALLOWED_ORIGINS` includes the Vercel frontend URL
2. Verify the backend main.py includes FRONTEND_URL in CORS (it should by default)
3. Restart the fly.io app

### Issue: "Authentication failed" after OAuth

**Solution:**
1. Check browser console for errors
2. Check fly.io logs: `fly logs`
3. Verify OAuth credentials are correct in fly.io secrets
4. Verify redirect URIs match in both fly.io config and OAuth provider settings

---

## Rollback to Local Development

To switch back to local development:

### Backend
Update `.env` to use localhost URLs:
```bash
FRONTEND_URL=http://localhost:3000
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
HUBSPOT_REDIRECT_URI=http://localhost:8000/api/auth/hubspot/callback
```

### Frontend
Update `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/chat
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## Notes

- The backend CORS middleware automatically adds `FRONTEND_URL` to allowed origins (see `backend/app/main.py:16-20`)
- Route protection is handled by the `AuthContext` in the frontend
- User authentication state is stored in `localStorage`
- The logout function clears `localStorage` and redirects to `/login`

---

**Last Updated:** 2025-10-18
