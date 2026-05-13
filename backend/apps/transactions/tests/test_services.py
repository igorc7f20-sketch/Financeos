import pytest
from decimal import Decimal
from datetime import date
from core.exceptions import ServiceException
from apps.transactions.services import CategoryService, TransactionService
from apps.transactions.models import Category, Transaction


@pytest.mark.django_db
class TestCategoryService:
    def test_list_categories(self, user, expense_category):
        categories = CategoryService.list(user)
        assert expense_category in categories

    def test_create_category(self, user):
        cat = CategoryService.create(user, name="Food", type="expense")
        assert cat.name == "Food"
        assert cat.type == "expense"
        assert cat.user == user

    def test_create_duplicate_raises(self, user):
        CategoryService.create(user, name="Food", type="expense")
        with pytest.raises(ServiceException):
            CategoryService.create(user, name="Food", type="expense")

    def test_delete_category(self, user, expense_category):
        CategoryService.delete(user, expense_category.pk)
        assert not Category.objects.filter(pk=expense_category.pk).exists()

    def test_delete_nonexistent_raises(self, user):
        with pytest.raises(ServiceException):
            CategoryService.delete(user, 9999)


@pytest.mark.django_db
class TestTransactionService:
    def test_list_transactions(self, user, transaction):
        transactions = TransactionService.list(user)
        assert transaction in transactions

    def test_create_transaction(self, user, expense_category):
        tx = TransactionService.create(
            user,
            {
                "title": "Grocery",
                "amount": Decimal("100.00"),
                "type": "expense",
                "date": date.today(),
                "category_id": expense_category.pk,
            },
        )
        assert tx.title == "Grocery"
        assert tx.amount == Decimal("100.00")
        assert tx.type == "expense"
        assert tx.category == expense_category
        assert tx.user == user

    def test_amount_must_be_positive(self, user):
        with pytest.raises(ServiceException):
            TransactionService.create(
                user,
                {
                    "title": "Bad",
                    "amount": Decimal("-10"),
                    "type": "expense",
                    "date": date.today(),
                },
            )

    def test_category_not_found_raises(self, user):
        with pytest.raises(ServiceException):
            TransactionService.create(
                user,
                {
                    "title": "No Category",
                    "amount": Decimal("50.00"),
                    "type": "expense",
                    "date": date.today(),
                    "category_id": 9999,
                },
            )

    def test_category_type_mismatch_raises(self, user, income_category):
        with pytest.raises(ServiceException):
            TransactionService.create(
                user,
                {
                    "title": "Mismatch",
                    "amount": Decimal("50.00"),
                    "type": "expense",
                    "date": date.today(),
                    "category_id": income_category.pk,
                },
            )

    def test_update_transaction(self, user, transaction):
        updated = TransactionService.update(user, transaction.pk, {"title": "Updated"})
        assert updated.title == "Updated"

    def test_update_transaction_amount(self, user, transaction):
        updated = TransactionService.update(user, transaction.pk, {"amount": Decimal("200.00")})
        assert updated.amount == Decimal("200.00")

    def test_update_transaction_negative_amount_raises(self, user, transaction):
        with pytest.raises(ServiceException):
            TransactionService.update(user, transaction.pk, {"amount": Decimal("-10.00")})

    def test_update_transaction_category(self, user, transaction, expense_category):
        updated = TransactionService.update(user, transaction.pk, {"category_id": expense_category.pk})
        assert updated.category == expense_category

    def test_update_transaction_category_not_found_raises(self, user, transaction):
        with pytest.raises(ServiceException):
            TransactionService.update(user, transaction.pk, {"category_id": 9999})

    def test_update_transaction_not_found_raises(self, user):
        with pytest.raises(ServiceException):
            TransactionService.update(user, 9999, {"title": "Updated"})

    def test_delete_transaction(self, user, transaction):
        TransactionService.delete(user, transaction.pk)
        assert not Transaction.objects.filter(pk=transaction.pk).exists()

    def test_delete_transaction_not_found_raises(self, user):
        with pytest.raises(ServiceException):
            TransactionService.delete(user, 9999)

    def test_get_nonexistent_raises(self, user):
        with pytest.raises(ServiceException):
            TransactionService.get(user, 9999)
