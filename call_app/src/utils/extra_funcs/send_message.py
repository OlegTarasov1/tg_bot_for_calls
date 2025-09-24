from aiogram import Bot
import os

async def send_message(
    chat_id: int,
    message: str,
    token: str = os.getenv("BOT_TOKEN")
):
    bot = Bot(
        token=token
    )
    
    await bot.send_message(
        chat_id,
        message
    )
    
    await bot.session.close()