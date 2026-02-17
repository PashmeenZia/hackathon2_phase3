# Phase III Deployment Checklist

## Pre-Deployment

### Backend Setup
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database tables created (`python create_chat_tables.py`)
- [ ] Environment variables configured in `.env`
  - [ ] `DATABASE_URL` set to production database
  - [ ] `JWT_SECRET` set to secure random string
  - [ ] `OPENAI_API_KEY` set (optional but recommended)
- [ ] Test setup verified (`python test_setup.py`)
- [ ] Backend runs locally without errors

### Frontend Setup
- [ ] All dependencies installed (`npm install`)
- [ ] Environment variables configured in `.env.local`
  - [ ] `NEXT_PUBLIC_API_URL` set to backend URL
- [ ] Frontend runs locally without errors
- [ ] Chat page accessible at `/chat`

### Testing
- [ ] User can login successfully
- [ ] Chat interface loads without errors
- [ ] Can send messages and receive responses
- [ ] Task operations work (add, list, complete, delete)
- [ ] Conversation persists across page refreshes
- [ ] User isolation verified (users can't see others' data)

## Deployment

### Backend Deployment (Railway/Render/etc.)

- [ ] Create new project/service
- [ ] Connect to GitHub repository
- [ ] Set root directory to `backend/`
- [ ] Configure environment variables:
  ```
  DATABASE_URL=postgresql://...
  JWT_SECRET=...
  OPENAI_API_KEY=sk-proj-...
  ```
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- [ ] Deploy and verify health endpoint: `https://your-backend.com/health`
- [ ] Run database migration: `python create_chat_tables.py`

### Frontend Deployment (Vercel)

- [ ] Create new project
- [ ] Connect to GitHub repository
- [ ] Set root directory to `frontend/`
- [ ] Configure environment variables:
  ```
  NEXT_PUBLIC_API_URL=https://your-backend.com
  ```
- [ ] Deploy and verify site loads
- [ ] Test chat functionality on production

### OpenAI Configuration (If Using OpenAI)

- [ ] Get production frontend URL (e.g., `https://your-app.vercel.app`)
- [ ] Navigate to: https://platform.openai.com/settings/organization/security/domain-allowlist
- [ ] Click "Add domain"
- [ ] Enter frontend URL (without trailing slash)
- [ ] Save changes
- [ ] Get domain key from OpenAI
- [ ] Add to frontend environment variables:
  ```
  NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
  ```
- [ ] Redeploy frontend

## Post-Deployment

### Verification
- [ ] Backend health check responds: `GET /health`
- [ ] Frontend loads without errors
- [ ] User can register/login
- [ ] Chat interface accessible
- [ ] Can create tasks via chat
- [ ] Can list tasks via chat
- [ ] Can complete tasks via chat
- [ ] Can delete tasks via chat
- [ ] Conversation history persists
- [ ] No CORS errors in browser console

### Monitoring
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Monitor OpenAI API usage and costs
- [ ] Set up uptime monitoring
- [ ] Configure alerts for errors
- [ ] Monitor database performance

### Security
- [ ] HTTPS enabled on both frontend and backend
- [ ] JWT_SECRET is strong and unique
- [ ] Database credentials are secure
- [ ] OpenAI API key is not exposed in frontend
- [ ] CORS configured correctly (not allowing all origins in production)
- [ ] Rate limiting configured (optional but recommended)

## Rollback Plan

If deployment fails:

1. **Backend Issues**:
   - [ ] Check logs for errors
   - [ ] Verify environment variables
   - [ ] Verify database connection
   - [ ] Roll back to previous version if needed

2. **Frontend Issues**:
   - [ ] Check browser console for errors
   - [ ] Verify API URL is correct
   - [ ] Check CORS configuration
   - [ ] Roll back to previous version if needed

3. **Database Issues**:
   - [ ] Verify connection string
   - [ ] Check if tables exist
   - [ ] Run migration script again if needed
   - [ ] Restore from backup if necessary

## Performance Optimization (Optional)

- [ ] Enable database connection pooling
- [ ] Add Redis for session caching
- [ ] Configure CDN for frontend assets
- [ ] Enable gzip compression
- [ ] Optimize database queries with indexes
- [ ] Set up database read replicas

## Cost Management

- [ ] Monitor OpenAI API usage
- [ ] Set spending limits on OpenAI account
- [ ] Monitor database storage usage
- [ ] Review hosting costs
- [ ] Consider caching strategies to reduce API calls

## Documentation

- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Create user guide for chat interface

## Success Criteria

✅ Backend deployed and accessible
✅ Frontend deployed and accessible
✅ Users can register and login
✅ Chat interface works end-to-end
✅ All task operations functional
✅ Conversation persistence verified
✅ No critical errors in logs
✅ Performance is acceptable
✅ Security measures in place

## Notes

- Keep OpenAI API key secure and never commit to git
- Monitor costs closely in first few days
- Have rollback plan ready
- Test thoroughly before announcing to users
- Consider gradual rollout to manage load
