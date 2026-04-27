# FastAPI Tests for Mergington High School Activities API

This directory contains comprehensive unit and integration tests for the FastAPI backend application.

## Test Structure

All tests follow the **AAA (Arrange-Act-Assert)** pattern for clarity and consistency:

- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results

### Test Files

- **`conftest.py`**: Pytest configuration and shared fixtures
  - `client`: FastAPI TestClient for making HTTP requests
  - `reset_activities`: Fixture that resets the activities database to initial state before each test

- **`test_activities_api.py`**: Main test suite with 18 tests organized into 5 test classes

## Test Coverage

### TestGetActivities (3 tests)
- ✅ Returns all available activities
- ✅ Returns activity details correctly
- ✅ Includes participants list in response

### TestSignupForActivity (6 tests)
- ✅ Successful signup for an activity
- ✅ Adds participant to activity
- ✅ Returns 404 for non-existent activity
- ✅ Returns 400 for duplicate signup
- ✅ Multiple students can signup for different activities
- ✅ Multiple students can signup for same activity

### TestUnregisterFromActivity (5 tests)
- ✅ Successful unregistration
- ✅ Removes participant from activity
- ✅ Returns 404 for non-existent activity
- ✅ Returns 400 for non-signed-up participant
- ✅ Student can re-signup after unregistering
- ✅ Unregistering one student doesn't affect others

### TestActivityCapacity (1 test)
- ✅ Availability badge calculation is correct

### TestActivityCardIntegration (2 tests)
- ✅ Complete signup and unregister workflow
- ✅ Multiple operations maintain correct state

## Running Tests

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test class:
```bash
python -m pytest tests/test_activities_api.py::TestSignupForActivity -v
```

Run specific test:
```bash
python -m pytest tests/test_activities_api.py::TestSignupForActivity::test_signup_for_activity_success -v
```

Run with coverage report:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Testing Best Practices

### AAA Pattern Example

Every test in this suite follows the Arrange-Act-Assert pattern:

```python
def test_signup_adds_participant_to_activity(self, client):
    """Test that signup adds the participant to the activity."""
    # Arrange - Set up test data
    email = "test@mergington.edu"
    activity = "Soccer Club"
    
    # Act - Execute the code being tested
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.get("/activities")
    data = response.json()
    
    # Assert - Verify the results
    assert email in data[activity]["participants"]
```

This pattern makes tests:
- **Readable**: Clear intent of setup, action, and verification
- **Maintainable**: Easy to understand what each section does
- **Debuggable**: Easier to identify which phase failed

## Dependencies

Ensure the following packages are installed:
- `fastapi` - Web framework
- `httpx` - HTTP client for testing
- `pytest` - Testing framework

These are listed in `requirements.txt`.
