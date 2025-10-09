from schemas.fsm_schemas.individual_call_setup import IndividualCallState
from aiogram.fsm.context import FSMContext
from tasks.worker.tasks import send_message_to_user
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from ai_helper.ai import get_ai
from utils.async_sql_requests.call_requests import AsyncCallRequets
import logging


individual_call_handler = Router()


@individual_call_handler.callback_query(F.data == "set_individual_call")
async def setup_individual_call(
    query: CallbackQuery,
    state: FSMContext
):
    await state.set_state(IndividualCallState.time_for_call)
    await query.answer("Отправьте время и дату для индивидульного созвона в свободной форме.\n\nЕсли вы случайно нажали эту кнопку - напишите 'отмена'")


@individual_call_handler.message(IndividualCallState.time_for_call)
async def ai_for_call_setup(
    msg: Message,
    state: FSMContext
):
    await state.clear()
    ai_result = await get_ai(
        f"верни дату и время из текста. Ответ верни в ISO формате YYYY-MM-DD\nТекст:\n{msg.text.strip()}\nУчти, что сейчас: {datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")}. если не нашёл - верни None"
    )

    if ai_result.call_time:
        await msg.answer(f"Данные выявленны корректно?:\nВремя: {ai_result.call_time.strftime('%H:%M')}\nДата: {ai_result.call_date.isoformat()}")

        await state.set_state(IndividualCallState.verification)
        await state.update_data(verification = ai_result)

    else:
        await state.set_state(IndividualCallState.time_for_call)
        await msg.answer(f"не смог уловить время, попробуйте снова. Дата выявлено корректно?:\n{ai_result.call_date.isoformat()}")


@individual_call_handler.message(IndividualCallState.verification)
async def verification_check(
    msg: Message,
    state: FSMContext
):
    data = await state.get_data()
    await state.clear()
    if not msg.text.lower().strip() in ["да", "нет", "отмена"]:
        await state.clear()
    else:
        match msg.text.lower().strip():
            case "да":
                
                send_time = datetime.combine(
                    data.get('verification').call_date,
                    data.get('verification').call_time
                ).replace(tzinfo=ZoneInfo("Europe/Moscow"))

                link = send_message_to_user.apply_async(
                    args = [
                        "some text",
                        msg.chat.id
                    ],
                    eta = send_time
                )
                await msg.answer(f"ок, отработало...\nDate: {data.get('verification').call_date}\nTime: {data.get('verification').call_time}")

            case "нет":
                await msg.answer("Понял, попробуйте снова ввести дату и время")
                await state.set_state(IndividualCallState.time_for_call)
            case _:
                pass


