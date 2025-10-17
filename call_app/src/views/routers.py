from views.mutual_cbs.return_to_menue.go_to_menue import back_to_menue_router
from views.mutual_cbs.return_to_menue.shutters import shutter_router
from .basic.basic_api import basic_router 
from aiogram import Router


routers = Router()
routers.include_routers(basic_router)
routers.include_router(back_to_menue_router)
routers.include_router(shutter_router)