from aiogram import Router, F


individual_call_handler = Router()


@individual_call_handler.callback_query()
async def setup_individual_call():
    pass