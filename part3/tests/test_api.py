import pytest
import json
from api.app import create_app


@pytest.fixture
def client():
    """Create a test client"""
    app = create_app('testing')
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    """Create a user and return auth token"""
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/auth/register',
                          data=json.dumps(user_data),
                          content_type='application/json')
    data = json.loads(response.data)
    return data['access_token']


@pytest.fixture
def auth_headers(auth_token):
    """Create authorization headers with token"""
    return {'Authorization': f'Bearer {auth_token}'}


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_register_user(client):
    """Test user registration"""
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/auth/register',
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user']['first_name'] == 'John'
    assert data['user']['email'] == 'john.doe@example.com'
    assert 'password' not in data['user']
    assert 'access_token' in data


def test_login_user(client):
    """Test user login"""
    # First register a user
    user_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'password': 'password123'
    }
    client.post('/api/v1/auth/register',
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Then login
    login_data = {
        'email': 'jane.smith@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'jane.smith@example.com'


def test_invalid_login(client):
    """Test login with invalid credentials"""
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/api/v1/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


def test_protected_endpoint(client, auth_headers):
    """Test protected endpoint with valid token"""
    response = client.get('/api/v1/auth/protected',
                         headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data


def test_protected_endpoint_no_token(client):
    """Test protected endpoint without token"""
    response = client.get('/api/v1/auth/protected')
    assert response.status_code == 401


def test_get_users_public(client):
    """Test getting all users (public endpoint)"""
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_create_amenity(client):
    """Test amenity creation (public for now)"""
    amenity_data = {
        'name': 'WiFi'
    }
    response = client.post('/api/v1/amenities/',
                          data=json.dumps(amenity_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'WiFi'


def test_create_place_authenticated(client, auth_headers):
    """Test place creation with authentication"""
    # First create an amenity
    amenity_data = {'name': 'WiFi'}
    amenity_response = client.post('/api/v1/amenities/',
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
    amenity = json.loads(amenity_response.data)
    
    # Create a place
    place_data = {
        'title': 'Beautiful Apartment',
        'description': 'A wonderful place to stay',
        'price': 100.0,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'amenities': [amenity['id']]
    }
    response = client.post('/api/v1/places/',
                          data=json.dumps(place_data),
                          content_type='application/json',
                          headers=auth_headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Beautiful Apartment'
    assert data['price'] == 100.0


def test_create_place_unauthenticated(client):
    """Test place creation without authentication"""
    place_data = {
        'title': 'Unauthorized Place',
        'price': 100.0,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    response = client.post('/api/v1/places/',
                          data=json.dumps(place_data),
                          content_type='application/json')
    assert response.status_code == 401


def test_create_review_authenticated(client, auth_headers):
    """Test review creation with authentication"""
    # Create another user for place ownership
    owner_data = {
        'first_name': 'Owner',
        'last_name': 'User',
        'email': 'owner@example.com',
        'password': 'password123'
    }
    owner_response = client.post('/api/v1/auth/register',
                                data=json.dumps(owner_data),
                                content_type='application/json')
    owner_token = json.loads(owner_response.data)['access_token']
    owner_headers = {'Authorization': f'Bearer {owner_token}'}
    
    # Create a place as owner
    place_data = {
        'title': 'Test Place',
        'price': 50.0,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    place_response = client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json',
                                headers=owner_headers)
    place = json.loads(place_response.data)
    
    # Create a review as different user
    review_data = {
        'text': 'Great place!',
        'rating': 5,
        'place_id': place['id']
    }
    response = client.post('/api/v1/reviews/',
                          data=json.dumps(review_data),
                          content_type='application/json',
                          headers=auth_headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['text'] == 'Great place!'
    assert data['rating'] == 5


def test_update_user_profile(client, auth_headers):
    """Test updating user profile (own profile only)"""
    # Get current user
    user_response = client.get('/api/v1/auth/protected', headers=auth_headers)
    user_data = json.loads(user_response.data)
    user_id = user_data['user_id']
    
    # Update profile
    update_data = {
        'first_name': 'Updated Name'
    }
    response = client.put(f'/api/v1/users/{user_id}',
                         data=json.dumps(update_data),
                         content_type='application/json',
                         headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'Updated Name'


def test_validation_errors(client):
    """Test validation errors"""
    # Test invalid user registration
    invalid_user = {
        'first_name': '',
        'email': 'invalid-email',
        'password': '123'  # Too short
    }
    response = client.post('/api/v1/auth/register',
                          data=json.dumps(invalid_user),
                          content_type='application/json')
    assert response.status_code == 400

def test_register_user_debug(client):
    """Test user registration with debugging"""
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/auth/register',
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data}")
    print(f"Response Headers: {dict(response.headers)}")
    
    # Si es 500, intenta obtener más información del error
    if response.status_code == 500:
        try:
            error_data = json.loads(response.data)
            print(f"Error Details: {error_data}")
        except:
            print("Could not parse error response as JSON")
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.data}"