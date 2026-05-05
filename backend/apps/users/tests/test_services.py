import pytest
from core.exceptions import ServiceException
from apps.users.services import UserService


@pytest.mark.django_db
class TestUserService:
    def test_register_success(self):
        user = UserService.regiter(
            email="new@email.com",
            full_name="New User",
            password="securepass",
        )
        assert user.email == "new@email.com"

    def test_register_duplicate_email(self):
        UserService.regiter("dup@email.com", "User A", "securepass")
        with pytest.raises(ServiceException) as exc:
            UserService.regiter("dup@email.com", "User B", "securepass")
        assert "already exists" in exc.value.message

    def test_register_short_password(self):
        with pytest.raises(ServiceException) as exc:
            UserService.regiter("short@email.com", "User", "123")
        assert "8 characters" in exc.value.message