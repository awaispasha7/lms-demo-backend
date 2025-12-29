# Django SECRET_KEY Guide

## What is SECRET_KEY?

The `SECRET_KEY` is a critical Django setting used for:
- **Cryptographic signing** - Signing sessions, cookies, CSRF tokens
- **Password reset tokens** - Generating secure password reset links
- **Session security** - Encrypting session data
- **CSRF protection** - Generating CSRF tokens

## Why It's Important

⚠️ **NEVER commit your SECRET_KEY to version control!**
- If exposed, attackers can forge sessions, cookies, and tokens
- Always use environment variables for production

## Current Configuration

In `lms_backend/settings.py`:
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-demo-key-change-in-production')
```

This means:
- ✅ It reads from environment variable `SECRET_KEY` first
- ⚠️ Falls back to an insecure default (only for local development)

## Generate a New SECRET_KEY

### Option 1: Using Django (Recommended)
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Option 2: Using Python directly
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Option 3: Online Generator
Visit: https://djecrety.ir/ (generates Django secret keys)

## Generated Key Example

Here's a fresh key generated for you:
```
=n62&o@ef$hvo=w7060-xj47%&^$ue=&mpc*5*v2ty4ymr5vf=
```

**⚠️ Don't use this exact key - generate your own!**

## Setting SECRET_KEY for Vercel

### Step 1: Generate Your Key
Run the command above to get your unique key.

### Step 2: Add to Vercel Environment Variables

1. Go to **Vercel Dashboard** → Your Project
2. Click **Settings** → **Environment Variables**
3. Click **Add New**
4. Set:
   - **Key**: `SECRET_KEY`
   - **Value**: `your-generated-secret-key-here`
   - **Environment**: Select all (Production, Preview, Development)
5. Click **Save**

### Step 3: Redeploy
After adding the environment variable, Vercel will automatically redeploy, or you can manually trigger a new deployment.

## Local Development

### Option 1: Create `.env` file (Recommended)
Create a `.env` file in the `backend/` directory:
```
SECRET_KEY=your-generated-secret-key-here
```

Make sure `.env` is in `.gitignore`:
```
.env
```

### Option 2: Set Environment Variable
**Windows (PowerShell):**
```powershell
$env:SECRET_KEY="your-generated-secret-key-here"
```

**Windows (CMD):**
```cmd
set SECRET_KEY=your-generated-secret-key-here
```

**Linux/Mac:**
```bash
export SECRET_KEY="your-generated-secret-key-here"
```

## Security Best Practices

1. ✅ **Use different keys for different environments**
   - Production: Strong, unique key
   - Development: Can use a simpler key (but still secure)
   - Testing: Can use a fixed key for consistency

2. ✅ **Never commit keys to Git**
   - Add `.env` to `.gitignore`
   - Never hardcode in settings.py

3. ✅ **Rotate keys if compromised**
   - If a key is exposed, generate a new one immediately
   - Note: This will invalidate all existing sessions

4. ✅ **Use strong, random keys**
   - At least 50 characters
   - Mix of letters, numbers, and symbols

## Current Status

Your current setup:
- ✅ Reads from environment variable (good!)
- ⚠️ Has an insecure default (only for local dev)
- ✅ Ready for Vercel deployment (just need to set the env var)

## Quick Checklist

- [ ] Generate a new SECRET_KEY
- [ ] Add it to Vercel Environment Variables
- [ ] Create `.env` file for local development (optional)
- [ ] Add `.env` to `.gitignore` (if not already)
- [ ] Redeploy to Vercel

## Troubleshooting

**Error: "SECRET_KEY must not be empty"**
- Make sure you've set the environment variable
- Check Vercel dashboard → Environment Variables
- Verify the variable name is exactly `SECRET_KEY` (case-sensitive)

**Sessions not working after deployment**
- Verify SECRET_KEY is set correctly in Vercel
- Make sure you redeployed after adding the variable
- Check Vercel logs for any SECRET_KEY related errors

