from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    telegram_link = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "password", "telegram_username", "telegram_link"]
        read_only_fields = ["id", "is_staff"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def get_telegram_link(self, obj):
        token = obj.get_or_create_telegram_link_token()
        bot_username = "Borrow_watch_bot"
        return f"https://t.me/{bot_username}?start={token}"

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
