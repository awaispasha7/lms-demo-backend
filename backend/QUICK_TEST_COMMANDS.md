# Quick PowerShell Commands to Test Client's Backend

## Quick Test (Single Command)

```powershell
# Test if API is accessible
Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/health"

# Test Assignments endpoint (most likely to have data)
Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/assignments/assignments/"

# Test Schools endpoint
Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/academics/schools/"

# Test Users endpoint
Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/users/users/"
```

## Run Full Test Script

```powershell
# Navigate to backend folder
cd C:\Gspec\Ibrahim\lms-demo-backend\backend

# Run the test script
.\test_api.ps1
```

## Manual Testing Commands

### Test 1: Check API Health
```powershell
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/health"
$response | ConvertTo-Json
```

### Test 2: Check Assignments (Check for Data)
```powershell
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/assignments/assignments/"
Write-Host "Total assignments: $($response.count)"
if ($response.count -gt 0) {
    Write-Host "✅ HAS DATA!" -ForegroundColor Green
    $response.results | Select-Object -First 3
} else {
    Write-Host "⚠️  NO DATA (empty)" -ForegroundColor Yellow
}
```

### Test 3: Check Schools
```powershell
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/academics/schools/"
Write-Host "Total schools: $($response.count)"
$response.results | Select-Object -First 5
```

### Test 4: Check Submissions
```powershell
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/assignments/submissions/"
Write-Host "Total submissions: $($response.count)"
```

### Test 5: Check Users
```powershell
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/users/users/"
Write-Host "Total users: $($response.count)"
```

## If Endpoints Require Authentication

If you get authentication errors, you might need to add a token:

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN_HERE"
}
$response = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/assignments/assignments/" -Headers $headers
```

## What to Look For

### ✅ Backend HAS Data:
```
Total assignments: 15
✅ HAS DATA!
```
- **Action:** Use the SAME database for Django
- **Don't create a new database**
- **Be careful with migrations**

### ⚠️ Backend Works But Empty:
```
Total assignments: 0
⚠️  NO DATA (empty)
```
- **Action:** Database exists but is empty
- **Safe to run migrations**
- **No data to lose**

### ❌ Backend Not Connected:
```
Invoke-RestMethod: The remote server returned an error: (500) Internal Server Error
```
- **Action:** Backend might not be connected to database
- **Or:** Endpoints require authentication
- **Check with client**

## Quick One-Liner to Check Everything

```powershell
@("health", "assignments/assignments", "academics/schools", "users/users") | ForEach-Object {
    try {
        $r = Invoke-RestMethod -Uri "http://3.226.252.253:8000/api/$_" -ErrorAction SilentlyContinue
        Write-Host "$_`: $($r.count) items" -ForegroundColor $(if($r.count -gt 0){"Green"}else{"Yellow"})
    } catch {
        Write-Host "$_`: ❌ Failed" -ForegroundColor Red
    }
}
```

