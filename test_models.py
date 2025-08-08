import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
