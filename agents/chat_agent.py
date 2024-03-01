import re
from typing import Sequence
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from dotenv import load_dotenv
from tools.stabilityai_text_to_image import generate_image
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from langchain.memory import ChatMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()


class AIOutput(BaseModel):
    ai_msg: str | None = Field("Your response for the user message")
    image_url: str | None = Field("URL of the generated image")

    def to_dict(self):
        return {"ai_msg": self.ai_msg, "image_url": self.image_url}


parser = PydanticOutputParser(pydantic_object=AIOutput)
output_format = parser.get_format_instructions()


tools: Sequence = [generate_image]

# Choose the LLM that will drive the agent
chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

SYSTEM_MESSAGE = """
Your name is Cortana, an AI assistant. Your job is to help user to generate images according to text prompt 
developed by interacting with the user. First of all you must get all the details like colors, background, 
composition etc.. from the user and finally create a good text prompt and show it to the user. 
Then, if the user approves, use the tool to generate an image according to that prompt. 
That tool will return a URL of the generated image.
You should present it to the user and get feedback to improve the prompt and generate the image recursively. 
You should iterate this proces until user is satisfied.

Do not assist user to generate text prompts with adult content or abusive content.
Your only job is to assist user to generate images according to developed text prompt. 
Do not assist with anything else!  
"""

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


x = '''

Follow the following output format:
{output_format}
Value for "Url" is not always required. It can return the link for the generated image otherwise it can be null.'''