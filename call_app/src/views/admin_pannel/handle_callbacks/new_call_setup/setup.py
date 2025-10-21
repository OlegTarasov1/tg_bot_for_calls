from views.admin_pannel.handle_callbacks.new_call_setup.time_choice.choice_router import choice_router
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from schemas.fsm_schemas.call_schedule import ScheduleState
from utils.keyboards.kb_temp import temp_kb
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F


new_call_router = Router()
new_call_router.include_router(choice_router)


@new_call_router.callback_query(F.data == "setup_new_call")
async def new_call(
    callback_data: CallbackQuery,
    state: FSMContext
):
    await callback_data.message.delete()

    await state.set_state(ScheduleState.schedule_time)

    await callback_data.message.answer(
        "Напишите время для оповещений о созонах в формате: '8:00' (час:минута)."
    )
