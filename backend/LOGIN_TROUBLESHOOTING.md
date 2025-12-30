# Login Troubleshooting Guide

## Your Error: 400 Bad Request on Login

This means the login endpoint received your request but rejected it. Here's how to troubleshoot:

## Possible Causes

### 1. User Doesn't Exist
The email `affan4321@gmail.com` might not be in the database yet.

**Solution:** Try registering first:
```powershell
$registerBody = @{
    username = "affan"
    email = "affan4321@gmail.com"
    password = "your-password"
    role = "STUDENT"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/users/register/" -Method Post -Body $registerBody -ContentType "application/json"
$token = $response.token
```

### 2. Wrong Password
The password might be incorrect.

**Solution:** 
- Ask the client for the correct password
- Or reset the password if possible

### 3. Different Authentication Method
The client's backend might use a different authentication system (not Token auth).

**Solution:** Check the API docs at `http://3.226.252.253:8000/redoc/` to see:
- What authentication method is used
- What the login endpoint format is
- What fields are required

## Quick Test Commands

### Test 1: Check if Register Endpoint Works
```powershell
$registerBody = @{
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    role = "STUDENT"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/users/register/" -Method Post -Body $registerBody -ContentType "application/json"
    Write-Host "✅ Registration works! Token: $($response.token)" -ForegroundColor Green
} catch {
    Write-Host "❌ Registration failed: $($_.Exception.Message)" -ForegroundColor Red
}
```

### Test 2: Check Login Endpoint Details
```powershell
# Try to see what the error actually says
try {
    $loginBody = @{
        email = "affan4321@gmail.com"
        password = "your-password"
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/users/login/" -Method Post -Body $loginBody -ContentType "application/json"
} catch {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    Write-Host "Error response: $responseBody" -ForegroundColor Red
}
```

### Test 3: Check API Documentation
Visit `http://3.226.252.253:8000/redoc/` and look for:
- Authentication section
- Login endpoint details
- Required fields
- Expected format

## What We Know

✅ **Backend IS Running** - You got 400 (not 500 or connection error)
✅ **Backend IS Connected** - It's processing requests
✅ **Login Endpoint Exists** - It responded (not 404)
❌ **Login Failed** - Either user doesn't exist or format is wrong

## Next Steps

1. **Ask the client:**
   - "Does the user `affan4321@gmail.com` exist in the database?"
   - "What's the correct password?"
   - "Can you provide test credentials?"

2. **Try registering a new user:**
   - Use the register endpoint
   - Then login with those credentials

3. **Check the API docs:**
   - Visit `/redoc/` to see the exact format
   - Check if there are any required fields we're missing

4. **Try alternative authentication:**
   - The client might use JWT instead of Token
   - Or session-based auth
   - Check the docs for the correct method

## Updated Script

I've updated `test_api.ps1` to:
- Show detailed error messages
- Offer to try registration if login fails
- Display the actual error response from the server

Run it again and it will give you more information!

