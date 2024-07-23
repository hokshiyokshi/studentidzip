import pytest
from app import app, is_password_strong

# Fixture to provide a test client for the Flask app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page_get(client):
    """Test GET request to home page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Enter your password' in response.data

def test_home_page_post_weak_password(client):
    """Test POST request with a weak password"""
    response = client.post('/', data={'password': 'weakpass'})
    assert response.status_code == 200
    assert b'Password does not meet the requirements.' in response.data

def test_home_page_post_common_password(client):
    """Test POST request with a common password"""
    common_password = list(app.common_passwords)[0]  # Using a common password from the list
    response = client.post('/', data={'password': common_password})
    assert response.status_code == 200
    assert b'Password does not meet the requirements.' in response.data

def test_home_page_post_strong_password(client):
    """Test POST request with a strong password"""
    response = client.post('/', data={'password': 'StrongPass123!'})
    assert response.status_code == 200
    assert b'Your password: StrongPass123!' in response.data

def test_is_password_strong():
    """Test password strength checker function"""
    assert not is_password_strong('weakpass')
    assert not is_password_strong('commonpass')
    assert is_password_strong('StrongPass123!')
