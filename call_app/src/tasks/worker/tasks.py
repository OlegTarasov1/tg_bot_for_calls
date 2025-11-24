from config.redis_config import RedisEnv
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.extra_funcs.send_message import send_message
from schemas.raw_templates.template_call import get_call_text_template
from celery import Celery
from datetime import datetime, timedelta
import asyncio
import os
import logging
from zoneinfo import ZoneInfo


settings = RedisEnv()

app = Celery(
    "tasks",
    broker = settings.redis_url,
    backend = settings.redis_url
)

app.conf.timezone = "Europe/Moscow"

@app.task()
def send_message_to_user(
    msg: str,
    chat_id: int
):
    asyncio.run(
        send_message(
            message = msg,
            chat_id = chat_id
        )
    )


@app.task()
def load_invites():
    moscow_tz = ZoneInfo("Europe/Moscow")
    logging.info(f'time executed: {datetime.now(moscow_tz)}')
    send_message_to_user.apply_async(
        args=[
            "start",
            5613879654
        ],
        eta = datetime.now(moscow_tz)
    )
    today_calls = asyncio.run(
        AsyncCallRequets.get_todays_calls(
            str(datetime.today().weekday())
        )
    )
    for i in today_calls:
        for j in i.employees:
            call_time = datetime.combine(datetime.now(moscow_tz).date(), i.time)
            logging.warning(call_time)
            if datetime.now(moscow_tz) <= call_time.replace(tzinfo = moscow_tz):
                send_message_to_user.apply_async(
                    args=[
                        get_call_text_template(call_time),
                        j.chat_id
                    ],
                    eta = call_time
                )
            else:
                logging.warning(f"time now: {datetime.now(moscow_tz)} > {call_time}")
