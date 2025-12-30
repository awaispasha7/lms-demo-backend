# PowerShell Script to Test Client's Backend API
# Tests if the backend has data and is connected to a database

$baseUrl = "http://3.226.252.253:8000"
$token = $null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Client's Backend API" -ForegroundColor Cyan
Write-Host "URL: $baseUrl" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 0: Try to get authentication token (optional)
Write-Host "Step 0: Checking Authentication..." -ForegroundColor Yellow
Write-Host "Note: Endpoints require authentication. You can:" -ForegroundColor Gray
Write-Host "  1. Provide credentials to login and get a token" -ForegroundColor Gray
Write-Host "  2. Skip authentication (will test without token)" -ForegroundColor Gray
Write-Host ""

$useAuth = Read-Host "Do you want to login? (y/n)"
if ($useAuth -eq "y" -or $useAuth -eq "Y") {
    $email = Read-Host "Enter email"
    $password = Read-Host "Enter password" -AsSecureString
    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    
    try {
        $loginBody = @{
            email = $email
            password = $plainPassword
        } | ConvertTo-Json
        
        $loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/users/login/" -Method Post -Body $loginBody -ContentType "application/json" -ErrorAction Stop
        $token = $loginResponse.token
        Write-Host "✅ Login successful! Token obtained." -ForegroundColor Green
        Write-Host "   Token: $($token.Substring(0, [Math]::Min(20, $token.Length)))..." -ForegroundColor Gray
    } catch {
        $errorMsg = $_.Exception.Message
        Write-Host "❌ Login failed: $errorMsg" -ForegroundColor Red
        
        # Try to get more details from the error response
        if ($_.Exception.Response) {
            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $responseBody = $reader.ReadToEnd()
                Write-Host "   Error details: $responseBody" -ForegroundColor Yellow
            } catch {
                # Couldn't read response body
            }
        }
        
        Write-Host ""
        Write-Host "Possible reasons:" -ForegroundColor Yellow
        Write-Host "  1. User doesn't exist in database" -ForegroundColor Gray
        Write-Host "  2. Wrong password" -ForegroundColor Gray
        Write-Host "  3. Endpoint format is different" -ForegroundColor Gray
        Write-Host "  4. User needs to be registered first" -ForegroundColor Gray
        Write-Host ""
        
        $tryRegister = Read-Host "Would you like to try registering this user? (y/n)"
        if ($tryRegister -eq "y" -or $tryRegister -eq "Y") {
            Write-Host "Attempting to register user..." -ForegroundColor Yellow
            try {
                $registerBody = @{
                    username = $email.Split('@')[0]
                    email = $email
                    password = $plainPassword
                    role = "STUDENT"
                } | ConvertTo-Json
                
                $registerResponse = Invoke-RestMethod -Uri "$baseUrl/api/users/register/" -Method Post -Body $registerBody -ContentType "application/json" -ErrorAction Stop
                $token = $registerResponse.token
                Write-Host "✅ Registration successful! Token obtained." -ForegroundColor Green
                Write-Host "   Token: $($token.Substring(0, [Math]::Min(20, $token.Length)))..." -ForegroundColor Gray
            } catch {
                Write-Host "❌ Registration also failed: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "   Will test without authentication (will likely get 401 errors)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   Will test without authentication (will likely get 401 errors)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Skipping authentication. Testing without token..." -ForegroundColor Yellow
}
Write-Host ""

# Prepare headers
$headers = @{}
if ($token) {
    $headers["Authorization"] = "Token $token"
}

# Test 1: Check if API is accessible
Write-Host "Test 1: Checking API Health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "✅ API is accessible!" -ForegroundColor Green
    Write-Host "Response: $($healthResponse | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ API Health endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "   Status Code: $statusCode" -ForegroundColor Red
        if ($statusCode -eq 401) {
            Write-Host "   → This endpoint requires authentication" -ForegroundColor Yellow
        }
    }
    Write-Host "Trying /api/info instead..." -ForegroundColor Yellow
    try {
        $infoResponse = Invoke-RestMethod -Uri "$baseUrl/api/info" -Method Get -Headers $headers -ErrorAction Stop
        Write-Host "✅ API Info endpoint works!" -ForegroundColor Green
        Write-Host "Response: $($infoResponse | ConvertTo-Json)" -ForegroundColor Gray
    } catch {
        Write-Host "❌ API Info endpoint also failed" -ForegroundColor Red
    }
}
Write-Host ""

