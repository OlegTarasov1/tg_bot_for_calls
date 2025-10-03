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
    call_id: int
):
    call_with_users = asyncio.run(
        AsyncCallRequets.get_users_for_call(
            call_id = call_id
        )
    )

    if call_with_users.employees:            
        for i in call_with_users.employees:



            msg = f"""День добрый.       
     
Заглядывайте к нам на созвон!         
Сегодня после {call_with_users.time.strftime("%H:%M")} по москве!      
-----     
При входе пишите ПОЛНОЕ ИМЯ С ФАМИЛИЕЙ одинаково на всех созвонах. Чтобы Транскрибация созвона правильно учитывала ваши комментарии 

Когда вы вошли не ждите, когда вас заметят!      
Если возникла пауза в разговоре, берите инициативу и напоминайте о себе!   
Не выходите с созвона, пока не убедитесь, что вам ответили на все вопросы!     
Если вы не отвечаете — это не этично!      
В этом случае, к сожалению, по правилам студии мы ВЫНУЖДЕНЫ БУДЕМ ПРЕКРАТИТЬ С ВАМИ РАБОТУ.       

(Если вы спешите по делам, не бойтесь перебить нас, маякните нам и мы вас быстро отпустим. А если совсем не можете выйти на созвон, напишите мне в личные сообщения)     

Все созвоны компании идут с 7:00 до 12:00 и 18:00 до 23:00 (можно заходить на любой из них, если не успеваете. Ссылка всегда та же)

https://teams.microsoft.com/l/meetup-join/19:2vRT5we1Hzd5CfgVm9uqKE1i3t6IYwRmAcu2eCWCqBQ1@thread.tacv2/1745468981665?context=%7B%22Tid%22:%22ef3ef297-42e1-4a5e-b9b0-4f558960a875%22,%22Oid%22:%227d076506-0e4c-4560-b727-0fe7a8ee4501%22%7D
     
В конце созвона, говорите сколько процентов вы прочли книгу и наше обучение ! 

ПОСЛЕ ОКОНЧАНИИ СОЗВОНА НАПИШИТЕ МНЕ КАКОЕ ЗАДАНИЕ ВЫ ПОЛУЧИЛИ!"""



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