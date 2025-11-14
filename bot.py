import os
import telebot
import requests
from flask import Flask, request

# Tokenlarni Render Environment Variables orqali olish
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Sening Render URL'ing
WEBHOOK_URL = "https://mybot-vj1z.onrender.com/" + TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# ----------- Webhook qismi -----------
@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook ishga tushdi!", 200


# ----------- /start buyruq -----------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Men ishga tushdim 😊\nXohlagan narsani yozing."
    )


# ----------- AI bilan javob berish -----------
@bot.message_handler(func=lambda m: True)
def ai_answer(message):
    text = message.text

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-70b-versatile",
        "messages": [{"role": "user", "content": text}]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    try:
        answer = response.json()["choices"][0]["message"]["content"]
    except:
        answer = "Xatolik yuz berdi 🥲"

    bot.send_message(message.chat.id, answer)


# ----------- App ishga tushirish -----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)