# Test 2: Check Assignments (most likely to have data)
Write-Host "Test 2: Checking Assignments..." -ForegroundColor Yellow
try {
    $assignmentsResponse = Invoke-RestMethod -Uri "$baseUrl/api/assignments/assignments/" -Method Get -Headers $headers -ErrorAction Stop
    $count = $assignmentsResponse.count
    $results = $assignmentsResponse.results
    
    if ($count -gt 0) {
        Write-Host "✅ Assignments endpoint has DATA!" -ForegroundColor Green
        Write-Host "   Total assignments: $count" -ForegroundColor Green
        Write-Host "   First few assignments:" -ForegroundColor Gray
        $results | Select-Object -First 3 | ForEach-Object {
            Write-Host "   - ID: $($_.id), Title: $($_.title)" -ForegroundColor Gray
        }
    } else {
        Write-Host "⚠️  Assignments endpoint works but has NO DATA (empty)" -ForegroundColor Yellow
        Write-Host "   Database is connected but empty" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Assignments endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "   Status Code: $statusCode" -ForegroundColor Red
    }
}
Write-Host ""

# Test 3: Check Schools (academics)
Write-Host "Test 3: Checking Schools..." -ForegroundColor Yellow
try {
    $schoolsResponse = Invoke-RestMethod -Uri "$baseUrl/api/academics/schools/" -Method Get -Headers $headers -ErrorAction Stop
    $count = $schoolsResponse.count
    $results = $schoolsResponse.results
    
    if ($count -gt 0) {
        Write-Host "✅ Schools endpoint has DATA!" -ForegroundColor Green
        Write-Host "   Total schools: $count" -ForegroundColor Green
        $results | Select-Object -First 3 | ForEach-Object {
            Write-Host "   - ID: $($_.id), Name: $($_.name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "⚠️  Schools endpoint works but has NO DATA" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Schools endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Check Users
Write-Host "Test 4: Checking Users..." -ForegroundColor Yellow
try {
    $usersResponse = Invoke-RestMethod -Uri "$baseUrl/api/users/users/" -Method Get -Headers $headers -ErrorAction Stop
    $count = $usersResponse.count
    $results = $usersResponse.results
    
    if ($count -gt 0) {
        Write-Host "✅ Users endpoint has DATA!" -ForegroundColor Green
        Write-Host "   Total users: $count" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Users endpoint works but has NO DATA" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Users endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 5: Check Submissions
Write-Host "Test 5: Checking Submissions..." -ForegroundColor Yellow
try {
    $submissionsResponse = Invoke-RestMethod -Uri "$baseUrl/api/assignments/submissions/" -Method Get -Headers $headers -ErrorAction Stop
    $count = $submissionsResponse.count
    $results = $submissionsResponse.results
    
    if ($count -gt 0) {
        Write-Host "✅ Submissions endpoint has DATA!" -ForegroundColor Green
        Write-Host "   Total submissions: $count" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Submissions endpoint works but has NO DATA" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Submissions endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you see ✅ with data counts > 0:" -ForegroundColor Green
Write-Host "  → Backend IS connected to database WITH DATA" -ForegroundColor Green
Write-Host "  → Use the SAME database for Django" -ForegroundColor Green
Write-Host ""
Write-Host "If you see ⚠️  (endpoints work but empty):" -ForegroundColor Yellow
Write-Host "  → Backend IS connected to database but NO DATA" -ForegroundColor Yellow
Write-Host "  → Database exists but is empty" -ForegroundColor Yellow
Write-Host ""
Write-Host "If you see ❌ (endpoints fail):" -ForegroundColor Red
Write-Host "  → Backend might not be connected to database" -ForegroundColor Red
Write-Host "  → Or endpoints require authentication (401 = needs token)" -ForegroundColor Red
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Authentication Info" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The API uses Token Authentication." -ForegroundColor Yellow
Write-Host "To get a token, login at:" -ForegroundColor Yellow
Write-Host "  POST $baseUrl/api/users/login/" -ForegroundColor Gray
Write-Host "  Body: { 'email': 'your@email.com', 'password': 'yourpassword' }" -ForegroundColor Gray
Write-Host ""
Write-Host "Then use the token in headers:" -ForegroundColor Yellow
Write-Host "  Authorization: Token <your-token>" -ForegroundColor Gray
Write-Host ""

