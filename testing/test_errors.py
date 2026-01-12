"""Tests for error handling and edge cases."""
import requests
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class TestErrors:
    """Test error handling and edge cases."""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    
    def test_invalid_email_format(self) -> bool:
        """Test registration with invalid email format."""
        print("\n[TEST] Invalid Email Format")
        data = {"email": "invalid-email", "password": "test123"}
        
        try:
            response = requests.post(f"{API_BASE}/auth/register", json=data)
            if response.status_code == 422:
                print("✓ PASS: Correctly rejected invalid email")
                return True
            else:
                print(f"✗ FAIL: Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_short_password(self) -> bool:
        """Test registration with short password."""
        print("\n[TEST] Short Password")
        data = {"email": "test@example.com", "password": "short"}
        
        try:
            response = requests.post(f"{API_BASE}/auth/register", json=data)
            if response.status_code == 422:
                print("✓ PASS: Correctly rejected short password")
                return True
            else:
                print(f"✗ FAIL: Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_duplicate_email(self) -> bool:
        """Test registration with duplicate email."""
        print("\n[TEST] Duplicate Email")
        email = f"duplicate_{hash('test') % 10000}@example.com"
        
        # First registration
        data = {"email": email, "password": "testpassword123"}
        requests.post(f"{API_BASE}/auth/register", json=data)
        
        # Second registration (should fail)
        try:
            response = requests.post(f"{API_BASE}/auth/register", json=data)
            if response.status_code == 400:
                print("✓ PASS: Correctly rejected duplicate email")
                return True
            else:
                print(f"✗ FAIL: Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_invalid_verification_code(self) -> bool:
        """Test verification with invalid code."""
        print("\n[TEST] Invalid Verification Code")
        email = f"invalid_code_{hash('test') % 10000}@example.com"
        
        # Register first
        data = {"email": email, "password": "testpassword123"}
        requests.post(f"{API_BASE}/auth/register", json=data)
        
        # Try invalid code
        data = {"email": email, "code": "000000"}
        try:
            response = requests.post(f"{API_BASE}/auth/verify-email", json=data)
            if response.status_code == 400:
                print("✓ PASS: Correctly rejected invalid code")
                return True
            else:
                print(f"✗ FAIL: Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_unauthorized_access(self) -> bool:
        """Test accessing protected endpoint without token."""
        print("\n[TEST] Unauthorized Access")
        
        try:
            response = requests.get(f"{API_BASE}/users/me")
            if response.status_code == 401:
                print("✓ PASS: Correctly rejected unauthorized access")
                return True
            else:
                print(f"✗ FAIL: Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_invalid_token(self) -> bool:
        """Test accessing protected endpoint with invalid token."""
        print("\n[TEST] Invalid Token")
        headers = {"Authorization": "Bearer invalid_token_12345"}
        
        try:
            response = requests.get(f"{API_BASE}/users/me", headers=headers)
            if response.status_code == 401:
                print("✓ PASS: Correctly rejected invalid token")
                return True
            else:
                print(f"✗ FAIL: Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_nonexistent_workspace(self) -> bool:
        """Test accessing nonexistent workspace."""
        print("\n[TEST] Nonexistent Workspace")
        
        if not self.access_token:
            print("⊘ SKIP: No access token")
            return True
        
        try:
            response = requests.get(f"{API_BASE}/workspaces/99999", headers=self.headers)
            if response.status_code == 404:
                print("✓ PASS: Correctly returned 404 for nonexistent workspace")
                return True
            else:
                print(f"✗ FAIL: Expected 404, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_nonexistent_session(self) -> bool:
        """Test accessing nonexistent session."""
        print("\n[TEST] Nonexistent Session")
        
        if not self.access_token:
            print("⊘ SKIP: No access token")
            return True
        
        try:
            response = requests.get(f"{API_BASE}/sessions/99999", headers=self.headers)
            if response.status_code == 404:
                print("✓ PASS: Correctly returned 404 for nonexistent session")
                return True
            else:
                print(f"✗ FAIL: Expected 404, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False


if __name__ == "__main__":
    token = input("Enter access token (or press Enter to skip auth tests): ").strip()
    test = TestErrors(token if token else None)
    
    print("=" * 60)
    print("Error Handling Tests")
    print("=" * 60)
    
    test.test_invalid_email_format()
    test.test_short_password()
    test.test_duplicate_email()
    test.test_invalid_verification_code()
    test.test_unauthorized_access()
    test.test_invalid_token()
    test.test_nonexistent_workspace()
    test.test_nonexistent_session()

