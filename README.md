[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## GAN-based Text-to-Image Synthesizer Chatbot API

This repository provides a chatbot API that utilizes a Generative Adversarial Network (GAN) to generate images based on textual descriptions. 

**Features:**

* Chat-bot API endpoint.
* Swagger docs for the endpoints.
* You can integrate the API into your chatbot application UI.

**Requirements:**

* Python 3.8+
* Additional dependencies listed in `requirements.txt`
* Firebase Storage configured (You should have secrets with you)
* OpenAI API key
* Hugging Face Hub API token

**Installation:**

1. Clone this repository.
1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
1. Configure `.env` file.
   ```
   OPENAI_API_KEY=<replace with original value>
   GOOGLE_APPLICATION_CREDENTIALS=<replace with original value>
   TYPE=<replace with original value>
   PROJECT_ID=<replace with original value>
   PRIVATE_KEY_ID=<replace with original value>
   PRIVATE_KEY=<replace with original value>
   CLIENT_EMAIL=<replace with original value>
   CLIENT_ID=<replace with original value>
   AUTH_URI=<replace with original value>
   TOKEN_URI=<replace with original value>
   AUTH_PROVIDER_X509_CERT_URL=<replace with original value>
   CLIENT_X509_CERT_URL=<replace with original value>
   UNIVERSE_DOMAIN=<replace with original value>
   HUGGINGFACEHUB_API_TOKEN=<replace with original value>
   ```
   You can get `OPENAI_API_KEY` from openAI's website. Other secret keys are for the configuration of Firebase and Hugging Face.

**Usage:**

1. Start the chatbot API server by running `main.py`
2. Go to `http://localhost:8000/docs#/` to view documentation of the API.

**Contributing:**

Please refer to the CONTRIBUTING.md file for guidelines.

**License:**

This project is licensed under the [MIT License](LICENSE).
