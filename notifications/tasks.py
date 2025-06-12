from celery import shared_task

from notifications.telegram import send_telegram_message, get_chat_id_by_username


@shared_task(name="notifications.tasks.send_telegram_message_task")
def send_telegram_message_task(username, text):
    chat_id = get_chat_id_by_username(username)
    if chat_id:
        send_telegram_message(chat_id, text)
    else:
        print(f"Cannot send message, chat_id not found for username {username}")