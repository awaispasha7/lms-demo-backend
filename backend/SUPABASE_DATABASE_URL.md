# Supabase DATABASE_URL Configuration for Vercel

## The Error
```
dj_database_url.UnknownSchemeError: Scheme 'https://' is unknown.
```

This means your `DATABASE_URL` in Vercel is set incorrectly.

## Correct Format

Your `DATABASE_URL` should be a **PostgreSQL connection string**, not an HTTPS URL.

### Format:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

### Example:
```
postgresql://postgres:your-password-here@db.abcdefghijklmnop.supabase.co:5432/postgres
```

## How to Get the Correct URL from Supabase

1. Go to **Supabase Dashboard** → Your Project
2. Click **Settings** (gear icon) → **Database**
3. Scroll down to **Connection string**
4. Select **URI** tab (not Session mode)
5. Copy the connection string - it should look like:
   ```
   postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
   OR
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
   ```

6. **Replace `[PASSWORD]`** with your actual database password
7. Copy the **entire string** including `postgresql://`

## Setting in Vercel

1. Go to **Vercel Dashboard** → Your Project → **Settings**
2. Click **Environment Variables**
3. Find or add `DATABASE_URL`
4. Paste the PostgreSQL connection string (starts with `postgresql://`)
5. Make sure it's set for **Production**, **Preview**, and **Development**
6. Click **Save**
7. **Redeploy** your application

## Common Mistakes

❌ **Wrong:**
```
https://abcdefghijklmnop.supabase.co
```
This is the Supabase project URL, not the database connection string.

❌ **Wrong:**
```
postgres://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```
While `postgres://` might work, `postgresql://` is preferred.

✅ **Correct:**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

## Password Special Characters

If your password contains special characters, you may need to URL-encode them:
- `@` becomes `%40`
- `#` becomes `%23`
- `$` becomes `%24`
- `%` becomes `%25`
- `&` becomes `%26`
- `+` becomes `%2B`
- `=` becomes `%3D`

## Testing the Connection

After setting the correct `DATABASE_URL`, redeploy and check the logs. You should see:
- No `UnknownSchemeError`
- Django initializes successfully
- Database connection works

## Alternative: Use Manual Database Config

If you prefer, you can set individual database variables instead of `DATABASE_URL`:

```
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password
SUPABASE_DB_HOST=db.[PROJECT].supabase.co
SUPABASE_DB_PORT=5432
```

The settings.py will use these if `DATABASE_URL` is not set.

