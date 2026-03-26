#!/usr/bin/env python3
"""Test chat endpoint with authentication."""

import requests
import json

BASE_URL = "http://localhost:8000"

# Step 1: Login
print("Step 1: Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "chattest@example.com", "password": "TestPassword123!"}
)
print(f"Login Status: {login_response.status_code}")

if login_response.status_code != 200:
    print("Login failed!")
    print(login_response.json())
    exit(1)

token_data = login_response.json()
token = token_data["access_token"]
print(f"Token obtained: {token[:50]}...")

# Step 2: Test chat endpoint
print("\nStep 2: Testing chat endpoint...")
print(f"Authorization header: Bearer {token[:20]}...")

chat_response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "What is ROS 2?"},
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Chat Status: {chat_response.status_code}")
print(f"Response: {json.dumps(chat_response.json(), indent=2)}")

# Step 3: Check server logs
print("\nStep 3: If failed, check server logs for details")

if chat_response.status_code == 200:
    print("\n✓ SUCCESS: Chat endpoint works!")
else:
    print(f"\n✗ FAILED: Status {chat_response.status_code}")

    # Debug: Try to verify the token manually
    print("\nStep 4: Testing token verification endpoint...")
    verify_response = requests.post(
        f"{BASE_URL}/auth/verify",
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )
    print(f"Verify Status: {verify_response.status_code}")
    print(f"Verify Response: {json.dumps(verify_response.json(), indent=2)}")
