from aiogram import Router, F
from aiogram.types import message, CallbackQuery


shutter_router = Router()


@shutter_router.callback_query(F.data == "shutter")
async def shutter_handler(
    cb: CallbackQuery
):
    await cb.answer("Заглушка: функция пока не работает.")