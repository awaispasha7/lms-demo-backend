# 🚀 Quick Start Guide

## Local Development (5 minutes)

### 1. Setup Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env and set:
# - SECRET_KEY (generate one)
# - USE_SUPABASE=False (for SQLite)
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Test
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- Health: http://localhost:8000/api/assignments/api/health

---

## Production Deployment

### Option 1: Supabase + Railway (Recommended)

1. **Run Supabase Migration**:
   - Go to Supabase SQL Editor
   - Run `supabase_migration_complete.sql`

2. **Deploy to Railway**:
   ```bash
   npm i -g @railway/cli
   railway login
   railway init
   railway variables set USE_SUPABASE=True
   railway variables set SUPABASE_DB_HOST=your-host
   # ... set all env vars
   railway up
   ```

### Option 2: Heroku

```bash
heroku create your-app
heroku config:set SECRET_KEY=your-key
heroku config:set USE_SUPABASE=True
# ... set all env vars
git push heroku main
```

---

## Testing Checklist

- [ ] Health check endpoint works
- [ ] User registration works
- [ ] User login works
- [ ] Can create school
- [ ] Can create assignment
- [ ] Can submit assignment
- [ ] Admin panel accessible
- [ ] All API endpoints respond

---

## Need Help?

See `VERCEL_SETUP_COMPLETE.md` for Vercel deployment or check the main `README.md`.

