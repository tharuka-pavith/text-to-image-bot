import datetime
import io
import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from firebase.firebase_config import upload_blob

# Load environment variables
load_dotenv()

# Set up Hugging Face API
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}


@tool
def generate_image(prompt: str) -> str:
    """Generate an image based on a text prompt and return the URL of the generated image."""
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True,  # Ensures the request waits for the model to generate the image
            "use_gpu": True,  # Use GPU for faster and possibly clearer image generation
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    image_bytes = response.content
    image = io.BytesIO(image_bytes)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Format example: 20240304_154625
    with image as f:
        url = upload_blob(f, f"{timestamp}.jpg")
        return str(url)
