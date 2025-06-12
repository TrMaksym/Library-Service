import os

import requests
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")


def get_chat_id_by_username(username):
    if not username.startswith("@"):
        username = "@" + username
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    params = {"chat_id": username}
    response = requests.get(url, params=params)
    data = response.json()
    if data["ok"]:
        return data["result"]["id"]
    else:
        print(f"Error getting chat_id: {data}")
        return None


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.post(url, data=payload)
    print("Telegram response:", response.status_code, response.text)
