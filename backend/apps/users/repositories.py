"""
User repository - Data Access Layer.

Only this layer allowed to query the database for users.
No business logic here - Only queries.
"""

from typing import Optional
from core.base_repository import BaseRepository
from .models import User

class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.model.objects.filter(email=email).first()
    
    @classmethod
    def email_exists(cls, email: str) -> bool:
        return cls.model.objects.filter(email=email).exists()
    
    @classmethod
    def create_user(cls, email: str, full_name: str, password: str) -> User:
        return cls.model.objects.create_user(
            email=email, 
            full_name=full_name,
            password=password 
        )