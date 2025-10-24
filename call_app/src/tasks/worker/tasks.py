from config.redis_config import RedisEnv
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.extra_funcs.send_message import send_message
from schemas.raw_templates.template_call import get_call_text_template
from celery import Celery
from datetime import datetime, timedelta
import asyncio
import os


settings = RedisEnv()

app = Celery(
    "tasks",
    broker = settings.redis_url,
    backend = settings.redis_url
)


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


async def load_invites_today_async(
    date: int
):
    today_calls = await AsyncCallRequets.get_todays_calls(date)
    for i in today_calls:
        for j in i.employees:
            call_time = datetime.combine(datetime.now().date(), i.time)
            
            send_message_to_user.apply_async(
                args=[
                    get_call_text_template(call_time),
                    j.chat_id
                ],
                eta = call_time
            )



@app.task()
def load_invites():
    asyncio.run(
        load_invites_today_async(
            date = str(datetime.today().weekday())
        )
    )