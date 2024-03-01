from chat_models.openai_model import get_chat_openai_chain
from langchain.memory import ChatMessageHistory
from models.models import HumanMessageModel, AIMessageModel
from agents.chat_agent import get_openai_tools_agent

chain = get_chat_openai_chain()
chat_history = ChatMessageHistory()


def respond_human_message(msg: HumanMessageModel) -> AIMessageModel:
    chat_history.add_user_message(msg.human_msg)
    result = chain.invoke({"messages": chat_history.messages}).dict()
    chat_history.add_ai_message(result['content'])
    return AIMessageModel(ai_msg=result["content"])


def chat_agent_response(msg: HumanMessageModel) -> AIMessageModel:
    agent_executor = get_openai_tools_agent()
    chat_history.add_user_message(msg.human_msg)
    result = agent_executor.invoke({"messages": chat_history.messages})
    chat_history.add_ai_message(result["output"])
    return AIMessageModel(ai_msg=result["output"], url=None)


if __name__ == "__main__":
    while True:
        msg = input("[user]>>> ")
        if msg == "/exit":
            break
        chat_history.add_user_message(msg)
        response = chat_agent_response(HumanMessageModel(human_msg=msg)).dict()
        # print(response)
        chat_history.add_ai_message(response["ai_msg"])
        print("[assistant]>>> ", response["ai_msg"])
