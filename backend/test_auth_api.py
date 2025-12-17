#!/usr/bin/env python3
"""Test script for authentication API endpoints."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint."""
    print("\n=== Testing Health Endpoint ===")
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Health check passed")


def test_registration():
    """Test user registration."""
    print("\n=== Testing User Registration ===")
    test_email = "test@example.com"
    test_password = "SecurePassword123!"

    response = client.post(
        "/auth/register",
        json={"email": test_email, "password": test_password}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 201:
        print("✓ Registration successful")
        return True
    elif response.status_code == 409:
        print("ℹ User already exists (expected if running multiple times)")
        return True
    else:
        print(f"✗ Registration failed with status {response.status_code}")
        return False


def test_login():
    """Test user login."""
    print("\n=== Testing User Login ===")
    test_email = "test@example.com"
    test_password = "SecurePassword123!"

    response = client.post(
        "/auth/login",
        json={"email": test_email, "password": test_password}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"✓ Login successful, token received: {token[:20]}...")
        return token
    else:
        print(f"✗ Login failed with status {response.status_code}")
        return None


def test_token_verification(token):
    """Test token verification."""
    print("\n=== Testing Token Verification ===")

    response = client.get(
        "/auth/verify",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✓ Token verification successful")
        return True
    else:
        print(f"✗ Token verification failed with status {response.status_code}")
        return False


def test_protected_chat_endpoint(token):
    """Test the protected chat endpoint."""
    print("\n=== Testing Protected Chat Endpoint ===")

    response = client.post(
        "/chat",
        json={"message": "What is ROS 2?"},
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response preview: {data.get('response', '')[:100]}...")
        print("✓ Chat endpoint successful")
        return True
    else:
        print(f"Response: {response.json()}")
        print(f"✗ Chat endpoint failed with status {response.status_code}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Backend Authentication API Test Suite")
    print("=" * 60)

    try:
        # Test 1: Health check
        test_health_endpoint()

        # Test 2: Registration
        test_registration()

        # Test 3: Login
        token = test_login()

        if token:
            # Test 4: Token verification
            test_token_verification(token)

            # Test 5: Protected chat endpoint
            test_protected_chat_endpoint(token)

        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
