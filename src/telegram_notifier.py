import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[1] / ".env"
# print(dotenv_path)
load_dotenv(dotenv_path=dotenv_path, override=True)


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"

    if not bot_token or not chat_id:
        print("Token ou Chat ID manquant")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=payload)
        print("Message Telegram envoyé")
        return True
    except Exception as e:
        print(f"Erreur Telegram : {e}")
        return False


if __name__ == "__main__":
    send_telegram_message("TEST")
