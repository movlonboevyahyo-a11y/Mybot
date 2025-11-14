import telebot
from flask import Flask, request

TOKEN = "7371202845:AAGZKymwF1eBsfYVisQ1M0DnElOz_LRZfr0"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Telegram webhook qismi
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def set_webhook():
    bot.remove_webhook()
    webhook_url = "https://mybot-vj1z.onrender.com/" + TOKEN
    bot.set_webhook(url=webhook_url)
    return "Webhook ishga tushdi!", 200

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Bot ishga tushdi 😊")

# Echo handler
@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)