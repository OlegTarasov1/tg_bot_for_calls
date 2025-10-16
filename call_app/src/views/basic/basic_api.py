from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.async_sql_requests.call_requests import AsyncCallRequets
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from pydantic import ValidationError
from utils.keyboards.kb_temp import temp_kb
from aiogram.fsm.context import FSMContext
from schemas.fsm_schemas.call_schedule import ScheduleState
from tasks.worker.tasks import send_message_to_user
from uuid import uuid4
from datetime import datetime, timedelta, time as time_dt
import logging
from celery.schedules import crontab
from zoneinfo import ZoneInfo
from schemas.raw_templates.template_call import get_call_text_template



basic_router = Router()


@basic_router.message(Command("set_call"))
async def start_handler(
    msg: Message,
    state: FSMContext
):
    user = await AsyncRequestsUser.get_user_by_id(
        id = msg.from_user.id
    )
    await state.set_state(ScheduleState.schedule_time)

    await msg.answer(
        "Напишите время и день недели в формате:\n'время\n\n23:00\n\nНапишите: 'отмена', чтобы отменить ввод."
    )

    if not user:
        try:
            user_data = UserTemplate(
                **msg.from_user.model_dump(),
                chat_id = msg.chat.id
            )

            await AsyncRequestsUser.new_user(
                from_user = user_data
            )

        except ValidationError:
            logging.warning("что-то не так с данными: " + msg.from_user)

    else:
        pass


@basic_router.message(ScheduleState.schedule_time)
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
            await state.set_state(ScheduleState.schedule_date)
            await msg.answer("Отправьте дату в формате:\n<формат>")
        except TypeError:
            # await state.clear()
            await msg.answer("Не корректный формат, попробуйте снова.")



@basic_router.message(ScheduleState.schedule_date)
async def schedule_date(msg: Message, state: FSMContext):
    receipt = msg.text.strip()
    
    if receipt.strip() == 'отмена':
        await state.clear()
        await msg.answer("Ввод отменён") 
    else:
        chat_id = msg.chat.id
        meta_data = await state.get_data()

        # try:
        moscow_tz = ZoneInfo("Europe/Moscow")
        now_moscow = datetime.now(moscow_tz)
        dates_list = msg.text.strip().split(", ")
        call_invoke_id = None
        eta_time = datetime.combine(
            now_moscow.date(),
            meta_data.get('time'),
            tzinfo = moscow_tz
        )

        logging.warning(eta_time)

        if str(now_moscow.weekday()) in dates_list and now_moscow <= eta_time:
            logging.warning("ok, it passed the filter")
            call_invoke_id = f"task_{uuid4()}"
            send_message_to_user.apply_async(
                args = [
                    get_call_text_template(meta_data['time']),
                    chat_id
                ],
                eta = eta_time
            )
            logging.warning(eta_time)

        new_call = await AsyncCallRequets.add_call(
            call_invoke_id = call_invoke_id,
            master_name = "Test",
            call_link = "https://test",
            call_purpose = "test",
            time = meta_data['time'],
            days_of_the_week = dates_list
        )
        await AsyncRequestsUser.update_user_call_group(
            call_id_to_update = new_call.id,
            user_id = msg.from_user.id
        )

        await msg.answer(f"Хорошо, всё устанновлено: {new_call.time} | {new_call.call_purpose}")
        await state.clear()
        # except:
        #     pass

















    # if receipt == "Утро (8:00)":
    #     await AsyncRequestsUser.update_user_call_group(
    #         user_id = msg.from_user.id,
    #         call_id_to_update = 1
    #     )
    #     await msg.answer(
    #         "Время установлено на 8:00 успешно.",
    #         reply_markup = ReplyKeyboardRemove()
    #     )
    # elif receipt == "Вечер (18:00)":
    #     await AsyncRequestsUser.update_user_call_group(
    #         user_id = msg.from_user.id,
    #         call_id_to_update = 2
    #     )
    #     await msg.answer(
    #         "Вемя установлено на 18:00 успешно.",
    #         reply_markup = ReplyKeyboardRemove()
    #     )
    # else:
    #     await msg.answer(
    #         "Что-то пошло не так, время не было изменино.",
    #         reply_markup = ReplyKeyboardRemove()
    #     )