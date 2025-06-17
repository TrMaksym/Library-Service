from django.contrib import admin

from django.contrib import admin
from .models import Book, Payment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "Author", "Cover", "Inventory", "Daily_fee")
    search_fields = ("title", "Author")
    list_filter = ("Cover",)
    ordering = ("title",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "type", "borrowing_id", "money_to_pay", "session_id")
    search_fields = ("session_id",)
    list_filter = ("status", "type")
    ordering = ("-id",)
