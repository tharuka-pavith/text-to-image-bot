#  Copyright (c) 2024. Tharuka Pavith
#  For the full license text, see the LICENSE file.
#

import datetime
import io
import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from firebase.firebase_config import upload_blob

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}


@tool
def generate_image(prompt: str) -> str:
    """Use this function to generate image according to the given text prompt
    and to get the url of the generated image."""
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    # return response.content
    image_bytes = response.content
    # image_bytes = generate_image(Input(inputs="Astronaut riding a horse"))
    image = io.BytesIO(image_bytes)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Format example: 20240304_154625
    with image as f:
        url = upload_blob(f, f"{timestamp}.jpg")
        return str(url)


if __name__ == "__main__":
    # image_bytes = generate({"inputs": "A black benz car on the moon", })
    url = generate_image("A dog sleeping under a tree")
    print(url)
