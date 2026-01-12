"""Tests for user profile endpoints."""
import requests
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class TestUsers:
    """Test user profile endpoints."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def test_get_profile(self) -> bool:
        """Test get user profile."""
        print("\n[TEST] Get User Profile")
        
        try:
            response = requests.get(f"{API_BASE}/users/me", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Profile retrieved")
                print(f"  Email: {result.get('email')}")
                print(f"  Name: {result.get('first_name', 'N/A')} {result.get('last_name', 'N/A')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_update_profile(self) -> bool:
        """Test update user profile."""
        print("\n[TEST] Update User Profile")
        data = {
            "first_name": "Test",
            "last_name": "User",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        
        try:
            response = requests.put(f"{API_BASE}/users/me", json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Profile updated")
                print(f"  Name: {result.get('first_name')} {result.get('last_name')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False


if __name__ == "__main__":
    token = input("Enter access token: ").strip()
    if not token:
        print("Error: Access token required")
        exit(1)
    
    test = TestUsers(token)
    print("=" * 60)
    print("User Profile Tests")
    print("=" * 60)
    
    test.test_get_profile()
    test.test_update_profile()

