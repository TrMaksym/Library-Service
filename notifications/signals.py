from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import Borrowing
from notifications.tasks import send_telegram_message_task

@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        username = instance.user.telegram_username
        message = f"📚 a new book is taken: {instance.book.title}\nUser: {instance.user.email}"
        send_telegram_message_task.delay(username, message)