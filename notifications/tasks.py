from celery import shared_task
from django.utils import timezone

from Library.models import Book
from notifications.telegram import send_telegram_message, get_chat_id_by_username
from user.models import Borrowing, User

chat_id = 954524211


@shared_task(name="notifications.tasks.send_telegram_message_task")
def send_telegram_message_task(identifier, text):
    if isinstance(identifier, int) or (
        isinstance(identifier, str) and identifier.lstrip("-").isdigit()
    ):
        chat_id = identifier
    else:
        chat_id = get_chat_id_by_username(identifier)
    if chat_id:
        send_telegram_message(chat_id, text)
    else:
        print(f"Cannot send message, chat_id not found for identifier {identifier}")


@shared_task(name="notifications.tasks.notify_overdue_borrowings")
def notify_overdue_borrowings():
    today = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        Expected_return__lt=today, Actual_return__isnull=True
    )
    for borrowing in overdue_borrowings:
        user = User.objects.filter(pk=borrowing.User_id).first()
        book = Book.objects.filter(pk=borrowing.Book_id).first()
        if user and user.telegram_username:
            message = (
                f"Reminder! You are overdue for returning the book: \n"
                f" Name: {book.title}\n"
                f" Date of return: {borrowing.Expected_return}"
                f" Please return the book as soon as possible."
            )
            send_telegram_message_task.delay(user.telegram_username, message)
