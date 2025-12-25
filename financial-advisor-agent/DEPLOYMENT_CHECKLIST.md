# Deployment Checklist

Use this checklist to ensure your deployment is complete and working correctly.

## 🔧 Pre-Deployment

### Backend Configuration (fly.io)
- [ ] `FRONTEND_URL` set to `https://financial-advisor-agent-kgqs.vercel.app`
- [ ] `GOOGLE_REDIRECT_URI` set to `https://financial-advisor-agent-be.fly.dev/api/auth/google/callback`
- [ ] `HUBSPOT_REDIRECT_URI` set to `https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback`
- [ ] `ALLOWED_ORIGINS` includes `["https://financial-advisor-agent-kgqs.vercel.app"]`
- [ ] `APP_ENV` set to `production`
- [ ] `DEBUG` set to `False`
- [ ] `SECRET_KEY` set (securely generated)
- [ ] `DATABASE_URL` configured
- [ ] `GOOGLE_CLIENT_ID` set
- [ ] `GOOGLE_CLIENT_SECRET` set
- [ ] `HUBSPOT_CLIENT_ID` set (if using)
- [ ] `HUBSPOT_CLIENT_SECRET` set (if using)
- [ ] `ANTHROPIC_API_KEY` set
- [ ] `OPENAI_API_KEY` set
- [ ] `ENCRYPTION_KEY` set (securely generated)
- [ ] Backend restarted: `fly apps restart`

### Frontend Configuration (Vercel)
- [ ] `NEXT_PUBLIC_API_URL` set to `https://financial-advisor-agent-be.fly.dev/api/chat`
- [ ] `NEXT_PUBLIC_BACKEND_URL` set to `https://financial-advisor-agent-be.fly.dev`
- [ ] Code pushed to git repository
- [ ] Vercel deployment triggered and successful

### OAuth Provider Configuration
- [ ] Google Cloud Console: Redirect URI updated to `https://financial-advisor-agent-be.fly.dev/api/auth/google/callback`
- [ ] HubSpot Developer Portal: Redirect URI updated (if using)
- [ ] Both production and localhost redirect URIs configured (for flexibility)

## ✅ Post-Deployment Testing

### 1. Basic Connectivity
- [ ] Frontend loads: https://financial-advisor-agent-kgqs.vercel.app
- [ ] Backend health check: https://financial-advisor-agent-be.fly.dev/health
- [ ] Backend API docs: https://financial-advisor-agent-be.fly.dev/docs

### 2. Route Protection
- [ ] Visiting root URL redirects to `/login`
- [ ] Cannot access chat without authentication
- [ ] Login page loads correctly
- [ ] Login page shows "Continue with Google" button

### 3. OAuth Flow
- [ ] Click "Continue with Google"
- [ ] Redirected to Google OAuth consent page
- [ ] Google consent page shows correct app name and permissions
- [ ] After consent, redirected to `/auth/callback` with success parameters
- [ ] Redirected to PRODUCTION URL (not localhost) ⭐ CRITICAL
- [ ] Auth callback page shows success message
- [ ] Automatically redirected to chat interface

### 4. Chat Interface
- [ ] Chat interface loads successfully
- [ ] User info displayed in header (email, avatar)
- [ ] Status indicator shows "Ready"
- [ ] Input area is functional
- [ ] Can type and send messages
- [ ] Messages are displayed correctly
- [ ] AI responses stream in real-time (SSE)
- [ ] Tool calls are displayed (if any)

### 5. Logout Functionality
- [ ] Logout button visible in header
- [ ] Click logout button
- [ ] Redirected to login page
- [ ] Cannot access chat after logout (redirected to login)
- [ ] Can login again successfully

### 6. Error Handling
- [ ] Logout → Try to access `/` → Redirected to login
- [ ] Open chat in private/incognito mode → Redirected to login
- [ ] Invalid OAuth callback → Shows error message
- [ ] Network errors displayed to user

### 7. Browser Compatibility
- [ ] Chrome: All features work
- [ ] Firefox: All features work
- [ ] Safari: All features work
- [ ] Edge: All features work
- [ ] Mobile browser: Layout responsive and functional

### 8. Security
- [ ] HTTPS enabled (should be automatic with Vercel/fly.io)
- [ ] OAuth uses HTTPS redirect URIs
- [ ] No sensitive data exposed in URLs
- [ ] Tokens stored securely (localStorage for session)
- [ ] CORS configured correctly (no cross-origin errors)

## 🔍 Verification Commands

### Check Backend Environment
```bash
fly secrets list
```
Should show all required secrets (values hidden).

### Check Backend Logs
```bash
fly logs
```
Look for:
- No error messages
- Successful OAuth callbacks
- No CORS errors

### Check Frontend Build
```bash
# In Vercel dashboard or:
vercel logs
```
Look for:
- Successful build
- No build errors
- Environment variables loaded

### Test API Endpoints
```bash
# Health check
curl https://financial-advisor-agent-be.fly.dev/health

# OAuth URL generation (should return JSON with authorization_url)
curl https://financial-advisor-agent-be.fly.dev/api/auth/google/login
```

## 🐛 Common Issues & Solutions

### Issue: Still redirecting to localhost
- [ ] Verified `FRONTEND_URL` is set correctly on fly.io
- [ ] Restarted fly.io app
- [ ] Cleared browser cache and cookies
- [ ] Checked fly.io logs for errors

### Issue: CORS errors
- [ ] Verified `ALLOWED_ORIGINS` includes Vercel URL
- [ ] Verified `FRONTEND_URL` is set (automatically added to CORS)
- [ ] Checked browser console for specific CORS error
- [ ] Restarted fly.io app

### Issue: OAuth fails
- [ ] Verified redirect URIs match in both fly.io config and OAuth provider
- [ ] Verified OAuth credentials are correct
- [ ] Checked fly.io logs for error details
- [ ] Verified OAuth app is enabled in provider console

### Issue: Route protection not working
- [ ] Cleared localStorage
- [ ] Verified AuthContext is loaded (check browser console)
- [ ] Hard refresh (Ctrl+Shift+R)
- [ ] Check browser console for errors

### Issue: Logout doesn't work
- [ ] Verified logout button calls AuthContext.logout()
- [ ] Checked browser console for errors
- [ ] Verified localStorage.clear() is called
- [ ] Hard refresh and try again

## 📊 Performance Checks

### Backend
- [ ] Response time < 500ms for simple queries
- [ ] OAuth redirect < 2 seconds
- [ ] SSE streaming starts within 1 second
- [ ] No memory leaks (check fly.io metrics)

### Frontend
- [ ] Initial page load < 3 seconds
- [ ] Login page load < 2 seconds
- [ ] Chat interface renders quickly
- [ ] Smooth scrolling and interactions

## 🎉 Deployment Complete!

Once all items are checked, your deployment is complete and verified!

**Final Check:**
1. [ ] All checklist items above are completed
2. [ ] No errors in fly.io logs
3. [ ] No errors in Vercel logs
4. [ ] No errors in browser console
5. [ ] OAuth flow works end-to-end
6. [ ] Route protection works
7. [ ] Logout works
8. [ ] Chat functionality works

## 📝 Notes

**Date Deployed:** _____________

**Deployed By:** _____________

**Issues Encountered:**
-
-

**Resolutions:**
-
-

**Additional Notes:**
-
-

---

**Need Help?**
- See [QUICK_START_DEPLOYMENT.md](QUICK_START_DEPLOYMENT.md) for quick instructions
- See [DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md) for detailed guide
- Check fly.io logs: `fly logs`
- Check Vercel deployment logs in Vercel dashboard
