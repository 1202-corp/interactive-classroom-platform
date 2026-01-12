#!/usr/bin/env python3
"""Test script for Interactive Classroom Platform API."""
import requests
import json
import sys
from typing import Optional, Dict, Any

# Configuration
BASE_URL = "http://localhost:6100"
API_BASE = f"{BASE_URL}/api/v1"

# Test state
test_state = {
    "access_token": None,
    "user_id": None,
    "workspace_id": None,
    "session_id": None,
    "email": f"test_{hash('test') % 10000}@example.com",
    "password": "testpassword123"
}


def print_test(name: str):
    """Print test name."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")


def print_result(success: bool, message: str = ""):
    """Print test result."""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {message}")


def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    expected_status: int = 200
) -> Optional[Dict[str, Any]]:
    """Make HTTP request and return response."""
    url = f"{API_BASE}{endpoint}"
    
    if headers is None:
        headers = {}
    
    if test_state["access_token"]:
        headers["Authorization"] = f"Bearer {test_state['access_token']}"
    
    headers["Content-Type"] = "application/json"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print_result(False, f"Unknown method: {method}")
            return None
        
        if response.status_code != expected_status:
            print_result(False, f"Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text}")
            return None
        
        if response.status_code == 204:  # No Content
            return {}
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print_result(False, f"Request error: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print_result(False, f"JSON decode error: {str(e)}")
        return None


def test_register():
    """Test user registration."""
    print_test("User Registration")
    
    data = {
        "email": test_state["email"],
        "password": test_state["password"]
    }
    
    result = make_request("POST", "/auth/register", data=data, expected_status=201)
    
    if result and "user_id" in result:
        test_state["user_id"] = result["user_id"]
        print_result(True, f"User registered: {result['email']}")
        print(f"  User ID: {result['user_id']}")
        print(f"  Verification code sent: {result.get('verification_code_sent', False)}")
        return True
    else:
        print_result(False, "Registration failed")
        return False


def test_verify_email():
    """Test email verification."""
    print_test("Email Verification")
    
    print("  Note: In development mode, verification code is logged to console")
    print("  Please check the API logs for the verification code")
    code = input("  Enter verification code: ").strip()
    
    if not code:
        print_result(False, "No verification code provided")
        return False
    
    data = {
        "email": test_state["email"],
        "code": code
    }
    
    result = make_request("POST", "/auth/verify-email", data=data, expected_status=200)
    
    if result and "access_token" in result:
        test_state["access_token"] = result["access_token"]
        print_result(True, "Email verified and token received")
        print(f"  Access token: {result['access_token'][:20]}...")
        return True
    else:
        print_result(False, "Email verification failed")
        return False


def test_login():
    """Test user login."""
    print_test("User Login")
    
    data = {
        "email": test_state["email"],
        "password": test_state["password"]
    }
    
    result = make_request("POST", "/auth/login", data=data, expected_status=200)
    
    if result and "access_token" in result:
        test_state["access_token"] = result["access_token"]
        print_result(True, "Login successful")
        print(f"  Access token: {result['access_token'][:20]}...")
        return True
    else:
        print_result(False, "Login failed")
        return False


def test_get_profile():
    """Test get user profile."""
    print_test("Get User Profile")
    
    result = make_request("GET", "/users/me", expected_status=200)
    
    if result and "id" in result:
        print_result(True, f"Profile retrieved: {result['email']}")
        print(f"  Name: {result.get('first_name', 'N/A')} {result.get('last_name', 'N/A')}")
        return True
    else:
        print_result(False, "Get profile failed")
        return False


def test_update_profile():
    """Test update user profile."""
    print_test("Update User Profile")
    
    data = {
        "first_name": "Test",
        "last_name": "User",
        "avatar_url": "https://example.com/avatar.jpg"
    }
    
    result = make_request("PUT", "/users/me", data=data, expected_status=200)
    
    if result and "first_name" in result:
        print_result(True, "Profile updated")
        print(f"  Name: {result['first_name']} {result['last_name']}")
        return True
    else:
        print_result(False, "Update profile failed")
        return False


def test_create_workspace():
    """Test create workspace."""
    print_test("Create Workspace")
    
    data = {
        "name": "Test Workspace",
        "description": "This is a test workspace",
        "session_settings": {"anonymous_mode": True}
    }
    
    result = make_request("POST", "/workspaces", data=data, expected_status=201)
    
    if result and "id" in result:
        test_state["workspace_id"] = result["id"]
        print_result(True, f"Workspace created: {result['name']}")
        print(f"  Workspace ID: {result['id']}")
        print(f"  Status: {result['status']}")
        return True
    else:
        print_result(False, "Create workspace failed")
        return False


def test_list_workspaces():
    """Test list workspaces."""
    print_test("List Workspaces")
    
    result = make_request("GET", "/workspaces", expected_status=200)
    
    if result and "workspaces" in result:
        print_result(True, f"Found {result['total']} workspaces")
        for ws in result["workspaces"]:
            print(f"  - {ws['name']} (ID: {ws['id']}, Status: {ws['status']})")
        return True
    else:
        print_result(False, "List workspaces failed")
        return False


def test_get_workspace():
    """Test get workspace."""
    print_test("Get Workspace")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("GET", f"/workspaces/{test_state['workspace_id']}", expected_status=200)
    
    if result and "id" in result:
        print_result(True, f"Workspace retrieved: {result['name']}")
        print(f"  Description: {result.get('description', 'N/A')}")
        print(f"  Sessions: {result['session_count']}")
        return True
    else:
        print_result(False, "Get workspace failed")
        return False


def test_archive_workspace():
    """Test archive workspace."""
    print_test("Archive Workspace")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("POST", f"/workspaces/{test_state['workspace_id']}/archive", expected_status=200)
    
    if result and "status" in result:
        print_result(True, f"Workspace archived: {result['status']}")
        return True
    else:
        print_result(False, "Archive workspace failed")
        return False


def test_unarchive_workspace():
    """Test unarchive workspace."""
    print_test("Unarchive Workspace")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("POST", f"/workspaces/{test_state['workspace_id']}/unarchive", expected_status=200)
    
    if result and "status" in result:
        print_result(True, f"Workspace unarchived: {result['status']}")
        return True
    else:
        print_result(False, "Unarchive workspace failed")
        return False


def test_create_session():
    """Test create session."""
    print_test("Create Session")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    data = {
        "name": "Test Session",
        "description": "This is a test session"
    }
    
    result = make_request("POST", f"/workspaces/{test_state['workspace_id']}/sessions", data=data, expected_status=201)
    
    if result and "id" in result:
        test_state["session_id"] = result["id"]
        print_result(True, f"Session created: {result['name']}")
        print(f"  Session ID: {result['id']}")
        print(f"  Status: {result['status']}")
        return True
    else:
        print_result(False, "Create session failed")
        return False


def test_list_sessions():
    """Test list sessions."""
    print_test("List Sessions")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("GET", f"/workspaces/{test_state['workspace_id']}/sessions", expected_status=200)
    
    if result and "sessions" in result:
        print_result(True, f"Found {result['total']} sessions")
        for s in result["sessions"]:
            print(f"  - {s['name']} (ID: {s['id']}, Status: {s['status']})")
        return True
    else:
        print_result(False, "List sessions failed")
        return False


def test_start_session():
    """Test start session."""
    print_test("Start Session")
    
    if not test_state["session_id"]:
        print_result(False, "No session ID available")
        return False
    
    result = make_request("POST", f"/sessions/{test_state['session_id']}/start", expected_status=200)
    
    if result and "status" in result:
        print_result(True, f"Session started: {result['status']}")
        print(f"  Start time: {result.get('start_datetime', 'N/A')}")
        return True
    else:
        print_result(False, "Start session failed")
        return False


def test_stop_session():
    """Test stop session."""
    print_test("Stop Session")
    
    if not test_state["session_id"]:
        print_result(False, "No session ID available")
        return False
    
    result = make_request("POST", f"/sessions/{test_state['session_id']}/stop", expected_status=200)
    
    if result and "status" in result:
        print_result(True, f"Session stopped: {result['status']}")
        return True
    else:
        print_result(False, "Stop session failed")
        return False


def test_delete_session():
    """Test delete session."""
    print_test("Delete Session (Soft Delete)")
    
    if not test_state["session_id"]:
        print_result(False, "No session ID available")
        return False
    
    result = make_request("DELETE", f"/sessions/{test_state['session_id']}", expected_status=204)
    
    if result is not None:
        print_result(True, "Session deleted (soft delete)")
        return True
    else:
        print_result(False, "Delete session failed")
        return False


def test_restore_session():
    """Test restore session."""
    print_test("Restore Session")
    
    if not test_state["session_id"]:
        print_result(False, "No session ID available")
        return False
    
    result = make_request("POST", f"/sessions/{test_state['session_id']}/restore", expected_status=200)
    
    if result and "id" in result:
        print_result(True, "Session restored from trash")
        return True
    else:
        print_result(False, "Restore session failed")
        return False


def test_delete_workspace():
    """Test delete workspace."""
    print_test("Delete Workspace (Soft Delete)")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("DELETE", f"/workspaces/{test_state['workspace_id']}", expected_status=204)
    
    if result is not None:
        print_result(True, "Workspace deleted (soft delete)")
        return True
    else:
        print_result(False, "Delete workspace failed")
        return False


def test_restore_workspace():
    """Test restore workspace."""
    print_test("Restore Workspace")
    
    if not test_state["workspace_id"]:
        print_result(False, "No workspace ID available")
        return False
    
    result = make_request("POST", f"/workspaces/{test_state['workspace_id']}/restore", expected_status=200)
    
    if result and "id" in result:
        print_result(True, "Workspace restored from trash")
        return True
    else:
        print_result(False, "Restore workspace failed")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Interactive Classroom Platform API Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Email: {test_state['email']}")
    print("="*60)
    
    tests = [
        ("Registration", test_register),
        ("Email Verification", test_verify_email),
        ("Login", test_login),
        ("Get Profile", test_get_profile),
        ("Update Profile", test_update_profile),
        ("Create Workspace", test_create_workspace),
        ("List Workspaces", test_list_workspaces),
        ("Get Workspace", test_get_workspace),
        ("Create Session", test_create_session),
        ("List Sessions", test_list_sessions),
        ("Start Session", test_start_session),
        ("Stop Session", test_stop_session),
        ("Archive Workspace", test_archive_workspace),
        ("Unarchive Workspace", test_unarchive_workspace),
        ("Delete Session", test_delete_session),
        ("Restore Session", test_restore_session),
        ("Delete Workspace", test_delete_workspace),
        ("Restore Workspace", test_restore_workspace),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user")
            sys.exit(1)
        except Exception as e:
            print_result(False, f"Test error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

