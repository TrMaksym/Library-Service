from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response

from Library.models import Book, Payment
from user.models import Borrowing

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "Author", "Cover", "Inventory", "Daily_fee")

    def get_current_borrower_telegram_username(self, obj):
        current_borrowing = (
            Borrowing.objects.filter(Book_id=obj.id, Actual_return__isnull=True)
            .select_related("User")
            .first()
        )
        if current_borrowing and current_borrowing.User and current_borrowing.User.telegram_username:
            return current_borrowing.User.telegram_username
        return None


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BorrowingSerializer(serializers.ModelSerializer):
    telegram_username = serializers.CharField(
        source="get_telegram_username", read_only=True
    )

    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ("User_id",)

    def get_telegram_username(self, obj):
        from user.models import User
        user = User.objects.filter(pk=obj.User_id).first()
        return user.telegram_username if user else None

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.telegram_username:
            raise serializers.ValidationError("Потрібно вказати telegram_username у профілі!")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["User_id"] = user.id
        return super().create(validated_data)


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "type", "money_to_pay", "borrowing_id", "session_url", "session_id")
        read_only_fields = ("session_url", "session_id")

