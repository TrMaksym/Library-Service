import os

import requests
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    response = requests.post(url, data=payload)
    print("Telegram response:", response.status_code, response.text)

if __name__ == "__main__":
    send_telegram_message(chat_id=954524211, text="Здоров Лох")
