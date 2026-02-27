import os
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ..settings import TOKEN_TELEGRAM_BOT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")
django.setup()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đang chạy")

def main():
    app = ApplicationBuilder().token(TOKEN_TELEGRAM_BOT).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()