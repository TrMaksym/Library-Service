from django.db import models


class Book(models.Model):
    HARD = "HARD"
    SOFT = "SOFT"

    COVER_CHOICES = [
        (HARD, "Hardcover"),
        (SOFT, "Softcover"),
    ]
    title = models.CharField(max_length=150)
    Author = models.CharField(max_length=60)
    Cover = models.CharField(max_length=100, choices=COVER_CHOICES)
    Inventory = models.PositiveIntegerField()
    Daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Payment(models.Model):
    PENDING = "PENDING"
    PAID = "PAID"

    PAYMENT = "PAYMENT"
    FINE = "FINE"

    TYPE_CHOICES = [
        (PAYMENT, "Payment"),
        (FINE, "Fine"),
    ]
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing_id = models.IntegerField()
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
