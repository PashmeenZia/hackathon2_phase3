# Frontend Deployment Fix Guide

## Problem: Signin/Signup Not Working After Deployment

### Root Cause:
The frontend on Vercel doesn't know where to send API requests because the `NEXT_PUBLIC_API_BASE_URL` environment variable is not configured.

---

## Solution: Configure Environment Variables in Vercel

### Step 1: Get Your Hugging Face Backend URL

Your backend is deployed on Hugging Face Spaces. The URL format is:
```
https://your-username-your-space-name.hf.space
```

For example:
```
https://pashmeenzia-taskflow-backend.hf.space
```

### Step 2: Add Environment Variable in Vercel

1. Go to your project in Vercel Dashboard
2. Click on **Settings** → **Environment Variables**
3. Click **Add Environment Variable**
4. Add the following:
   - **Key**: `NEXT_PUBLIC_API_BASE_URL`
   - **Value**: `https://your-backend.hf.space` (your actual Hugging Face URL)
   - **Environment**: Select **Production**, **Preview**, and **Development**
5. Click **Save**

### Step 3: Redeploy the Frontend

After adding the environment variable:

1. Go to **Deployments** tab in Vercel
2. Click on the latest deployment
3. Click **Redeploy** (or push a new commit to trigger redeployment)
4. Wait for deployment to complete

---

## Backend Configuration (Hugging Face Spaces)

### Update Backend Environment Variables

In your Hugging Face Space settings, ensure these environment variables are set:

1. **BETTER_AUTH_SECRET**: A random secret (minimum 32 characters)
   ```
   BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long
   ```

2. **BETTER_AUTH_URL**: Your frontend Vercel URL
   ```
   BETTER_AUTH_URL=https://your-frontend.vercel.app
   ```

3. **OPENAI_API_KEY**: Your OpenAI API key
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

### CORS Configuration

The backend already has CORS configured to allow all origins (`allow_origins=["*"]`), which is fine for development. For production, you may want to restrict it:

```python
# In backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",  # Your Vercel URL
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing the Deployment

### 1. Check Frontend API Configuration

Open your browser console on the deployed site and check:
```javascript
console.log(process.env.NEXT_PUBLIC_API_BASE_URL)
```

It should show your Hugging Face backend URL.

### 2. Test API Connection

Visit: `https://your-backend.hf.space/health`

You should see:
```json
{"status": "healthy", "service": "task-management-api"}
```

### 3. Test Signin/Signup

1. Go to your Vercel deployed site
2. Click "Get Started" or "Sign In"
3. Try to create an account or sign in
4. Check browser console (F12) for any errors

---

## Common Issues & Solutions

### Issue 1: "Network Error" or "Failed to fetch"

**Cause**: Backend URL is incorrect or backend is not running

**Solution**: 
- Verify backend URL in Vercel environment variables
- Check if backend is accessible: `https://your-backend.hf.space/health`

### Issue 2: "CORS Error"

**Cause**: Backend CORS not configured properly

**Solution**:
- Ensure backend has CORS middleware enabled
- Check `allow_origins` includes your Vercel domain

### Issue 3: "401 Unauthorized" on every request

**Cause**: Authentication token not being sent

**Solution**:
- Check browser console for token issues
- Verify `localStorage` is working
- Check API client interceptor is adding Authorization header

### Issue 4: Backend sleeping on Hugging Face

**Cause**: Hugging Face free tier puts spaces to sleep after inactivity

**Solution**:
- Upgrade to Hugging Face Pro ($9/month)
- Or use a different backend hosting (Railway, Render, Fly.io)
- Or use a uptime monitor to ping your backend every 5 minutes

---

## Quick Checklist

- [ ] Backend deployed and accessible on Hugging Face
- [ ] `NEXT_PUBLIC_API_BASE_URL` set in Vercel (Production, Preview, Development)
- [ ] Backend environment variables configured (BETTER_AUTH_SECRET, BETTER_AUTH_URL, OPENAI_API_KEY)
- [ ] Frontend redeployed after adding environment variable
- [ ] CORS configured in backend for Vercel domain
- [ ] Tested signin/signup functionality
- [ ] Checked browser console for errors

---

## Alternative: Use Railway/Render for Backend

If Hugging Face Spaces is causing issues (sleeping, limited resources), consider:

### Railway Deployment:
1. Push backend to GitHub
2. Connect Railway to GitHub repo
3. Set environment variables in Railway
4. Railway provides: `https://your-backend.railway.app`

### Render Deployment:
1. Push backend to GitHub
2. Create Web Service in Render
3. Set environment variables
4. Render provides: `https://your-backend.onrender.com`

Then update Vercel's `NEXT_PUBLIC_API_BASE_URL` to the new backend URL.

---

## Debug Commands

### Check Vercel Environment Variables (locally):
```bash
cd frontend
vercel env pull
cat .env.development.local
```

### Test Backend API:
```bash
curl https://your-backend.hf.space/health
curl https://your-backend.hf.space/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test123"}'
```

### Check Frontend Network Requests:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to sign in
4. Check the request URL and response
