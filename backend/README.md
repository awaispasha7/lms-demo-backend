# LMS Django Full-Stack Application

A complete Learning Management System built with Django, HTMX, and Tailwind CSS. Deployed on Vercel with Supabase database.

## Features

- ✅ **Django Full-Stack**: Server-side rendering with HTMX for dynamic updates
- ✅ **REST API**: Complete API matching OpenAPI specification (60+ endpoints)
- ✅ **Auto-Grading**: Automatic MCQ grading with AI-powered feedback
- ✅ **Supabase Integration**: PostgreSQL database via Supabase
- ✅ **Beautiful UI**: Modern design with Tailwind CSS
- ✅ **Vercel Ready**: Configured for serverless deployment

## Tech Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: Supabase (PostgreSQL) or SQLite (local development)
- **Frontend**: Django Templates + HTMX + Tailwind CSS
- **AI**: OpenAI API for feedback generation
- **Deployment**: Vercel (serverless)

## Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env with your settings

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 4. Start server
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

### Production Deployment (Vercel)

See `VERCEL_SETUP_COMPLETE.md` for complete deployment guide.

**Quick steps:**
1. Set environment variables in Vercel Dashboard
2. Run `supabase_migration_complete.sql` in Supabase
3. Deploy: `vercel --prod`

## Project Structure

```
backend/
├── assignments/      # Assignments & submissions
├── academics/         # Schools, classes, subjects
├── attendance/        # Attendance tracking
├── reports/          # Reports generation
├── policies/         # Policy management
├── users/            # User management
├── ai/               # AI endpoints
├── api/              # Vercel serverless entry
└── lms_backend/      # Django settings
```

## API Endpoints

All endpoints available at `/api/*`:

- `/api/users/` - User management
- `/api/academics/` - Schools, classes, subjects
- `/api/assignments/` - Assignments & submissions
- `/api/attendance/` - Attendance tracking
- `/api/reports/` - Report generation
- `/api/policies/` - Policy management
- `/api/ai/` - AI features

See API documentation at `/redoc/` (if configured).

## Database

- **Local**: SQLite (default)
- **Production**: Supabase PostgreSQL

Set `USE_SUPABASE=True` in `.env` to use Supabase.

## Documentation

- `QUICK_START.md` - Quick setup guide
- `VERCEL_SETUP_COMPLETE.md` - Vercel deployment guide
- `SUPABASE_PASSWORD_RECOVERY.md` - How to get Supabase password

## License

MIT
