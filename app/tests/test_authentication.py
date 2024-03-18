import pytest
from ..app import create_app
from ..database.db import db


@pytest.fixture
def app():
    """
    Fixture for creating and configuring the Flask app for testing.

    Yields:
        Flask app: The configured Flask app instance.
    """
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Fixture for creating a test client to interact with the Flask app.

    Args:
        app: The configured Flask app instance.

    Returns:
        Test client: The test client for making requests to the app.
    """
    return app.test_client()


def test_user_registration_with_valid_credentials(client):
    """
    Test case for registering a new user with valid credentials.

    Args:
        client: The test client for making requests to the app.
    """
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 201
    assert 'message' in response.json


def test_duplicate_user_registration(client):
    """
    Test case for attempting to register the same user twice.

    Args:
        client: The test client for making requests to the app.
    """
    client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 400
    assert 'message' in response.json
    assert response.json['message'] == 'Username already exists.'


def test_user_login_with_valid_credentials(client):
    """
    Test case for user login with valid credentials.

    Args:
        client: The test client for making requests to the app.
    """
    client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    # Login with correct credentials
    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_with_invalid_credentials(client):
    """
    Test case for login attempt with invalid credentials.

    Args:
        client: The test client for making requests to the app.
    """
    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401
    assert 'message' in response.json
    assert response.json['message'] == 'Invalid credentials.'
