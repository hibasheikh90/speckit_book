#!/usr/bin/env python3
"""Test live API endpoints."""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 60)
    print("TEST 1: Health Endpoint")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_registration(email, password):
    """Test user registration."""
    print("\n" + "=" * 60)
    print("TEST 2: User Registration")
    print("=" * 60)
    print(f"Email: {email}")
    print(f"Password: {password}")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [201, 409]  # Created or Already Exists
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_login(email, password):
    """Test user login."""
    print("\n" + "=" * 60)
    print("TEST 3: User Login")
    print("=" * 60)
    print(f"Email: {email}")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")

        if response.status_code == 200:
            token = data.get("access_token")
            print(f"\nToken (first 50 chars): {token[:50]}...")
            return token
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_verify(token):
    """Test token verification."""
    print("\n" + "=" * 60)
    print("TEST 4: Token Verification")
    print("=" * 60)
    try:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_chat(token, message):
    """Test protected chat endpoint."""
    print("\n" + "=" * 60)
    print("TEST 5: Protected Chat Endpoint")
    print("=" * 60)
    print(f"Message: {message}")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except requests.Timeout:
        print("ERROR: Request timed out")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("LIVE API TESTING SUITE")
    print("Backend URL: " + BASE_URL)
    print("=" * 60)

    results = {
        "health": False,
        "registration": False,
        "login": False,
        "verify": False,
        "chat": False
    }

    # Test 1: Health check
    results["health"] = test_health()
    if not results["health"]:
        print("\nFAILED: Backend server is not responding!")
        return 1

    time.sleep(1)

    # Test 2: Registration
    test_email = "livetest@example.com"
    test_password = "SecurePassword123!"
    results["registration"] = test_registration(test_email, test_password)

    time.sleep(1)

    # Test 3: Login
    token = test_login(test_email, test_password)
    results["login"] = token is not None

    if not token:
        print("\nFAILED: Could not obtain authentication token!")
        return 1

    time.sleep(1)

    # Test 4: Token verification
    results["verify"] = test_verify(token)

    time.sleep(1)

    # Test 5: Chat endpoint
    results["chat"] = test_chat(token, "What is ROS 2?")

    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.upper():20} {status}")

    print("=" * 60)

    all_passed = all(results.values())
    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
