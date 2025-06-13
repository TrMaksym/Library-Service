from django.db.models.signals import post_save
from django.dispatch import receiver

from Library.models import Book, Payment
from user.models import Borrowing, User
from notifications.tasks import send_telegram_message_task


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.User_id)
        book = Book.objects.get(pk=instance.Book_id)
        chat_id = getattr(user, "telegram_chat_id", None)
        if not chat_id:
            print("The user does not have a telegram_username specified.")
            return
        message = (
            f"Congratulations! Your new book order has been successfully created.\n"
            f"\nname book: {book.title}\n"
            f"Email user: {user.email}\n"
            "Please remember to return the book on time to avoid fines.\n\n"
            "If you have any questions, please contact the library administration.\n\n"
            "Thank you for using our services!\n"
            "Your library service"
        )
        send_telegram_message_task.delay(chat_id, message)


@receiver(post_save, sender=Payment)
def notify_new_payment(sender, instance, created, **kwargs):
    if created:
        borrowing = Borrowing.objects.filter(pk=instance.borrowing_id).first()
        if not borrowing:
            return
        user = User.objects.get(pk=borrowing.User_id)
        username = getattr(user, "telegram_username", None)
        if not username:
            print("The user does not have a telegram_username specified.")
            return
        message = (
            f"Payment successfully created!\n"
            f"Amount to pay: {instance.money_to_pay} UAH\n"
            f"Type: {instance.get_type_display()}\n"
            f"Status: {instance.get_status_display()}\n\n"
            f"Borrowing ID: {instance.borrowing_id}\n"
            f"You can find details about your payment in your user dashboard."
        )
        send_telegram_message_task.delay(username, message)