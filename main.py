import os
from fastapi import FastAPI
from uvicorn import run
from models.models import HumanMessageModel, AIMessageModel
from handlers.chat_handler import chat_agent_response
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()


@app.post("/chat-bot")
def chat_endpoint(chat: HumanMessageModel) -> AIMessageModel:
    response = chat_agent_response(chat)
    return response


if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)
