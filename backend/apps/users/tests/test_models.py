import pytest
from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@email.com", full_name="Test User", password="strongpassword123"
        )
        assert user.email == "test@email.com"
        assert user.full_name == "Test User"
        assert user.check_password("strongpassword123")
        assert user.is_active is True
        assert user.is_staff is False

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@email.com",
            full_name="Admin",
            password="adminpass123",
        )
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_email_is_unique(self):
        User.objects.create_user(
            email="dup@email.com", full_name="A", password="pass1234"
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                email="dup@email.com", full_name="B", password="pass1234"
            )

    def test_str_returns_email(self):
        user = User.objects.create_user(
            email="str@email.com", full_name="STR", password="pass1234"
        )
        assert str(user) == "str@email.com"
