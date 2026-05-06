import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def registered_user(db):
    return User.objects.create_user(
        email="user@email.com",
        full_name="Test User",
        password="securepass123",
    )
