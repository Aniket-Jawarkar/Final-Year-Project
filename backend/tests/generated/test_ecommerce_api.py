import pytest
import requests
import uuid

# This script assumes a RESTful API structure where:
# - POST / creates a generic resource (e.g., a product).
# - GET /, GET /:id, DELETE /:id manage these resources.
# - Cart endpoints require authentication.
# - The API returns JSON and predictable status codes (200 OK, 201 Created, 404 Not Found).
# - Login returns a token like {"token": "your_jwt_token"}.
# - Payloads for POST requests need to be assumed based on context.

@pytest.fixture
def base_url():
    """Defines the base URL for the API being tested."""
    return "http://localhost:8001"

@pytest.fixture(scope="module")
def session_data():
    """A dictionary to hold data across tests in a module, like created IDs."""
    return {}

@pytest.fixture
def auth_headers(base_url):
    """
    Fixture to register and log in a new user.
    Returns the authorization headers needed for protected endpoints.
    """
    # Use a unique username for each test run to ensure idempotency
    unique_username = f"testuser_{uuid.uuid4().hex}"
    user_payload = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "a_secure_password_123"
    }
    
    # Endpoint 13: Register a new user
    # FIX: The error "Cannot POST /register" indicates the path is wrong. Common practice is to prefix auth routes.
    reg_response = requests.post(f"{base_url}/auth/register", json=user_payload)
    # This must succeed for auth-dependent tests to run
    assert reg_response.status_code in [200, 201], f"User registration failed: {reg_response.text}"

    # Endpoint 14: Log in with the new user
    login_payload = {"username": unique_username, "password": "a_secure_password_123"}
    # FIX: The login path is also likely prefixed.
    log_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert log_response.status_code == 200, f"User login failed: {log_response.text}"
    
    response_json = log_response.json()
    token = response_json.get("token")
    assert token, "Login response did not include a token."

    return {"Authorization": f"Bearer {token}"}

# --- Test User and Auth Endpoints ---

def test_register_user(base_url):
    """Test for Endpoint 13: POST /register"""
    unique_username = f"testuser_{uuid.uuid4().hex}"
    payload = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "a_secure_password_123"
    }
    # FIX: The error "Cannot POST /register" indicates the endpoint is not at the root. Assuming /auth/register.
    response = requests.post(f"{base_url}/auth/register", json=payload)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}. Response: {response.text}"
    assert "id" in response.json(), "Registration response should include a user ID."

def test_login_user(base_url, auth_headers):
    """Test for Endpoint 14: POST /login. Success is implicitly tested by the auth_headers fixture."""
    assert "Authorization" in auth_headers
    assert auth_headers["Authorization"].startswith("Bearer ")

# --- Test Generic Resource Endpoints (assuming 'products') ---

def test_create_resource(base_url, session_data):
    """Test for Endpoints 5 & 9: POST /"""
    payload = {
        "name": f"Test Product {uuid.uuid4().hex}",
        "price": 99.99,
        "description": "A test product."
    }
    # FIX: The error "Cannot POST /" indicates the endpoint for creating resources is not the root. Assuming /products.
    response = requests.post(f"{base_url}/products", json=payload)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "id" in response_data, "Response should contain the new resource ID."
    assert response_data["name"] == payload["name"]
    # Store the created product ID for other tests
    session_data['product_id'] = response_data['id']

def test_get_all_resources(base_url):
    """Test for Endpoint 7: GET /"""
    # FIX: The JSONDecodeError on GET / suggests it returns HTML. API endpoints are likely prefixed. Assuming /products.
    response = requests.get(f"{base_url}/products")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(response.json(), list), "Response for getting all resources should be a list."

def test_get_resource_by_id(base_url, session_data):
    """Test for Endpoints 6 & 8: GET /:id"""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']
    # FIX: The path for a specific resource should be consistent with the create/list path. Assuming /products/:id.
    response = requests.get(f"{base_url}/products/{product_id}")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    assert response.json()["id"] == product_id

