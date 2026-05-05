"""
User Service - Business Logic Layer.

All rules related to user creation and validation live here.
This layer never touches the request or the response directly.
"""

from core.exceptions import ServiceException
from .models import User
from .repositories import UserRepository


class UserService:

    @staticmethod
    def regiter(email: str, full_name: str, password: str) -> User:
        """
        Register a new user.
        Raises ServiceException if the email is already in use.
        """
        if UserRepository.email_exists(email):
            raise ServiceException("A user with this email already exists.")
        
        if len(password) < 8:
            raise ServiceException("Password must be at least 8 characters long.")
        
        return UserRepository.create_user(
            email=email, 
            full_name=full_name, 
            password=password
        )
    
    @staticmethod
    def get_profile(user: User) -> User:
        """
        Returns the authenticated user's profile.
        Centralized here so future rules (e.g. account status) are applied consistently.
        """
        if not user.is_active:
            raise ServiceException("This account is inactive.", status_code=403)
        return user