import asyncio
from telegram import Bot
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def _send(chat_id: str, message: str):
    await bot.send_message(chat_id=chat_id, text=message)

def send_telegram_message(chat_id: str, message: str):
    asyncio.run(_send(chat_id, message))