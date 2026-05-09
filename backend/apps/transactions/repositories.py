"""
Transaction Repository - Data acess Layer.

All database queries for transactions and categories live here.
No business rules - only data access.
"""

from typing import Optional
from django.db.models import QuerySet
from core.base_repository import BaseRepository
from .models import Category, Transaction


class CategoryRepository(BaseRepository):
    model = Category

    @classmethod
    def get_by_user(cls, user) -> QuerySet:
        return cls.model.objects.filter(user=user)

    @classmethod
    def get_by_user_and_id(cls, user, pk: int) -> Optional[Category]:
        return cls.model.objects.filter(user=user, pk=pk).first()

    @classmethod
    def exists_for_user(cls, user, **kwargs) -> Category:
        return cls.model.objects.create(user=user, **kwargs)

    @classmethod
    def create_for_user(cls, user, **kwargs) -> Category:
        return cls.model.objects.create(user=user, **kwargs)


class TransactionRepository(BaseRepository):
    model = Transaction

    @classmethod
    def get_by_user(cls, user, filters: dict = None) -> QuerySet:
        qs = cls.model.objects.filter(user=user).select_related("category")
        if not filters:
            return qs

        if filters.get("type"):
            qs = qs.filter(type=filters["type"])
        if filters.get("category_id"):
            qs = qs.filter(category_id=filters["category_id"])
        if filters.get("date_from"):
            qs = qs.filter(date__gte=filters["date_from"])
        if filters.get("date_to"):
            qs = qs.filter(date__lte=filters["date_to"])
        if filters.get("search"):
            qs = qs.filter(title__icontains=filters["search"])

        return qs

    @classmethod
    def get_by_user_and_id(cls, user, pk: int) -> Optional[Transaction]:
        return (
            cls.model.objects.filter(user=user, pk=pk)
            .select_related("category")
            .first()
        )

    @classmethod
    def create_for_user(cls, user, **kwargs) -> Transaction:
        return cls.model.objects.create(user=user, **kwargs)

    @classmethod
    def update(cls, transaction: Transaction, **kwargs) -> Transaction:
        for field, value in kwargs.items():
            setattr(transaction, field, value)
        transaction.save()
        return transaction
