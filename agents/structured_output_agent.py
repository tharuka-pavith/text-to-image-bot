#  Copyright (c) 2024. Tharuka Pavith
#  For the full license text, see the LICENSE file.
#

from typing import Sequence
from dotenv import load_dotenv
from tools.stabilityai_text_to_image import generate_image
from prompts.chat_agent_prompts import SYSTEM_MESSAGE
from langchain_core.pydantic_v1 import BaseModel, Field
import json
from langchain_core.agents import AgentActionMessageLog, AgentFinish
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

load_dotenv()
tools: Sequence = [generate_image]

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


class Response(BaseModel):
    """Final response to the input message"""
    chatbot_message: str = Field(description="Your Response to the message asked")
    url: str = Field(description="URL returned by `generate_image` tool")


def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"assistant": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )


llm_with_tools = llm.bind_functions([generate_image, Response])

agent = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"],
                # Format agent scratchpad from intermediate steps
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | parse
    )


def get_openai_tools_agent() -> AgentExecutor:
    executor = AgentExecutor(tools=[generate_image], agent=agent, verbose=True)
    return executor


if __name__ == "__main__":
    chat_history = ChatMessageHistory()

    agent_executor = get_openai_tools_agent()

    while True:
        user_msg = input("[user]>>> ")
        if user_msg == "/exit":
            break
        # chat_history.add_user_message(user_msg)
        result = agent_executor.invoke(
            {"input": [HumanMessage(user_msg)], "chat_history": chat_history.messages},
            return_only_outputs=True,
        )
        chat_history.add_user_message(user_msg)

        try:
            chat_history.add_ai_message(result["assistant"]
                                        + "| url: " + result["url"])
        except KeyError as key_err:
            chat_history.add_ai_message(result["assistant"])
        except Exception as e:
            print("Error adding ai message: ", e)

        print(result)
        # print("[assistant]>>> ", result["output"])
