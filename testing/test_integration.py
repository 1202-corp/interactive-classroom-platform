"""Integration tests for complete user flows."""
import requests
import time
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class TestIntegration:
    """Integration tests for complete flows."""
    
    def __init__(self):
        self.email = f"test_integration_{hash('test') % 10000}@example.com"
        self.password = "testpassword123"
        self.access_token = None
        self.user_id = None
        self.workspace_id = None
        self.session_id = None
    
    def get_headers(self):
        """Get headers with authentication."""
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def test_complete_flow(self) -> bool:
        """Test complete user flow: register -> verify -> login -> create workspace -> create session -> start -> stop."""
        print("\n" + "=" * 60)
        print("COMPLETE INTEGRATION TEST")
        print("=" * 60)
        
        # 1. Register
        print("\n[1/7] Registering user...")
        data = {"email": self.email, "password": self.password}
        response = requests.post(f"{API_BASE}/auth/register", json=data)
        if response.status_code != 201:
            print(f"✗ FAIL: Registration failed: {response.text}")
            return False
        result = response.json()
        self.user_id = result.get("user_id")
        print(f"✓ User registered (ID: {self.user_id})")
        
        # 2. Verify email (skip if code not provided)
        print("\n[2/7] Verifying email...")
        code = input("Enter verification code (or press Enter to skip): ").strip()
        if code:
            data = {"email": self.email, "code": code}
            response = requests.post(f"{API_BASE}/auth/verify-email", json=data)
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                print("✓ Email verified")
            else:
                print(f"✗ FAIL: Email verification failed: {response.text}")
                return False
        else:
            print("⊘ Skipped (no code provided)")
            return False
        
        # 3. Login
        print("\n[3/7] Logging in...")
        data = {"email": self.email, "password": self.password}
        response = requests.post(f"{API_BASE}/auth/login", json=data)
        if response.status_code != 200:
            print(f"✗ FAIL: Login failed: {response.text}")
            return False
        result = response.json()
        self.access_token = result.get("access_token")
        print("✓ Logged in")
        
        # 4. Create workspace
        print("\n[4/7] Creating workspace...")
        data = {
            "name": "Integration Test Workspace",
            "description": "Created during integration test"
        }
        response = requests.post(f"{API_BASE}/workspaces", json=data, headers=self.get_headers())
        if response.status_code != 201:
            print(f"✗ FAIL: Workspace creation failed: {response.text}")
            return False
        result = response.json()
        self.workspace_id = result.get("id")
        print(f"✓ Workspace created (ID: {self.workspace_id})")
        
        # 5. Create session
        print("\n[5/7] Creating session...")
        data = {
            "name": "Integration Test Session",
            "description": "Created during integration test"
        }
        response = requests.post(
            f"{API_BASE}/workspaces/{self.workspace_id}/sessions",
            json=data,
            headers=self.get_headers()
        )
        if response.status_code != 201:
            print(f"✗ FAIL: Session creation failed: {response.text}")
            return False
        result = response.json()
        self.session_id = result.get("id")
        print(f"✓ Session created (ID: {self.session_id})")
        
        # 6. Start session
        print("\n[6/7] Starting session...")
        response = requests.post(
            f"{API_BASE}/sessions/{self.session_id}/start",
            headers=self.get_headers()
        )
        if response.status_code != 200:
            print(f"✗ FAIL: Session start failed: {response.text}")
            return False
        result = response.json()
        print(f"✓ Session started (Status: {result.get('status')})")
        time.sleep(1)  # Wait a bit
        
        # 7. Stop session
        print("\n[7/7] Stopping session...")
        response = requests.post(
            f"{API_BASE}/sessions/{self.session_id}/stop",
            headers=self.get_headers()
        )
        if response.status_code != 200:
            print(f"✗ FAIL: Session stop failed: {response.text}")
            return False
        result = response.json()
        print(f"✓ Session stopped (Status: {result.get('status')})")
        
        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED")
        print("=" * 60)
        return True


if __name__ == "__main__":
    test = TestIntegration()
    test.test_complete_flow()

