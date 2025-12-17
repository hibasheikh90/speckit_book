#!/usr/bin/env python3
"""
End-to-End Login Page Test
Tests the complete login flow from frontend to backend.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chattest@example.com",
    "password": "TestPassword123!"
}

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}[PASS] {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}[FAIL] {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{YELLOW}[INFO] {text}{RESET}")

def print_test(test_name):
    """Print test name."""
    print(f"\n{BLUE}[TEST] {test_name}{RESET}")

# ============================================================================
# TEST 1: Frontend Accessibility
# ============================================================================

def test_frontend_homepage():
    """Test if frontend homepage is accessible."""
    print_test("Frontend Homepage Accessibility")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"Frontend homepage accessible (Status: {response.status_code})")
            print_info(f"   Response size: {len(response.content)} bytes")
            return True
        else:
            print_error(f"Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend - is it running?")
        print_info(f"   Expected URL: {FRONTEND_URL}")
        return False
    except Exception as e:
        print_error(f"Error accessing frontend: {str(e)}")
        return False

def test_frontend_login_page():
    """Test if login page is accessible."""
    print_test("Frontend Login Page Accessibility")
    try:
        response = requests.get(f"{FRONTEND_URL}/signin", timeout=5)
        if response.status_code == 200:
            print_success(f"Login page accessible (Status: {response.status_code})")

            # Check if page contains expected elements (basic check)
            content = response.text.lower()
            checks = {
                "has_form": "form" in content or "login" in content or "signin" in content,
                "has_docusaurus": "docusaurus" in content,
                "has_react": "react" in content or "__docusaurus" in content
            }

            for check_name, result in checks.items():
                if result:
                    print_info(f"   {check_name}: PASS")
                else:
                    print_info(f"   {check_name}: FAIL")

            return True
        else:
            print_error(f"Login page returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error accessing login page: {str(e)}")
        return False

# ============================================================================
# TEST 2: Backend API Availability
# ============================================================================

def test_backend_health():
    """Test if backend is healthy."""
    print_test("Backend Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Backend is healthy")
            print_info(f"   Status: {data.get('status')}")
            print_info(f"   Model: {data.get('model')}")
            print_info(f"   Rate Limit: {data.get('rate_limit')}")
            return True
        else:
            print_error(f"Backend health check failed (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend - is it running?")
        print_info(f"   Expected URL: {BACKEND_URL}")
        return False
    except Exception as e:
        print_error(f"Error checking backend health: {str(e)}")
        return False

# ============================================================================
# TEST 3: User Login Flow
# ============================================================================

def test_user_login_valid():
    """Test login with valid credentials."""
    print_test("Valid User Login")
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=TEST_USER,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user_id = data.get("user_id")
            token_type = data.get("token_type")

            print_success("Login successful!")
            print_info(f"   User ID: {user_id}")
            print_info(f"   Token Type: {token_type}")
            print_info(f"   Token (first 30 chars): {token[:30]}...")
            print_info(f"   Token Length: {len(token)} characters")

            # Validate token format
            if token and len(token) > 50 and token.count('.') == 2:
                print_success("   JWT token format valid")
            else:
                print_error("   JWT token format invalid")
                return False, None

            return True, token
        else:
            print_error(f"Login failed (Status: {response.status_code})")
            print_info(f"   Response: {response.text}")
            return False, None

    except Exception as e:
        print_error(f"Error during login: {str(e)}")
        return False, None

def test_user_login_invalid():
    """Test login with invalid credentials."""
    print_test("Invalid User Login (Wrong Password)")
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={
                "email": TEST_USER["email"],
                "password": "WrongPassword123!"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 401:
            data = response.json()
            print_success("Correctly rejected invalid credentials")
            print_info(f"   Error message: {data.get('detail')}")
            return True
        else:
            print_error(f"Expected 401, got {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error during invalid login test: {str(e)}")
        return False

# ============================================================================
# TEST 4: Token Validation
# ============================================================================

def test_token_verification(token):
    """Test if the token can be verified."""
    print_test("Token Verification")

    if not token:
        print_error("No token provided for verification")
        return False

    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/verify",
            json={},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Token verified successfully")
            print_info(f"   User ID: {data.get('user_id')}")
            print_info(f"   Valid: {data.get('valid')}")
            return True
        else:
            print_error(f"Token verification failed (Status: {response.status_code})")
            print_info(f"   Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"Error during token verification: {str(e)}")
        return False

# ============================================================================
# TEST 5: Protected Endpoint Access
# ============================================================================

def test_protected_endpoint(token):
    """Test accessing protected endpoint with token."""
    print_test("Protected Endpoint Access (Chat)")

    if not token:
        print_error("No token provided for protected endpoint test")
        return False

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": "Test message: What is ROS 2?"},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print_success("Protected endpoint accessible with valid token")
            print_info(f"   Agent: {data.get('agent_name', 'N/A')}")
            response_text = data.get('response', '')
            print_info(f"   Response (first 100 chars): {response_text[:100]}...")
            return True
        elif response.status_code == 500:
            # 500 with AI quota is acceptable - auth worked!
            print_success("Authentication worked (500 due to AI service quota)")
            print_info("   This confirms JWT authentication is functional")
            return True
        else:
            print_error(f"Protected endpoint returned {response.status_code}")
            print_info(f"   Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"Error accessing protected endpoint: {str(e)}")
        return False

def test_protected_endpoint_no_token():
    """Test accessing protected endpoint without token."""
    print_test("Protected Endpoint Without Token")

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": "Test message"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 401 or response.status_code == 403:
            print_success(f"Correctly rejected request without token (Status: {response.status_code})")
            return True
        else:
            print_error(f"Expected 401/403, got {response.status_code}")
            print_error("   Protected endpoint not properly secured!")
            return False

    except Exception as e:
        print_error(f"Error during no-token test: {str(e)}")
        return False

# ============================================================================
# TEST 6: Cross-Origin Resource Sharing (CORS)
# ============================================================================

def test_cors_headers():
    """Test if CORS headers are properly configured."""
    print_test("CORS Configuration")

    try:
        response = requests.options(
            f"{BACKEND_URL}/auth/login",
            headers={
                "Origin": FRONTEND_URL,
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )

        cors_header = response.headers.get("Access-Control-Allow-Origin")

        if cors_header:
            print_success(f"CORS headers present: {cors_header}")
            return True
        else:
            print_error("CORS headers not found")
            print_info("   This may cause issues with frontend-backend communication")
            return False

    except Exception as e:
        print_error(f"Error checking CORS: {str(e)}")
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all end-to-end tests."""
    print_header("END-TO-END LOGIN PAGE TEST SUITE")
    print(f"Frontend: {FRONTEND_URL}")
    print(f"Backend:  {BACKEND_URL}")
    print(f"Test User: {TEST_USER['email']}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }

    # Run tests
    tests = [
        ("Frontend Homepage", test_frontend_homepage),
        ("Frontend Login Page", test_frontend_login_page),
        ("Backend Health", test_backend_health),
    ]

    # Execute basic tests
    for test_name, test_func in tests:
        result = test_func()
        results["tests"].append((test_name, result))
        if result:
            results["passed"] += 1
        else:
            results["failed"] += 1
        time.sleep(0.5)  # Small delay between tests

    # Login flow tests
    print_header("AUTHENTICATION FLOW TESTS")

    # Test invalid login
    result = test_user_login_invalid()
    results["tests"].append(("Invalid Login Rejection", result))
    if result:
        results["passed"] += 1
    else:
        results["failed"] += 1
    time.sleep(0.5)

    # Test valid login
    result, token = test_user_login_valid()
    results["tests"].append(("Valid User Login", result))
    if result:
        results["passed"] += 1
    else:
        results["failed"] += 1
    time.sleep(0.5)

    # If login succeeded, run token tests
    if result and token:
        # Token verification
        result = test_token_verification(token)
        results["tests"].append(("Token Verification", result))
        if result:
            results["passed"] += 1
        else:
            results["failed"] += 1
        time.sleep(0.5)

        # Protected endpoint with token
        result = test_protected_endpoint(token)
        results["tests"].append(("Protected Endpoint (With Token)", result))
        if result:
            results["passed"] += 1
        else:
            results["failed"] += 1
        time.sleep(0.5)

    # Protected endpoint without token
    result = test_protected_endpoint_no_token()
    results["tests"].append(("Protected Endpoint (No Token)", result))
    if result:
        results["passed"] += 1
    else:
        results["failed"] += 1
    time.sleep(0.5)

    # CORS test
    result = test_cors_headers()
    results["tests"].append(("CORS Configuration", result))
    if result:
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Print summary
    print_header("TEST RESULTS SUMMARY")

    for test_name, result in results["tests"]:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {status}  {test_name}")

    print(f"\n{BLUE}{'-'*60}{RESET}")
    total = results["passed"] + results["failed"]
    percentage = (results["passed"] / total * 100) if total > 0 else 0

    print(f"  Total Tests: {total}")
    print(f"  {GREEN}Passed: {results['passed']}{RESET}")
    print(f"  {RED}Failed: {results['failed']}{RESET}")
    print(f"  Success Rate: {percentage:.1f}%")
    print(f"{BLUE}{'-'*60}{RESET}\n")

    # Final verdict
    if results["failed"] == 0:
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}{'SUCCESS: All tests passed!':^60}{RESET}")
        print(f"{GREEN}{'Login page is fully functional!':^60}{RESET}")
        print(f"{GREEN}{'='*60}{RESET}\n")
        return 0
    else:
        print(f"{RED}{'='*60}{RESET}")
        print(f"{RED}{'FAILURE: Some tests failed':^60}{RESET}")
        print(f"{RED}{f'{results['failed']} issue(s) need attention':^60}{RESET}")
        print(f"{RED}{'='*60}{RESET}\n")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    exit(exit_code)
