import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_resume_direct(resume_text, job_description):
    # Using the standard REST endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"Analyze this resume: {resume_text} for this JD: {job_description}. Return JSON with match_score, matched_skills, missing_skills, suggestions."
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json",
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            # Extracting text from the Google response structure
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {result}"
    except Exception as e:
        return f"System Error: {e}"

if __name__ == "__main__":
    print("--- Testing Direct Connection (No SDK) ---")
    res = analyze_resume_direct("Python Dev", "Need Python")
    print(res)