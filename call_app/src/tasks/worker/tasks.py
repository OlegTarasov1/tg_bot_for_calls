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
    call_id: int = 3
):
    call_with_users = asyncio.run(
        AsyncCallRequets.get_users_for_call(
            call_id = call_id
        )
    )

    if call_with_users.employees:            
        for i in call_with_users.employees:
            msg = f"""
            У вас назначен созвон.\n\n
            ссылка: {call_with_users.call_link}\n\n
            цель созвона: {call_with_users.call_purpose}\n
            скрам-мастер: {call_with_users.master_name}"""
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