from utils.async_sql_requests.user_requests import AsyncRequestsUser
from celery.schedules import crontab
from config.redis_config import RedisEnv
from tasks.worker.tasks import (
    send_message_to_user
)
from celery import Celery
import asyncio
import logging


settings = RedisEnv()

app = Celery(
    "beat",
    broker = settings.redis_url,
    backend = settings.redis_url
)

app.conf.timezone = "Europe/Moscow"

app.conf.beat_schedule = {
    "daily_morning_call_invites": {
        "task": "tasks.worker.tasks.common_invites",
        "schedule": crontab(
            hour = "8",
            day_of_week = "mon-fri",
        ),
        "args": (
            2,
        )
    },
    "daily_evening_call_invites": {
        "task": "tasks.worker.tasks.common_invites",
        "schedule": crontab(
            hour = "18",
            day_of_week = "mon-fri",
        ),
        "args": (
            3,
        )
    }
}


