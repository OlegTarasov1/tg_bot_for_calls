from utils.extra_funcs.send_message import send_message
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.async_sql_requests.call_requests import AsyncCallRequets
from config.database_config import EnvData 
import logging


settings = EnvData()

async def invite_to_call(
    msg: str,
    call_id: int
):
    users_to_send_messages_to = await AsyncCallRequets.get_users_for_call(
        call_id = call_id
    )

    if users_to_send_messages_to:
        for i in users_to_send_messages_to:
            await send_message(
                token = settings.BOT_TOKEN.get_secret_value(),
                chat_id = i.chat_id,
                message = msg
            )
    else:
        logging.info(f"no users to send the messsage: \"{msg}\" to")