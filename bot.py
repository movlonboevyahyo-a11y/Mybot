import telebot
from flask import Flask, request

TOKEN = "7371202845:AAGZKymwF1eBsfYVisQ1M0DnElOz_LRZfr0"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Telegram webhook uchun
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
        )]
    )
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://mybot-vj1z.onrender.com/' + TOKEN)
    return "Webhook ishladi!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Assalomu alaykum! Bot ishga tushdi 😊")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)