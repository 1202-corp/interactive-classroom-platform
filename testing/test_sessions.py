"""Tests for session endpoints."""
import requests
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class TestSessions:
    """Test session endpoints."""
    
    def __init__(self, access_token: str, workspace_id: int):
        self.access_token = access_token
        self.workspace_id = workspace_id
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.session_id = None
    
    def test_create_session(self) -> bool:
        """Test create session."""
        print("\n[TEST] Create Session")
        data = {
            "name": "Test Session",
            "description": "This is a test session"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/workspaces/{self.workspace_id}/sessions",
                json=data,
                headers=self.headers
            )
            if response.status_code == 201:
                result = response.json()
                self.session_id = result.get("id")
                print(f"✓ PASS: Session created (ID: {self.session_id})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_list_sessions(self) -> bool:
        """Test list sessions."""
        print("\n[TEST] List Sessions")
        
        try:
            response = requests.get(
                f"{API_BASE}/workspaces/{self.workspace_id}/sessions",
                headers=self.headers
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Found {result.get('total', 0)} sessions")
                for s in result.get("sessions", [])[:5]:
                    print(f"  - {s.get('name')} (ID: {s.get('id')}, Status: {s.get('status')})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_get_session(self) -> bool:
        """Test get session."""
        print("\n[TEST] Get Session")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        try:
            response = requests.get(f"{API_BASE}/sessions/{self.session_id}", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Session retrieved: {result.get('name')}")
                print(f"  Status: {result.get('status')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_update_session(self) -> bool:
        """Test update session."""
        print("\n[TEST] Update Session")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        data = {
            "name": "Updated Session Name",
            "description": "Updated description"
        }
        
        try:
            response = requests.put(f"{API_BASE}/sessions/{self.session_id}", json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Session updated: {result.get('name')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_start_session(self) -> bool:
        """Test start session."""
        print("\n[TEST] Start Session")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/sessions/{self.session_id}/start", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Session started (Status: {result.get('status')})")
                print(f"  Start time: {result.get('start_datetime', 'N/A')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_stop_session(self) -> bool:
        """Test stop session."""
        print("\n[TEST] Stop Session")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/sessions/{self.session_id}/stop", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Session stopped (Status: {result.get('status')})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_delete_session(self) -> bool:
        """Test delete session (soft delete)."""
        print("\n[TEST] Delete Session (Soft Delete)")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        try:
            response = requests.delete(f"{API_BASE}/sessions/{self.session_id}", headers=self.headers)
            if response.status_code == 204:
                print(f"✓ PASS: Session deleted (soft delete)")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_restore_session(self) -> bool:
        """Test restore session from trash."""
        print("\n[TEST] Restore Session from Trash")
        
        if not self.session_id:
            print("✗ FAIL: No session ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/sessions/{self.session_id}/restore", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Session restored (ID: {result.get('id')})")
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
    
    workspace_id = input("Enter workspace ID: ").strip()
    if not workspace_id:
        print("Error: Workspace ID required")
        exit(1)
    
    test = TestSessions(token, int(workspace_id))
    print("=" * 60)
    print("Session Tests")
    print("=" * 60)
    
    test.test_create_session()
    test.test_list_sessions()
    test.test_get_session()
    test.test_update_session()
    test.test_start_session()
    test.test_stop_session()
    test.test_delete_session()
    test.test_restore_session()

