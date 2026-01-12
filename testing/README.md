# API Testing Suite

This directory contains comprehensive tests for the Interactive Classroom Platform API.

## Test Files

- `test_api.py` - Main comprehensive test script (all endpoints)
- `test_auth.py` - Authentication tests (register, verify, login)
- `test_users.py` - User profile tests
- `test_workspaces.py` - Workspace management tests
- `test_sessions.py` - Session management tests
- `test_integration.py` - Complete integration flow tests
- `test_errors.py` - Error handling and edge case tests

## Running Tests

### Prerequisites

1. Install dependencies:
```bash
pip install requests
```

2. Start the API server:
```bash
cd api
uvicorn main:app --reload
```

### Run Individual Test Files

```bash
# Authentication tests
python testing/test_auth.py

# User profile tests
python testing/test_users.py

# Workspace tests
python testing/test_workspaces.py

# Session tests
python testing/test_sessions.py

# Integration tests
python testing/test_integration.py

# Error handling tests
python testing/test_errors.py
```

### Run All Tests

```bash
python testing/test_api.py
```

## Test Configuration

Default API base URL: `http://localhost:8000`

To change the base URL, modify the `BASE_URL` constant in each test file.

## Notes

- Some tests require manual input (e.g., verification codes)
- Tests create test data that may persist in the database
- Use a test database or clean up after tests

