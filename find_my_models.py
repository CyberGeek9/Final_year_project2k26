import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def list_allowed_models():
    # This endpoint returns a list of all models available to your key
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print("--- Fetching Available Models from Google ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Models Found:")
            for model in data.get('models', []):
                # Print just the name to keep it clean
                print(f"- {model['name']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"⚠️ System Error: {e}")

if __name__ == "__main__":
    list_allowed_models()