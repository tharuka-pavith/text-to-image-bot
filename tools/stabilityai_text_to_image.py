import os
import requests
from dotenv import load_dotenv
from langchain.tools import BaseTool, StructuredTool, tool
from pydantic import BaseModel, Field


load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}


class Input(BaseModel):
    inputs: str = Field(description="Text prompt that is going to send to the image generator")


@tool
def generate_image(payload):
    """Use this function to generate image according to the given text prompt"""
    response = requests.post(API_URL, headers=headers, json=payload)
    # return response.content
    return "dummy.com/gummy_image.jpg"


# import io
# from PIL import Image
# image = Image.open(io.BytesIO(image_bytes))

if __name__ == "__main__":
    # image_bytes = generate_image({"inputs": "Astronaut riding a horse", })
    image_bytes = generate_image(Input(inputs="Astronaut riding a horse"))
    print("Hi")
