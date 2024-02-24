from fastapi import FastAPI
from uvicorn import run
from chat_models.openai_model import get_chat_openai_chain
from langchain.memory import ChatMessageHistory
from models.models import HumanMessageModel, AIMessageModel

app = FastAPI()
chain = get_chat_openai_chain()
chat_history = ChatMessageHistory()


@app.post("/chat-bot")
def chat_endpoint(chat: HumanMessageModel) -> AIMessageModel:
    chat_history.add_user_message(chat.human_msg)
    result = chain.invoke({"messages": chat_history.messages}).dict()
    chat_history.add_ai_message(result['content'])
    return AIMessageModel(ai_msg=result["content"])


if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)
