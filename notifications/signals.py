from django.db.models.signals import post_save
from django.dispatch import receiver

from Library.models import Book
from user.models import Borrowing, User
from notifications.tasks import send_telegram_message_task


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.User_id)
        book = Book.objects.get(pk=instance.Book_id)
        username = getattr(user, "telegram_username", None)
        if not username:
            print("The user does not have a telegram_username specified.")
            return
        message = (
            f"Вітаємо! Нове замовлення на книгу успішно створено.\n"
            f"\nНазва книги: {book.title}\n"
            f"Email користувача: {user.email}\n"
            "Будь ласка, не забудьте повернути книгу вчасно, щоб уникнути штрафів.\n\n"
            "Якщо у вас виникли питання, звертайтесь до адміністрації бібліотеки.\n\n"
            "Дякуємо, що користуєтесь нашими послугами!\n"
            "Ваш бібліотечний сервіс"
        )

        send_telegram_message_task.delay(username, message)
