import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="cash-user@email.com",
        full_name="Cash User",
        password="securepass123",
    )


@pytest.fixture
def auth_client(client, user):
    res = client.post(
        "/api/auth/login/",
        {"email": "cash-user@email.com", "password": "securepass123"},
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client
