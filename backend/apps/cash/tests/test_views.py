import pytest
from decimal import Decimal


@pytest.mark.django_db
class TestCashViews:
    def test_create_movement(self, auth_client):
        res = auth_client.post(
            "/api/cash/movements/",
            {
                "type": "income",
                "description": "Sale",
                "amount": "25.50",
            },
        )

        assert res.status_code == 201
        assert res.data["description"] == "Sale"
        assert res.data["amount"] == "25.50"

    def test_list_movements_is_paginated(self, auth_client):
        auth_client.post(
            "/api/cash/movements/",
            {
                "type": "income",
                "description": "Sale",
                "amount": "25.50",
            },
        )

        res = auth_client.get("/api/cash/movements/")

        assert res.status_code == 200
        assert res.data["count"] == 1
        assert res.data["results"][0]["description"] == "Sale"
        assert res.data["totals"]["income"] == "25.50"
        assert res.data["totals"]["expense"] == "0.00"
