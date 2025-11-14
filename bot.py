import os
from flask import Flask, request
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

app = Flask(__name__)

# --- Telegramga xabar yuborish ---
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# --- Asosiy webhook ---
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        if "message" not in data:
            return "ok"

        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', "")

        # START komandasi
        if text == "/start":
            send_message(chat_id, "Assalomu alaykum! Men ishlayapman 😊\nHohlagan narsani yozing.")
            return "ok"

        # Oddiy matnlarga javob
        send_message(chat_id, f"Siz yozdingiz: {text}")

    except Exception as e:
        try:
            send_message(chat_id, "Xatolik yuz berdi 😢")
        except:
            pass

    return "ok"

@app.route('/')
def home():
    return "Bot ishlayapti!"