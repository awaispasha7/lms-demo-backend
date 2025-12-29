"""
Simple API testing script
Run: python test_api.py
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"
errors = []

def test_endpoint(name, method, url, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        if response.status_code == expected_status:
            print(f"✅ {name}: PASSED")
            return True
        else:
            print(f"❌ {name}: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            errors.append(f"{name}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        errors.append(f"{name}: {str(e)}")
        return False

def main():
    print("🧪 Starting API Tests...\n")
    
    # Test 1: Health Check
    test_endpoint(
        "Health Check",
        "GET",
        f"{BASE_URL}/assignments/api/health"
    )
    
    # Test 2: API Info
    test_endpoint(
        "API Info",
        "GET",
        f"{BASE_URL}/assignments/api/info"
    )
    
    # Test 3: User Registration
    registration_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "STUDENT"
    }
    registration_success = test_endpoint(
        "User Registration",
        "POST",
        f"{BASE_URL}/users/register/",
        data=registration_data,
        expected_status=201
    )
    
    # Test 4: User Login
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    login_response = None
    if test_endpoint(
        "User Login",
        "POST",
        f"{BASE_URL}/users/login/",
        data=login_data,
        expected_status=201
    ):
        try:
            login_response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
            token = login_response.json().get('token')
            if token:
                headers = {"Authorization": f"Token {token}"}
                
                # Test 5: Get Profile
                test_endpoint(
                    "Get Profile",
                    "GET",
                    f"{BASE_URL}/users/profile/",
                    headers=headers
                )
        except:
            pass
    
    # Test 6: List Academic Years
    test_endpoint(
        "List Academic Years",
        "GET",
        f"{BASE_URL}/academics/academic-years/"
    )
    
    # Test 7: List Schools
    test_endpoint(
        "List Schools",
        "GET",
        f"{BASE_URL}/academics/schools/"
    )
    
    # Test 8: List Assignments
    test_endpoint(
        "List Assignments",
        "GET",
        f"{BASE_URL}/assignments/assignments/"
    )
    
    # Test 9: List Submissions
    test_endpoint(
        "List Submissions",
        "GET",
        f"{BASE_URL}/assignments/submissions/"
    )
    
    # Test 10: List Attendance
    test_endpoint(
        "List Attendance",
        "GET",
        f"{BASE_URL}/attendance/attendance/"
    )
    
    # Test 11: AI Endpoints
    test_endpoint(
        "At-Risk Students",
        "GET",
        f"{BASE_URL}/ai/at-risk-students/"
    )
    
    test_endpoint(
        "Bias Alerts",
        "GET",
        f"{BASE_URL}/ai/bias-alerts/"
    )
    
    # Summary
    print("\n" + "="*50)
    if errors:
        print(f"❌ Tests completed with {len(errors)} error(s)")
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()

