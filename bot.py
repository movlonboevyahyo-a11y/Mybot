import os
import telebot
import requests
from flask import Flask, request

# Tokenlarni Render Environment Variables'dan olish
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# ---------- Webhook qismi ----------
@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def set_webhook():
    bot.remove_webhook()
    webhook_url = "https://YOUR_APP_NAME.onrender.com/" + TELEGRAM_TOKEN
    bot.set_webhook(url=webhook_url)
    return "Webhook ishga tushdi!", 200

# ---------- /start ----------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Bot ishga tushdi 😊")

# ---------- AI Chat javobi ----------
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

    answer = response.json()["choices"][0]["message"]["content"]
    bot.send_message(message.chat.id, answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)