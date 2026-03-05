import os
import logging
from threading import Thread
from flask import Flask
import telebot

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- TOKEN ----------------
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ---------------- MESSAGES ----------------
PACKAGES_MESSAGE = """
⭐Mixed PACKAGES ⭐

350+ Videos — $6
750+ Videos — $11
1550+ Videos — $21
5050+ Videos — $71
8050+ Videos — $101
Custom Plans available

💳 PAYMENT OPTIONS 

Crypto (BTC, ETH, USDT & more) | Binance Pay | PayPal | Visa / Mastercard | TON (Telegram Wallet).

>> SINGLE CATEGORIES AVAILABLE <<

Choose a plan And Payment Method.
"""

HELP_MESSAGE = "Hii 👋 How can I help you"


# ---------------- KEYWORD HANDLER ----------------
@bot.message_handler(func=lambda message: True)
def keyword_reply(message):
    text = message.text.lower()

    buy_keywords = [
        "i want to buy",
        "buy",
        "buy videos",
        "price",
        "how to buy",
        "videos price",
        "plan",
        "packages"
    ]

    help_keywords = [
        "i need help",
        "help",
        "support"
    ]

    if any(word in text for word in buy_keywords):
        bot.send_message(message.chat.id, PACKAGES_MESSAGE)

    elif any(word in text for word in help_keywords):
        bot.send_message(message.chat.id, HELP_MESSAGE)


# ---------------- FLASK WEB SERVER ----------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is alive ✅"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# ---------------- RUN BOT ----------------
def run_bot():
    logging.info("Bot polling started...")
    bot.infinity_polling(skip_pending=True)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_web()
