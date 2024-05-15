#  Copyright (c) 2024. Tharuka Pavith
#  For the full license text, see the LICENSE file.
#

from typing import Sequence
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from tools.stabilityai_text_to_image import generate_image
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ChatMessageHistory
from prompts.chat_agent_prompts import SYSTEM_MESSAGE

load_dotenv()
tools: Sequence = [generate_image]
# Choose the LLM that will drive the agent
chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


def get_openai_tools_agent() -> AgentExecutor:
    agent = create_openai_tools_agent(chat, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return executor


if __name__ == "__main__":
    chat_history = ChatMessageHistory()
    agent_executor = get_openai_tools_agent()
    while True:
        user_msg = input("[user]>>> ")
        if user_msg == "/exit":
            break
        chat_history.add_user_message(user_msg)
        result = agent_executor.invoke({"messages": chat_history.messages})
        chat_history.add_ai_message(result["output"])
        # print(result)
        print("[assistant]>>> ", result["output"])
