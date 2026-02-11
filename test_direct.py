import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def test_gemini_final():
    # Using v1beta as it has the best support for responseMimeType
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # PAYLOAD FIX: Use responseMimeType (Camel Case)
    payload = {
        "contents": [{
            "parts": [{"text": "Analyze this: Resume: Python Dev. JD: Python Expert. Return JSON: {score: 90}"}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    print("--- Connecting to Gemini 1.5 Flash (v1beta) ---")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # Extracting the AI output
            text_output = result['candidates'][0]['content']['parts'][0]['text']
            print("\n✅ SUCCESS! AI Response:")
            print(text_output)
            return True
        else:
            print(f"\n❌ FAILED with Status Code: {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"\n⚠️ System Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_final()