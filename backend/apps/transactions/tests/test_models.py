import pytest
from decimal import Decimal
from datetime import date
from apps.transactions.models import Category, Transaction


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self, user):
        cat = Category.objects.create(
            user=user,
            name="Food",
            type="expense",
        )
        assert cat.name == "Food"
        assert cat.type == "expense"
        assert cat.color == "#6366f1"
        assert str(cat) == "Food (expense)"

    def test_unique_together(self, user):
        Category.objects.create(user=user, name="Food", type="expense")
        with pytest.raises(Exception):
            Category.objects.create(user=user, name="Food", type="expense")


@pytest.mark.django_db
class TestTransactionModel:
    def test_create_transaction(self, user, expense_category):
        txn = Transaction.objects.create(
            user=user,
            category=expense_category,
            title="Grocery",
            amount=Decimal("150.00"),
            type="expense",
            date=date.today(),
        )
        assert txn.title == "Grocery"
        assert txn.amount == Decimal("150.00")
        assert txn.type == "expense"
        assert "Grocery" in str(tx)

    def test_category_null_on_delete(self, user, expense_category):
        tx = Transaction.objects.create(
            user=user,
            category=expense_category,
            title="Test",
            amount=Decimal("10.00"),
            type="expense",
            date=date.today(),
        )
        expense_category.delete()
        tx.refresh_from_db()
        assert tx.category is None