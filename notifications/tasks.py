from celery import shared_task

from notifications.telegram import send_telegram_message, get_chat_id_by_username

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
