import pytest
from datetime import date
from decimal import Decimal
from rest_framework.test import APIClient
from apps.users.models import User
from apps.transactions.models import Category, Transaction


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@email.com",
        full_name="Test User",
        password="securepass123",
    )


@pytest.fixture
def auth_client(client, user):
    res = client.post(
        "/api/auth/login/", {"email": "user@email.com", "password": "securepass123"}
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client


@pytest.fixture
def expense_category(user):
    return Category.objects.create(
        user=user,
        name="Food",
        type="expense",
    )


@pytest.fixture
def income_category(user):
    return Category.objects.create(
        user=user,
        name="Salary",
        type="income",
    )


@pytest.fixture
def transaction(user, expense_category):
    return Transaction.objects.create(
        user=user,
        category=expense_category,
        title="Grocery",
        amount=Decimal("150.00"),
        type="expense",
        date=date.today(),
    )
