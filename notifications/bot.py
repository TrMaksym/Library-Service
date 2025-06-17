import os
import django
from telebot import TeleBot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library_Service.settings")
django.setup()

from user.models import User

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    username = message.from_user.username

    if not username:
        bot.send_message(
            chat_id,
            "Your Telegram account does not have a username set! Please set a username in your Telegram settings and try again."
        )
        return

    user = User.objects.filter(telegram_username=username).first()

    if user:
        user.telegram_chat_id = chat_id
        user.telegram_username = username
        user.save()
        bot.send_message(chat_id, "You are now connected to Telegram notifications!")
    else:
        bot.send_message(
            chat_id,
            f"User with username @{username} was not found in the system."
        )

if __name__ == "__main__":
    bot.polling(none_stop=True)
