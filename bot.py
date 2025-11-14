import telebot

TOKEN = "7371202845:AAGZKymwF1eBsfYVisQ1M0DnElOz_LRZfr0"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Bot ishga tushdi 😊")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

print("Bot ishga tushdi...")

bot.infinity_polling()
