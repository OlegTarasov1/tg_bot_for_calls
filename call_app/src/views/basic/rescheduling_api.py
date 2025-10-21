from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.async_sql_requests.call_requests import AsyncCallRequets
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from pydantic import ValidationError
from utils.keyboards.kb_temp import temp_kb
from aiogram.fsm.context import FSMContext
from schemas.fsm_schemas.call_reschedule import RescheduleState
from tasks.worker.tasks import send_message_to_user
from uuid import uuid4
from datetime import datetime, time as time_dt
import logging
from zoneinfo import ZoneInfo
from schemas.raw_templates.template_call import get_call_text_template
from celery.result import AsyncResult
from tasks.worker.tasks import app



rescheduling_router = Router()


@rescheduling_router.message(RescheduleState.schedule_time)
async def set_schedule(msg: Message, state: FSMContext):
    receipt = msg.text.strip()
    
    if receipt.strip() == 'отмена':
        await state.clear()
        await msg.answer("Ввод отменён") 
    else:
        try:
            hours, minutes = map(int, receipt.strip().split(":"))
            time = time_dt(hours, minutes)
            await state.update_data({"time": time})
            await state.set_state(RescheduleState.schedule_date)
            await msg.answer("Отправьте дни недели как цифры через запятые:\n0 - понедельник\n1 - вторник\n2 - среда\n\nНу или введите 'отмена'")
        except TypeError:
            # await state.clear()
            await msg.answer("Не корректный формат, попробуйте снова.")



@rescheduling_router.message(RescheduleState.schedule_date)
async def schedule_date(msg: Message, state: FSMContext):
    receipt = msg.text.strip()
    
    if receipt.strip() == 'отмена':
        await state.clear()
        await msg.answer("Ввод отменён") 
    else:
        chat_id = msg.chat.id
        meta_data = await state.get_data()

        call_data = await AsyncCallRequets.retreive_call(call_id = meta_data.get("id"))
        await AsyncCallRequets.delete_call_by_id(id = meta_data.get("id"))
        if call_data.call_invoke_id:
            AsyncResult(id = call_data.call_invoke_id, backend = app).revoke(terminate = True, signal = "SIGKILL")


        try:
            moscow_tz = ZoneInfo("Europe/Moscow")
            now_moscow = datetime.now(moscow_tz)
            dates_list = msg.text.strip().split(", ")
            call_invoke_id = None
            eta_time = datetime.combine(
                now_moscow.date(),
                meta_data.get('time'),
                tzinfo = moscow_tz
            )

            if str(now_moscow.weekday()) in dates_list and now_moscow <= eta_time:
                call_metadata = send_message_to_user.apply_async(
                    args = [
                        get_call_text_template(meta_data['time']),
                        chat_id
                    ],
                    eta = eta_time
                )
                call_invoke_id = call_metadata.id
                logging.warning(eta_time)

            new_call = await AsyncCallRequets.add_call(
                call_invoke_id = call_invoke_id,
                master_name = "Рома Нгуен",
                call_link = "https://teams.microsoft.com/l/meetup-join/19:2vRT5we1Hzd5CfgVm9uqKE1i3t6IYwRmAcu2eCWCqBQ1@thread.tacv2/1745468981665?context=%7B%22Tid%22:%22ef3ef297-42e1-4a5e-b9b0-4f558960a875%22,%22Oid%22:%227d076506-0e4c-4560-b727-0fe7a8ee4501%22%7D",
                call_purpose = "регулярный scrum созвон",
                time = meta_data['time'],
                days_of_the_week = dates_list
            )
            await AsyncRequestsUser.update_user_call_group(
                call_id_to_update = new_call.id,
                user_id = msg.from_user.id
            )

            await msg.answer(f"Хорошо, всё устанновлено: {new_call.time} | {new_call.call_purpose}")
            await state.clear()
        except:
            await msg.answer("некорректный ввод. введите через запятую:\n0 - понедельник,\n1 - втотрник,\n2 - среда...")



