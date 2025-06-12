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
    telegram_username = serializers.CharField(
        source="User.telegram_username",
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = Borrowing
        fields = "__all__"

    def validate(self, attrs):
        user = self.context["request"].user
        telegram_username = attrs.get("User", {}).get("telegram_username")
        if not user.telegram_username and not telegram_username:
            raise serializers.ValidationError("Need to enter telegram_username.")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        telegram_username = validated_data.get("User", {}).get("telegram_username")
        if telegram_username and user.telegram_username != telegram_username:
            user.telegram_username = telegram_username
            user.save()
        validated_data["User"] = user
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "type", "money_to_pay")
