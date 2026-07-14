from apps.cash.serializers import CashMovementInputSerializer


def test_input_serializer_allows_missing_payment_method():
    serializer = CashMovementInputSerializer(
        data={
            "type": "income",
            "description": "Sale",
            "amount": "10.00",
        }
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["description"] == "Sale"
