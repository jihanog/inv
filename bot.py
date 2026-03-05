import os
import logging
from threading import Thread
from flask import Flask
import telebot

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN)

# ---------------- MESSAGES ----------------
PACKAGES_MESSAGE = """
⭐Mixed CP PACKAGES ⭐

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

    if not message.text:
        return

    text = message.text.lower()

    # BUY KEYWORDS
    if (
        "buy" in text
        or "price" in text
        or "videos" in text
        or "package" in text
        or "plan" in text
    ):
        bot.send_message(message.chat.id, PACKAGES_MESSAGE)
        return

    # HELP KEYWORDS
    if "help" in text:
        bot.send_message(message.chat.id, HELP_MESSAGE)
        return


# ---------------- FLASK ----------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is alive ✅"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# ---------------- BOT ----------------
def run_bot():
    bot.infinity_polling(skip_pending=True)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_web()
