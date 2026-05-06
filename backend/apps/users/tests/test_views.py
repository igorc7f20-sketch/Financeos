import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def client():
    return APIClient()


pytest.fixture


def registered_user(db):
    return User.objects.create_user(
        email="user@email.com",
        full_name="Test User",
        password="testpass123",
    )


@pytest.mark.django_db
class TestAuthViews:
    def test_register_success(self, client):
        res = client.post(
            reverse("auth-register"),
            {
                "email": "new@email.com",
                "full_name": "Test User",
                "password": "securepass123",
            },
        )
        assert res.status_code == 201
        assert res.data["email"] == "new@email.com"

    def test_register_duplicate_email(self, client, registered_user):
        res = client.post(
            reverse("auth-register"),
            {
                "email": "user@email.com",
                "full_name": "Other",
                "password": "securepass123",
            },
        )
        assert res.status_code == 400

    def test_login_success(self, client, registered_user):
        res = client.post(
            reverse("auth-login"),
            {
                "email": "user@email.com",
                "password": "securepass123",
            },
        )
        assert res.status_code == 200
        assert "access" in res.data
        assert "refresh" in res.data

    def test_profile_requires_auth(self, client):
        res = client.get(reverse("auth-profile"))
        assert res.status_code == 401

    def test_profile_authenticated(self, client, registered_user):
        login = client.post(
            reverse("auth-login"),
            {
                "email": "user@email.com",
                "password": "securepass123",
            },
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        res = client.get(reverse("auth-profile"))
        assert res.status_code == 200
        assert res.data["email"] == "user@email.com"
