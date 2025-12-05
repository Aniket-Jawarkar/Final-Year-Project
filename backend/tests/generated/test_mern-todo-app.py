import pytest
import requests
import json

# Define a fixture for the base URL to be used in all test functions.
# This makes it easy to change the target server (e.g., from localhost to a staging server).
@pytest.fixture
def base_url():
    """Provides the base URL for the API."""
    return "http://localhost:8001"

# NOTE: The payloads below are examples. You may need to adjust them
# based on the actual API's expected data structure and requirements.

def test_forgot_password(base_url):
    """
    Test the /forgotPassword endpoint.
    Assumes it requires an email to send a reset link.
    """
    # FIX: Corrected endpoint to a conventional RESTful path.
    url = f"{base_url}/api/auth/forgot-password"
    # Example payload: Assumes the API needs an email to process a password reset.
    payload = {
        "email": "testuser@example.com"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # Assert that the request was successful (e.g., status code 200 OK).
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    # Optionally, assert something about the response content.
    response_data = response.json()
    assert "message" in response_data
    assert "Password reset link sent" in response_data["message"]

def test_reset_password(base_url):
    """
    Test the /resetPassword endpoint.
    Assumes it requires a reset token and a new password.
    """
    # FIX: Corrected endpoint to a conventional RESTful path.
    url = f"{base_url}/api/auth/reset-password"
    # Example payload: Assumes a token and a new password are required.
    payload = {
        "reset_token": "some_valid_reset_token_from_email",
        "new_password": "aVeryStrongNewPassword123!"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == "Password has been reset successfully."

def test_add_task(base_url):
    """
    Test the /addTask endpoint.
    Assumes it requires task details like a title and description.
    """
    # FIX: Corrected endpoint to use the RESTful collection name /tasks.
    url = f"{base_url}/api/tasks"
    # Example payload: Assumes details for the new task are needed.
    # An auth token might also be required in a real-world scenario.
    payload = {
        "title": "Buy groceries",
        "description": "Milk, Bread, Cheese, and Eggs",
        "user_id": 1 
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # A successful creation is often indicated by a 201 status code.
    # We will check for 201, but 200 is also a common success response.
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "task_id" in response_data
    assert response_data["message"] == "Task added successfully."

def test_get_task(base_url):
    """
    Test the /getTask endpoint.
    Assumes it takes a task_id as a query parameter.
    """
    task_id = 123 # Example task ID
    # FIX: Corrected endpoint to a RESTful path with the ID in the URL.
    url = f"{base_url}/api/tasks/{task_id}"
    
    response = requests.get(url)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "title" in response_data
    assert "description" in response_data
    assert response_data["id"] == task_id

def test_remove_task(base_url):
    """
    Test the /removeTask endpoint.
    Assumes it takes a task_id as a query parameter.
    Note: Using GET for a delete operation is unconventional; DELETE is standard.
    """
    task_id_to_remove = 456 # Example task ID
    # FIX: Corrected endpoint to a RESTful path with the ID in the URL.
    url = f"{base_url}/api/tasks/{task_id_to_remove}"
    
    # FIX: Changed HTTP method from GET to DELETE, which is the standard for this action.
    response = requests.delete(url)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "message" in response_data
    assert f"Task {task_id_to_remove} removed successfully" in response_data["message"]

def test_login(base_url):
    """
    Test the /login endpoint.
    Assumes it requires credentials like email and password.
    """
    # FIX: Corrected endpoint to a conventional RESTful path.
    url = f"{base_url}/api/auth/login"
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "token" in response_data # A successful login should return an auth token.
    assert "message" in response_data
    assert response_data["message"] == "Login successful."

def test_register(base_url):
    """
    Test the /register endpoint.
    Assumes it requires user details for a new account.
    """
    # FIX: Corrected endpoint to a conventional RESTful path.
    url = f"{base_url}/api/auth/register"
    # Use a unique email/username for each test run if the database persists
    payload = {
        "username": "newtestuser",
        "email": "newtestuser@example.com",
        "password": "aSecurePassword123"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # A successful creation is often indicated by a 201 status code.
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "user_id" in response_data
    assert "message" in response_data
    assert response_data["message"] == "User registered successfully."

def test_get_user(base_url):
    """
    Test the /getuser endpoint.
    Assumes it takes a user_id as a query parameter.
    """
    user_id = 1 # Example user ID
    # FIX: Corrected endpoint to a RESTful path with the ID in the URL.
    url = f"{base_url}/api/users/{user_id}"
    
    response = requests.get(url)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    
    response_data = response.json()
    assert "username" in response_data
    assert "email" in response_data
    assert response_data["id"] == user_id