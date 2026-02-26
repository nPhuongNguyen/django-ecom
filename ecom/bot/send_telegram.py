import requests

TOKEN = "8679187453:AAGKFNlgfrs8I3FaP_HLQIFXglpotsDZmhM"
CHAT_ID = "8714972491"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    return requests.post(url, json=payload)