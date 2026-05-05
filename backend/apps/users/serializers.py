"""
User Serializer - Contract Layer.

Responsible for input validation and data transformation only.
Never contains busines rules - those belong in services.py
"""

from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "created_at"]
        read_only_fields = fields