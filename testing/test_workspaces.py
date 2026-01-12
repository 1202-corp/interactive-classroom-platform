"""Tests for workspace endpoints."""
import requests
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class TestWorkspaces:
    """Test workspace endpoints."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.workspace_id = None
    
    def test_create_workspace(self) -> bool:
        """Test create workspace."""
        print("\n[TEST] Create Workspace")
        data = {
            "name": "Test Workspace",
            "description": "This is a test workspace",
            "session_settings": {"anonymous_mode": True}
        }
        
        try:
            response = requests.post(f"{API_BASE}/workspaces", json=data, headers=self.headers)
            if response.status_code == 201:
                result = response.json()
                self.workspace_id = result.get("id")
                print(f"✓ PASS: Workspace created (ID: {self.workspace_id})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_list_workspaces(self) -> bool:
        """Test list workspaces."""
        print("\n[TEST] List Workspaces")
        
        try:
            response = requests.get(f"{API_BASE}/workspaces", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Found {result.get('total', 0)} workspaces")
                for ws in result.get("workspaces", [])[:5]:
                    print(f"  - {ws.get('name')} (ID: {ws.get('id')}, Status: {ws.get('status')})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_get_workspace(self) -> bool:
        """Test get workspace."""
        print("\n[TEST] Get Workspace")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        try:
            response = requests.get(f"{API_BASE}/workspaces/{self.workspace_id}", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Workspace retrieved: {result.get('name')}")
                print(f"  Sessions: {result.get('session_count')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_update_workspace(self) -> bool:
        """Test update workspace."""
        print("\n[TEST] Update Workspace")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        data = {
            "name": "Updated Workspace Name",
            "description": "Updated description"
        }
        
        try:
            response = requests.put(f"{API_BASE}/workspaces/{self.workspace_id}", json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Workspace updated: {result.get('name')}")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_archive_workspace(self) -> bool:
        """Test archive workspace."""
        print("\n[TEST] Archive Workspace")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/workspaces/{self.workspace_id}/archive", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Workspace archived (Status: {result.get('status')})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_unarchive_workspace(self) -> bool:
        """Test unarchive workspace."""
        print("\n[TEST] Unarchive Workspace")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/workspaces/{self.workspace_id}/unarchive", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Workspace unarchived (Status: {result.get('status')})")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_delete_workspace(self) -> bool:
        """Test delete workspace (soft delete)."""
        print("\n[TEST] Delete Workspace (Soft Delete)")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        try:
            response = requests.delete(f"{API_BASE}/workspaces/{self.workspace_id}", headers=self.headers)
            if response.status_code == 204:
                print(f"✓ PASS: Workspace deleted (soft delete)")
                return True
            else:
                print(f"✗ FAIL: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ FAIL: {str(e)}")
            return False
    
    def test_restore_workspace(self) -> bool:
        """Test restore workspace from trash."""
        print("\n[TEST] Restore Workspace from Trash")
        
        if not self.workspace_id:
            print("✗ FAIL: No workspace ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/workspaces/{self.workspace_id}/restore", headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ PASS: Workspace restored (ID: {result.get('id')})")
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
    
    test = TestWorkspaces(token)
    print("=" * 60)
    print("Workspace Tests")
    print("=" * 60)
    
    test.test_create_workspace()
    test.test_list_workspaces()
    test.test_get_workspace()
    test.test_update_workspace()
    test.test_archive_workspace()
    test.test_unarchive_workspace()
    test.test_delete_workspace()
    test.test_restore_workspace()

