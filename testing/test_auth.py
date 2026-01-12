"""Tests for authentication endpoints."""
import requests
import json
from typing import Optional, Dict, Any

BASE_URL = "http://localhost:6100"
API_BASE = f"{BASE_URL}/api/v1"


class TestAuth:
    """Test authentication endpoints."""
    
    def __init__(self):
        self.email = f"test_auth_{hash('test') % 10000}@example.com"
        self.password = "testpassword123"
        self.access_token = None
        self.user_id = None
    
    def test_register(self) -> bool:
        """Test user registration."""
        print("\n[TEST] User Registration")
        data = {"email": self.email, "password": self.password}
        
        try:
            response = requests.post(f"{API_BASE}/auth/register", json=data)
            if response.status_code == 201:
                result = response.json()
                self.user_id = result.get("user_id")
                print(f"✓ PASS: User registered (ID: {self.user_id})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_verify_email(self, code: str) -> bool:
        """Test email verification."""
        print("\n[TEST] Email Verification")
        data = {"email": self.email, "code": code}
        
        try:
            response = requests.post(f"{API_BASE}/auth/verify-email", json=data)
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                print(f"✓ PASS: Email verified, token received")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_login(self) -> bool:
        """Test user login."""
        print("\n[TEST] User Login")
        data = {"email": self.email, "password": self.password}
        
        try:
            response = requests.post(f"{API_BASE}/auth/login", json=data)
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                print(f"✓ PASS: Login successful")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_resend_code(self) -> bool:
        """Test resend verification code."""
        print("\n[TEST] Resend Verification Code")
        data = {"email": self.email}
        
        try:
            response = requests.post(f"{API_BASE}/auth/resend-code", json=data)
            if response.status_code == 200:
                print(f"✓ PASS: Code resent")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False


if __name__ == "__main__":
    test = TestAuth()
    print("=" * 60)
    print("Authentication Tests")
    print("=" * 60)
    
    test.test_register()
    code = input("\nEnter verification code (or press Enter to skip): ").strip()
    if code:
        test.test_verify_email(code)
    else:
        test.test_resend_code()
        code = input("Enter new verification code: ").strip()
        if code:
            test.test_verify_email(code)
    
    if test.access_token:
        test.test_login()

