import pytest
from datetime import date


@pytest.mark.django_db
class TestCategoryViews:
    def test_list_categories(self, auth_client, expense_category):
        res = auth_client.get("/api/categories/")
        assert res.status_code == 200
        assert len(res.data) == 1

    def test_create_category(self, auth_client):
        res = auth_client.post(
            "/api/categories/",
            {
                "name": "Transport",
                "type": "expense",
                "color": "#f59e0b",
            },
        )
        assert res.status_code == 201
        assert res.data["name"] == "Transport"

    def test_create_duplicate_category(self, auth_client, expense_category):
        res = auth_client.post(
            "/api/categories/",
            {
                "name": "Food",
                "type": "expense",
            },
        )
        assert res.status_code == 400

    def test_delete_category(self, auth_client, expense_category):
        res = auth_client.delete(f"/api/categories/{expense_category.pk}/")
        assert res.status_code == 204

    def test_delete_nonexistent_category(self, auth_client):
        res = auth_client.delete("/api/categories/9999/")
        assert res.status_code == 404

    def test_requires_auth(self, client):
        res = client.get("/api/categories/")
        assert res.status_code == 401


@pytest.mark.django_db
class TestTransactionViews:
    def test_list_transactions(self, auth_client, transaction):
        res = auth_client.get("/api/transactions/")
        assert res.status_code == 200
        assert res.data["count"] == 1

    def test_create_transaction(self, auth_client, expense_category):
        res = auth_client.post(
            "/api/transactions/",
            {
                "title": "Lunch",
                "amount": "25.00",
                "type": "expense",
                "date": str(date.today()),
                "category_id": expense_category.pk,
            },
        )
        assert res.status_code == 201
        assert res.data["title"] == "Lunch"

    def test_create_transaction_negative_amount(self, auth_client):
        res = auth_client.post(
            "/api/transactions/",
            {
                "title": "Bad",
                "amount": "-10.00",
                "type": "expense",
                "date": str(date.today()),
            },
        )
        assert res.status_code == 400

    def test_get_transaction(self, auth_client, transaction):
        res = auth_client.get(f"/api/transactions/{transaction.pk}/")
        assert res.status_code == 200
        assert res.data["title"] == "Grocery"

    def test_update_transaction(self, auth_client, transaction):
        res = auth_client.put(
            f"/api/transactions/{transaction.pk}/",
            {
                "title": "Supermarket",
                "amount": "200.00",
                "type": "expense",
                "date": str(date.today()),
            },
        )
        assert res.status_code == 200
        assert res.data["title"] == "Supermarket"

    def test_delete_transaction(self, auth_client, transaction):
        res = auth_client.delete(f"/api/transactions/{transaction.pk}/")
        assert res.status_code == 204

    def test_filter_by_type(self, auth_client, transaction):
        res = auth_client.get("/api/transactions/?type=expense")
        assert res.status_code == 200
        assert res.data["count"] == 1

    def test_filter_by_type_no_results(self, auth_client, transaction):
        res = auth_client.get("/api/transactions/?type=income")
        assert res.status_code == 200
        assert res.data["count"] == 0

    def test_requires_auth(self, client):
        res = client.get("/api/transactions/")
        assert res.status_code == 401
