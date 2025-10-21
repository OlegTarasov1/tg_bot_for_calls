# from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
# from utils.async_sql_requests.call_requests import AsyncCallRequets
# from schemas.fsm_schemas.call_schedule import ScheduleState
# from aiogram.fsm.context import FSMContext
# from utils.keyboards.kb_temp import temp_kb
# from aiogram.types import CallbackQuery
# from aiogram import Router, F
# from utils.keyboards.menu_kb.employee_kb import employee_menu
# import logging



# reschedule_router = Router()


# @reschedule_router.callback_query(RetreiveCallCB.filter(F.action == "reschedule"))
# async def reschedule_handler(
#     query: CallbackQuery,
#     callback_data: RetreiveCallCB,
#     state: FSMContext
# ):
#     await AsyncCallRequets.delete_call_by_ids(
#         user_id = callback_data.user_id,
#         call_id = callback_data.call_id
#     )
#     await state.set_state(ScheduleState.schedule)
    
#     await query.message.edit_reply_markup(
#         reply_markup = employee_menu
#     )

#     await query.message.answer(
#         text = "К какому созвону вы бы хотели присоединиться?",
#         reply_markup = temp_kb
#     )


