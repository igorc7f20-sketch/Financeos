"""
Transaction Service - Business Logic Layer.

All rules for creating, updating, and validating 
transactions and categories live here.
"""
from decimal import Decimal
from core.exceptions import ServiceException
from .models import Category, Transaction
from .repositories import CategoryRepository, TransactionRepository


class CategoryService:

    @staticmethod
    def list(user) -> list:
        return CategoryRepository.get_by_user(user)
    
    @staticmethod
    def create(user, name: str, type: str, color: str = "#6366f1", icon: str = "") -> Category:
        if CategoryRepository.exists_for_user(user, name, type):
            raise ServiceException(f"Category '{name}' of type '{type}' already exists.")
        return CategoryRepository.create_for_user(
            user,
            name=name,
            type=type,
            color=color,
            icon=icon
        )
    
    @staticmethod
    def delete(user, pk: int) -> None:
        category = CategoryRepository.get_by_user_and_id(user, pk)
        if not category:
            raise ServiceException("Category not found.", status_code=404)
        category.delete()


class TransactionService:

    @staticmethod
    def list(user, filters: dict = None):
        return TransactionRepository.get_by_user(user, filters)
    
    @staticmethod
    def get(user, pk: int) -> Transaction:
        transaction = TransactionRepository.get_by_user_and_id(user, pk)
        if not transaction:
            raise ServiceException("Transaction not found.", status_code=404)
        return transaction
    
    @staticmethod
    def create(user, data: dict) -> Transaction:
        amount = Decimal(data.get("amount", 0))
        if amount <= 0:
            raise ServiceException("Amount must be greater than zero.")
        
        category = None
        if data.get("category_id"):
            category = CategoryRepository.get_by_user_and_id(user, data["category_id"])
            if not category:
                raise ServiceException("Category not found.", status_code=404)
            if category.type != data.get("type"):
                raise ServiceException(
                    f"Category type '{category.type}' does not match " 
                    f"transaction type '{data.get('type')}'."
                )
            
        return TransactionRepository.create_for_user(
            user, 
            title=data["title"],
            amount=amount,
            type=data["type"],
            date=data["date"],
            notes=data.get("notes", ""),
            category=category
        )
    
    @staticmethod
    def update(user, pk: int, data: dict) -> Transaction:
        transaction = TransactionRepository.get_by_user_and_id(user, pk)
        if not transaction:
            raise ServiceException("Transaction not found.", status_code=404)

        if "amount" in data:
            amount = Decimal(str(data["amount"]))
            if amount <= 0:
                raise ServiceException("Amount must be greater than zero.")
            data["amount"] = amount

        if data.get("category_id"):
            category = CategoryRepository.get_by_user_and_id(user, data["category_id"])
            if not category:
                raise ServiceException("Category not found.", status_code=404)
            data["category"] = category
            del data["category_id"]

        return TransactionRepository.update(transaction, **data)
    
    @staticmethod
    def delete(user, pk: int) -> None:
        transaction = TransactionRepository.get_by_user_and_id(user, pk)
        if not transaction:
            raise ServiceException("Transaction not found.", status_code=404)
        transaction.delete()
