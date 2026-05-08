"""
Transaction Serializers - Content Layer.

Input validation and output transformation only.
No business rules here.
"""
from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type", "color", "icon", "created_at"]
        read_only_fields = ["id", "created_at"]


class CategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=Category.CategoryType.choices)
    color = serializers.CharField(max_length=7, default="#6366f1")
    icon = serializers.CharField(max_length=50, allow_blank=True, default="")


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_Only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "title",
            "amount",
            "type",
            "date",
            "notes",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TransactionInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    type = serializers.ChoiceField(choices=Transaction.TransactionType.choices)
    date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, default="")
    category_id = serializers.IntegerField(required=False, allow_null=True)


class TransactionFilterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=Transaction.TransactionType.choices, required=False
    )
    category_id = serializers.IntegerField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    search = serializers.CharField(required=False, allow_blank=True) 