#  Copyright (c) 2024. Tharuka Pavith
#  For the full license text, see the LICENSE file.
#

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

load_dotenv()

system_msg = """
Your name is Cortana, an AI assistant. Your job is to help user to create a text prompt that can be used to generate 
an image by sending to a text-to-image synthesizer. You should get all the details like colors, background, composition
etc.. from the user and finally create a good text prompt. Do not assist user to generate text prompts with adult 
content or abusive content.
Your only job is to assist user to generate above text prompt. Do not assist with anything else!"""


def get_chat_openai_chain():
    chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    return prompt | chat


if __name__ == "__main__":
    chain = get_chat_openai_chain()
    chat_history = ChatMessageHistory()

    while True:
        user_msg = input("[user]>>> ")
        if user_msg == "/exit":
            break
        chat_history.add_user_message(user_msg)
        result = chain.invoke({"messages": chat_history.messages}).dict()
        chat_history.add_ai_message(result['content'])
        print("[assistant]>>> ", result['content'])

msg = '''You are 'Cortana', a helpful assistant. Answer all questions to the best of your ability. 
            Limit your response to maximum 50 words.'''
