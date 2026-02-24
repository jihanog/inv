import os
import logging
from threading import Thread
from flask import Flask

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- TOKEN ----------------
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

# ---------------- MESSAGES ----------------
INVITE_MESSAGE = """Invite Code: <code>ADZ3U</code>
🔗 Link: https://ttier.xyz/register?i=ADZ3U
"""

CONTACT_MESSAGE = "Contact to buy:\nhttps://t.me/jihan_og"

# ---------------- TELEGRAM HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Invite Code"],
        ["Contact to buy"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        INVITE_MESSAGE,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Invite Code":
        await update.message.reply_text(
            INVITE_MESSAGE,
            parse_mode="HTML"
        )

    elif text == "Contact to buy":
        await update.message.reply_text(CONTACT_MESSAGE)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(msg="Exception while handling update:", exc_info=context.error)


# ---------------- TELEGRAM APP ----------------
tg_app = ApplicationBuilder().token(TOKEN).build()

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
tg_app.add_error_handler(error_handler)

# ---------------- FLASK WEB SERVER ----------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is alive ✅"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# ---------------- RUN TELEGRAM BOT ----------------
def run_bot():
    tg_app.run_polling()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_web()