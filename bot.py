import telebot
from flask import Flask, request

# Telegram BOT TOKEN – BU YERGA O'ZINGNI TOKENINGNI YOZ!
TOKEN = "7371202845:AAGZKymwF1eBsfYVisQ1M0DnElOz_LRZfr0"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --------------------- WEBHOOK QISMI ---------------------
@app.route("/" + TOKEN, methods=["POST"])
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


# --------------------- /start KOMANDASI ---------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Bot ishga tushdi 😊"
    )


# --------------------- HAMMA XABARLAR ---------------------
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    text = message.text.lower()

    if "salom" in text:
        bot.send_message(message.chat.id, "Va alaykum salom 😊")
    else:
        bot.send_message(message.chat.id, "Qabul qilindi ✔️")


# ------------------------------------------------------------
# Flask serverni ishga tushirish
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# ------------------ BARCHA XABARLAR UCHUN HANDLER ------------------

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    text = message.text.lower()

    if "salom" in text:
        bot.send_message(message.chat.id, "Va alaykum salom 😊")
    else:
        bot.send_message(message.chat.id, "Xabaringiz qabul qilindi ✔️")
