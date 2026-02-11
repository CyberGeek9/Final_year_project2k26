import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("--- Checking API Key Access ---")
try:
    # This is the correct way to list models in the new SDK
    for m in client.models.list():
        print(f"Model Name: {m.name} | Supported: {m.supported_variant_names}")
except Exception as e:
    print(f"Error: {e}")