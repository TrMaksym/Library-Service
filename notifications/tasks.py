from celery import shared_task

from notifications.telegram import send_telegram_message


@shared_task(name="notifications.tasks.send_telegram_message_task")
def send_telegram_message_task(text):
    chat_id = 954524211
    send_telegram_message(chat_id, text)