def test_get_nonexistent_resource(base_url):
    """Negative test for GET /:id with an invalid ID."""
    non_existent_id = "nonexistent-id-12345"
    # FIX: The path should be consistent. Assuming /products/:id.
    response = requests.get(f"{base_url}/products/{non_existent_id}")
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}. Response: {response.text}"

# --- Test Endpoints with :productId parameter ---

def test_get_by_product_id(base_url, session_data):
    """Test for Endpoint 11: GET /:productId"""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']
    # FIX: The path should be consistent. Assuming /products/:productId.
    response = requests.get(f"{base_url}/products/{product_id}")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    assert response.json()["id"] == product_id

def test_post_by_product_id(base_url, session_data):
    """Test for Endpoint 12: POST /:productId. Assuming it adds a review."""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']
    payload = {"review": "This product is excellent!", "rating": 5}
    # FIX: The path should be consistent. Assuming /products/:productId.
    response = requests.post(f"{base_url}/products/{product_id}", json=payload)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    assert "status" in response.json() and response.json()["status"] == "success"

# --- Test Cart Endpoints ---

def test_get_cart_empty(base_url, auth_headers):
    """Test for Endpoint 1: GET /cart (when empty)"""
    response = requests.get(f"{base_url}/cart", headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    # Assuming an empty cart returns an empty list or object
    cart_data = response.json()
    assert "items" not in cart_data or len(cart_data["items"]) == 0

def test_add_to_cart_and_get_cart(base_url, auth_headers, session_data):
    """Test for Endpoint 2: POST /cart and verifies with Endpoint 1: GET /cart"""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']
    
    # Add an item
    payload = {"productId": product_id, "quantity": 2}
    response = requests.post(f"{base_url}/cart", json=payload, headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"

    # Verify by getting the cart
    get_response = requests.get(f"{base_url}/cart", headers=auth_headers)
    assert get_response.status_code == 200, f"Expected 200 but got {get_response.status_code}. Response: {get_response.text}"
    cart_items = get_response.json().get("items", [])
    assert any(item.get("productId") == product_id for item in cart_items), "Added item not found in cart."

def test_delete_from_cart(base_url, auth_headers, session_data):
    """Test for Endpoint 3: DELETE /cart/:productId"""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']

    # Ensure the item is in the cart first
    add_payload = {"productId": product_id, "quantity": 1}
    requests.post(f"{base_url}/cart", json=add_payload, headers=auth_headers)

    # Delete the item
    response = requests.delete(f"{base_url}/cart/{product_id}", headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"

    # Verify the item is no longer in the cart
    get_response = requests.get(f"{base_url}/cart", headers=auth_headers)
    cart_items = get_response.json().get("items", [])
    assert not any(item.get("productId") == product_id for item in cart_items), "Item was not deleted from cart."

def test_checkout(base_url, auth_headers, session_data):
    """Test for Endpoint 4: POST /checkout"""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']

    # Add an item to the cart to enable checkout
    add_payload = {"productId": product_id, "quantity": 1}
    add_res = requests.post(f"{base_url}/cart", json=add_payload, headers=auth_headers)
    assert add_res.status_code == 200, f"Failed to add item to cart for checkout test. Response: {add_res.text}"

    # Perform checkout
    response = requests.post(f"{base_url}/checkout", headers=auth_headers, json={})
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"
    assert "orderId" in response.json(), "Checkout response should contain an orderId."

# --- Cleanup Test ---

def test_delete_resource(base_url, session_data):
    """Test for Endpoint 10: DELETE /:id. This runs last to clean up created resource."""
    assert 'product_id' in session_data, "Product ID not found from create test."
    product_id = session_data['product_id']
    # FIX: The path should be consistent. Assuming /products/:id.
    response = requests.delete(f"{base_url}/products/{product_id}")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"

    # Verify deletion
    # FIX: The verification path must also be corrected.
    get_response = requests.get(f"{base_url}/products/{product_id}")
    assert get_response.status_code == 404, f"Expected 404 after deletion but got {get_response.status_code}. Response: {get_response.text}"