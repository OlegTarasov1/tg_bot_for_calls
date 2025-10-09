from schemas.ai_sctructs.date_and_time_schema import DateAndTimeSchema
from langchain.chat_models import init_chat_model
from langchain.schema import AIMessage
from asyncio import sleep
from asyncio import Semaphore
import os


sem = Semaphore()


async def get_ai(
    message: str
) -> DateAndTimeSchema:
    llm = init_chat_model(
        model = os.getenv("AI_MODEL"),
        model_provider = os.getenv("AI_MODEL_PROVIDER"),
        api_key = os.getenv("GOOGLE_API_KEY")
    )
    structured_llm = llm.with_structured_output(DateAndTimeSchema)
    async with sem:

        await sleep(6)
        ai_response = await structured_llm.ainvoke(message)

    return ai_response


    





