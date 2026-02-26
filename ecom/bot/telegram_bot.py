import os
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")
django.setup()

TOKEN = "8679187453:AAGKFNlgfrs8I3FaP_HLQIFXglpotsDZmhM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("CHAT ID:", update.effective_chat.id)
    await update.message.reply_text("Bot đang chạy")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()