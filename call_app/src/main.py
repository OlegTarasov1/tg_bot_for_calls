from aiogram import (
    Bot,
    Dispatcher
)
import asyncio
from config.database_config import EnvData
from views.routers import routers

async def main():
    settingsData = EnvData() 
    bot = Bot(token = settingsData.BOT_TOKEN.get_secret_value())

    dp = Dispatcher()
    dp.include_router(routers)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())