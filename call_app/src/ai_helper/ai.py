from langchain.chat_models import init_chat_model
import os


async def start_ai():
    model = init_chat_model(
        model = os.getenv("AI_MODEL"),
        model_provider = os.getenv("AI_MODEL_PROVIDER")
    )

    





