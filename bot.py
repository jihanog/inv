import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ---------- BOT TOKEN ----------
TOKEN = os.getenv("BOT_TOKEN")

# ---------- MESSAGES ----------
INVITE_MESSAGE = """Invite Code: <code>ADZ3U</code>
🔗 Link: https://ttier.xyz/register?i=ADZ3U
"""

CONTACT_MESSAGE = "Contact to buy:\nhttps://t.me/jihan_og"


# ---------- START COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
    except:
        await update.message.reply_text("⚠️ Error occurred.")


# ---------- MENU BUTTON HANDLER ----------
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        if text == "Invite Code":
            await update.message.reply_text(
                INVITE_MESSAGE,
                parse_mode="HTML"
            )

        elif text == "Contact to buy":
            await update.message.reply_text(CONTACT_MESSAGE)

    except:
        await update.message.reply_text("⚠️ Error occurred.")


# ---------- GLOBAL ERROR HANDLER ----------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(
                "⚠️ Bot error. Try again later."
            )
    except:
        pass


# ---------- APP ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

app.add_error_handler(error_handler)

app.run_polling()