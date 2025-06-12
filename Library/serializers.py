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
    class Meta:
        model = User
        fields = ("first_name","last_name", "email")

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("Book_id", "Expected_return", "Actual_return", "User_id")

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "type", "money_to_pay")
