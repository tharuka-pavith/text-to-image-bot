import os
from fastapi import FastAPI
from uvicorn import run
from models.models import HumanMessageModel, AIMessageModel
from handlers.chat_handler import chat_agent_response
from dotenv import load_dotenv
load_dotenv()

description = """
GAN Based Text to Image Synthesizer API
### Description

Generate images according to text descriptions.

"""
tags_metadata = [
    {
        "name": "chat-bot",
        "description": "Endpoint to chat with the bot",
    },
]

app = FastAPI(
    title="Text-to-Image Bot API (dev)",
    description=description,
    version="0.1.0",
    openapi_tags=tags_metadata
)


@app.post("/chat-bot", description="Endpoint to chat with the bot",tags=["chat-bot"])
def chat_endpoint(chat: HumanMessageModel) -> AIMessageModel:
    response = chat_agent_response(chat)
    return response


if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)
