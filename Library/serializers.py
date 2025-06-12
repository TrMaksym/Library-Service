from django.contrib.auth import get_user_model
from rest_framework import serializers

from Library.models import Book, Payment
from user.models import Borrowing

User = get_user_model()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "Author", "Cover", "Inventory", "Daily_fee")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("Book_id", "Expected_return", "Actual_return", "User_id")

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "type", "money_to_pay")
