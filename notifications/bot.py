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

    user = User.objects.filter(telegram_username=username).first()
    if not user:
        user = User.objects.filter(telegram_chat_id=chat_id).first()

    if user:
        user.telegram_username = username
        user.telegram_chat_id = chat_id
        user.save()
        bot.send_message(chat_id, "You are connected to Telegram notifications!")
    else:
        bot.send_message(chat_id, "User not found!")

if __name__ == "__main__":
    bot.polling(none_stop=True)
