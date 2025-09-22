from aiogram import Bot


async def send_message(
    token,
    chat_id,
    message
):
    bot = Bot(
        token=token
    )
    
    await bot.send_message(
        chat_id,
        message
    )
    
    await bot.session.close()