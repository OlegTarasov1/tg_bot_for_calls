from config.redis_config import RedisEnv
from utils.extra_funcs.send_message import send_message
from .extra_funcs.process_tasks import invite_to_call
from celery import Celery
import asyncio


settings = RedisEnv()

app = Celery(
    "tasks",
    broker = settings.redis_url,
    backend = settings.redis_url
)


@app.task()
def message_before_call(
    msg: str,
    call_id: int
):
    asyncio.run(
        invite_to_call(
            msg=msg,
            call_id = call_id
        )
    )