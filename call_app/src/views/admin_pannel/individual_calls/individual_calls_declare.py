from schemas.fsm_schemas.individual_call_setup import IndividualCallState
from aiogram.fsm.context import FSMContext
from tasks.worker.tasks import send_message_to_user
from schemas.ai_sctructs.date_and_time_schema import DateAndTimeSchema
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from ai_helper.ai import get_ai
from utils.async_sql_requests.call_requests import AsyncCallRequets
from .switch_case_call_state import get_new_state
import logging


individual_call_handler = Router()


@individual_call_handler.callback_query(F.data == "set_individual_call")
async def setup_individual_call(
    query: CallbackQuery,
    state: FSMContext
):
    await state.set_state(IndividualCallState.validation)
    await state.set_data({"call_data": DateAndTimeSchema()})
    await query.message.answer("Отправьте время, дату, причину и ссылку для индивидульного созвона в свободной форме.\n\nЕсли вы случайно нажали эту кнопку - напишите 'отмена'")


@individual_call_handler.message(IndividualCallState.validation)
async def insufficient_values_check(
    message: Message,
    state: FSMContext
):
    if message.text.strip().lower() == "отмена":
        await state.clear()
        await message.answer("всё, действие отменено")
    else:
        received_data = await state.get_data()
        received_data = received_data.get("call_data")
        ai_result = await get_ai(
            f"Ты устанавливаешь скрам созвон. Верни дату, время, цель созвона, какие-то данные человека, с которым нужно установить созвон и ссылку на созвон из текста. Ответ верни в ISO формате YYYY-MM-DD\nТекст:\n{message.text.strip()}\nУчти, что сейчас: {datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")}. если не нашёл - верни None"
        )

        final_data = ai_result

        if received_data:
            for field_name, value in received_data.model_dump().items():
                if value is None:
                    new_value = getattr(ai_result, field_name, None)
                    if new_value is not None:
                        setattr(received_data, field_name, new_value)
            final_data = received_data

        insufficiant_data = await get_new_state(final_data.model_dump())


        if insufficiant_data:
            await message.answer(f"Не получил данные:\n{'\n'.join(insufficiant_data)}")
        else:
            await state.update_data({"call_data": final_data})

            user = await AsyncRequestsUser.get_user_by_creds(final_data.user_data)
            await message.answer(f"Всё корректно?\n\nTime: {final_data.call_time}\nDate: {final_data.call_date}\nPurpose: {final_data.call_purpose}\nLink: {final_data.call_link}\nUsername: {final_data.user_data}")
            await message.answer(f"{user.username} | {user.job_title} | {user.first_name.upper()}, {user.last_name.upper()}")
            await state.set_state(IndividualCallState.final_check)


@individual_call_handler.message(IndividualCallState.final_check)
async def final_check(
    message: Message,
    state: FSMContext
):
    if message.text.strip().lower() == "отмена":
        await state.clear()
        await message.answer("всё, действие отменено")
    elif message.text.strip().lower() == "да":
        received_data = await state.get_data()
        await state.clear()
        received_data = received_data.get("call_data")

        await message.answer(f"Всё получено.\n\nTime: {received_data.call_time}\nDate: {received_data.call_date}\nPurpose: {received_data.call_purpose}\nLink: {received_data.call_link}")





# @individual_call_handler.message(IndividualCallState.call_purpose)
# async def setup_call_purpose():
#     pass


# @individual_call_handler.message(IndividualCallState.call_link)
# async def setup_call_link():
#     pass


# @individual_call_handler.message(IndividualCallState.final_check)
# async def ai_for_call_setup(
#     msg: Message,
#     state: FSMContext
# ):
#     await state.clear()
#     ai_result = await get_ai(
#         f"верни дату и время из текста. Ответ верни в ISO формате YYYY-MM-DD\nТекст:\n{msg.text.strip()}\nУчти, что сейчас: {datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")}. если не нашёл - верни None"
#     )

#     if ai_result.call_time:
#         await msg.answer(f"Данные выявленны корректно?:\nВремя: {ai_result.call_time.strftime('%H:%M')}\nДата: {ai_result.call_date.isoformat()}")

#         await state.set_state(IndividualCallState.verification)
#         await state.update_data(verification = ai_result)

#     else:
#         await state.set_state(IndividualCallState.time_for_call)
#         await msg.answer(f"не смог уловить время, попробуйте снова. Дата выявлено корректно?:\n{ai_result.call_date.isoformat()}")


# @individual_call_handler.message(IndividualCallState.verification)
# async def verification_check(
#     msg: Message,
#     state: FSMContext
# ):
#     data = await state.get_data()
#     await state.clear()
#     if not msg.text.lower().strip() in ["да", "нет", "отмена"]:
#         await state.clear()
#     else:
#         match msg.text.lower().strip():
#             case "да":
                
#                 send_time = datetime.combine(
#                     data.get('verification').call_date,
#                     data.get('verification').call_time
#                 ).replace(tzinfo=ZoneInfo("Europe/Moscow"))

#                 link = send_message_to_user.apply_async(
#                     args = [
#                         "some text",
#                         msg.chat.id
#                     ],
#                     eta = send_time
#                 )
#                 await msg.answer(f"ок, отработало...\nDate: {data.get('verification').call_date}\nTime: {data.get('verification').call_time}")

#             case "нет":
#                 await msg.answer("Понял, попробуйте снова ввести дату и время")
#                 await state.set_state(IndividualCallState.time_for_call)
#             case _:
#                 pass


