from config.redis_config import RedisEnv
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.extra_funcs.send_message import send_message
from celery import Celery
import asyncio
import os


settings = RedisEnv()

app = Celery(
    "tasks",
    broker = settings.redis_url,
    backend = settings.redis_url
)


@app.task()
def common_invites(
    msg: str,
    call_id: int = 1
):
    users_list = asyncio.run(
        AsyncCallRequets.get_users_for_call(
            call_id = call_id
        )
    )

    for i in users_list:
        asyncio.run(
            send_message(
                message = msg,
                chat_id = i.chat_id
            )
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