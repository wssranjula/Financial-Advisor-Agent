# Quick Start: Deploying Your Fixes

## What Was Fixed?

✅ **OAuth Redirect Issue** - Users will now be redirected to your production URL after OAuth
✅ **Route Protection** - Only authenticated users can access the chat interface
✅ **Logout Button** - Users can now logout from the chat interface
✅ **Frontend URLs** - Updated to use production backend

---

## 🚀 Deploy in 3 Steps

### Step 1: Set Backend Environment Variables (fly.io)

**Option A: Quick Script (Recommended)**

Windows:
```cmd
cd backend
deploy-secrets.bat
```

Linux/Mac:
```bash
cd backend
chmod +x deploy-secrets.sh
./deploy-secrets.sh
```

**Option B: Manual**
```bash
fly secrets set FRONTEND_URL=https://financial-advisor-agent-kgqs.vercel.app
fly secrets set GOOGLE_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/google/callback
fly secrets set HUBSPOT_REDIRECT_URI=https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback
```

**Then restart:**
```bash
fly apps restart
```

---

### Step 2: Update OAuth Provider Settings

**Google Cloud Console:**
1. Go to: https://console.cloud.google.com/
2. Navigate to: APIs & Services → Credentials
3. Click your OAuth 2.0 Client ID
4. Under "Authorized redirect URIs", add:
   ```
   https://financial-advisor-agent-be.fly.dev/api/auth/google/callback
   ```
5. Click "Save"

**HubSpot (if using):**
1. Go to: https://developers.hubspot.com/
2. Open your app → Auth settings
3. Update "Redirect URL" to:
   ```
   https://financial-advisor-agent-be.fly.dev/api/auth/hubspot/callback
   ```

---

### Step 3: Deploy Frontend (Vercel)

**Your .env.local is already updated!**

Just commit and push your changes:
```bash
git add .
git commit -m "Fix OAuth redirect, add route protection and logout"
git push origin main
```

Vercel will auto-deploy, or manually:
```bash
cd frontend
vercel --prod
```

---

## ✅ Test Your Deployment

1. **Open your app:** https://financial-advisor-agent-kgqs.vercel.app
2. **You should be redirected to login page** (route protection working!)
3. **Click "Continue with Google"**
4. **Complete OAuth consent**
5. **You should be redirected back to your Vercel URL** (not localhost!)
6. **You should see the chat interface** with your email and logout button
7. **Click "Logout"** - you should be redirected back to login

---

## 📁 Files Changed

### New Files Created:
- `frontend/contexts/AuthContext.tsx` - Authentication context
- `frontend/app/providers.tsx` - Client-side providers
- `backend/deploy-secrets.sh` / `.bat` - Deployment helper scripts
- `DEPLOYMENT_CONFIG.md` - Complete deployment guide
- `DEPLOYMENT_FIXES_SUMMARY.md` - Summary of all fixes
- This file!

### Modified Files:
- `frontend/.env.local` - Updated to production URLs
- `frontend/app/layout.tsx` - Added AuthProvider
- `frontend/app/page.tsx` - Added 'use client'
- `frontend/app/auth/callback/AuthCallbackClient.tsx` - Uses AuthContext
- `frontend/components/ChatInterface.tsx` - Added logout button

---

## 🆘 Need Help?

### Still redirecting to localhost?
- Verify `fly secrets list` shows correct FRONTEND_URL
- Run `fly apps restart`
- Clear browser cache

### CORS errors?
- Check `fly logs` for errors
- Verify ALLOWED_ORIGINS is set correctly

### Route protection not working?
- Clear browser localStorage
- Check browser console for errors

### More detailed help?
- See `DEPLOYMENT_CONFIG.md` for complete guide
- See `DEPLOYMENT_FIXES_SUMMARY.md` for technical details

---

## 📋 Environment Variables Checklist

### Backend (fly.io) - Set These!
- [ ] FRONTEND_URL
- [ ] GOOGLE_REDIRECT_URI
- [ ] HUBSPOT_REDIRECT_URI (if using)
- [ ] ALLOWED_ORIGINS

### Frontend (Vercel) - Already Done!
- [x] NEXT_PUBLIC_API_URL
- [x] NEXT_PUBLIC_BACKEND_URL

### OAuth Providers - Update These!
- [ ] Google Cloud Console redirect URI
- [ ] HubSpot Developer Portal redirect URI (if using)

---

## 🎉 You're Done!

Once you complete the 3 steps above, your application will:
- ✅ Redirect to production URL after OAuth (not localhost)
- ✅ Protect all routes (only authenticated users can access chat)
- ✅ Allow users to logout
- ✅ Work seamlessly between Vercel and fly.io

**Happy deploying! 🚀**

---

**Questions?** Check `DEPLOYMENT_CONFIG.md` for detailed instructions.
