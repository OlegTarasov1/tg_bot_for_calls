from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from aiogram import Router, F
from schemas.fsm_schemas.call_reschedule import RescheduleState
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

reschedule_call_router = Router()


@reschedule_call_router.callback_query(RetreiveCallCB.filter(F.action == "reschedule"))
async def reschedule_handler(
    cb: CallbackQuery,
    callback_data: RetreiveCallCB,
    state: FSMContext
):
    await state.set_state(RescheduleState.schedule_time)
    await state.update_data({"id": callback_data.call_id})
    await cb.message.answer("Напишите время для оповещений о созонах в формате: '8:00' (час:минута).")