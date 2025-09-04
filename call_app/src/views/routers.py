from aiogram import Router
from .basic.basic_api import basic_router 


routers = Router()
routers.include_routers(basic_router)