from config.redis_config import RedisEnv
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.extra_funcs.send_message import send_message
from schemas.raw_templates.template_call import get_call_text_template
from celery import Celery
from datetime import datetime
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
    date: str
):
    today_calls = await AsyncCallRequets.get_todays_calls(date)
    for i in today_calls:
        asyncio.create_task(
            send_message_to_user(
                get_call_text_template(datetime.now().time()),
                i.employees.chat_id
            )
        )


@app.task()
def load_invites():
    asyncio.run(
        load_invites_today_async(
            date = str(datetime.today().weekday())
        )
    )