import os
import requests
import json
import PyPDF2
import docx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# We use the exact name found in your list
MODEL_NAME = "gemini-flash-latest"

def extract_text(file_path):
    """Detects file type and extracts text."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == ".pdf":
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        return text.strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

# def call_gemini_ai(resume_text, job_description):
    """Calls Gemini using the Direct REST API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    prompt = f"""
    Act as an expert ATS. Compare the following Resume and Job Description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Return ONLY a JSON object with this structure:
    {{
        "match_score": (0-100),
        "matched_skills": [],
        "missing_skills": [],
        "suggestions": []
    }}
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            raw_response = response.json()
            # Navigate the Google JSON structure to get the AI text
            ai_json_str = raw_response['candidates'][0]['content']['parts'][0]['text']
            return json.loads(ai_json_str)
        else:
            return {"error": f"API Error {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": f"System Error: {str(e)}"}
    #  new logic for multiple /
def call_gemini_ai(resume_text, job_description):
    """Calls Gemini with a prompt designed for both Single and Batch modes."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    prompt = f"""
    Act as an expert ATS (Applicant Tracking System). Compare the following Resume and Job Description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Return ONLY a JSON object with this EXACT structure:
    {{
        "candidate_name": "Extract candidate full name",
        "email": "Extract email address",
        "phone": "Extract mobile number",
        "experience": "Extract total years of experience (e.g., 5 years)",
        "match_score": (integer between 0 and 100),
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill1", "skill2"],
        "suggestions": ["suggestion1", "suggestion2"]
    }}
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": { "responseMimeType": "application/json" }
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            raw_response = response.json()
            ai_json_str = raw_response['candidates'][0]['content']['parts'][0]['text']
            return json.loads(ai_json_str)
        else:
            return {"error": f"API Error {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    

# --- TESTING SECTION ---
if __name__ == "__main__":
    # 1. Provide a path to a real resume file on your computer to test
    # Example: test_resume_path = "C:/Users/YourName/Documents/my_resume.pdf"
    # For this test, we'll use a string if you don't have a file ready
    
    test_resume = "Skilled in Python, FastAPI, and PostgreSQL. 3 years experience."
    test_jd = "Looking for a Python Developer who knows FastAPI and SQL."

    print(f"--- Running Final Test with {MODEL_NAME} ---")
    result = call_gemini_ai(test_resume, test_jd)
    
    print("\n--- AI ANALYSIS RESULT ---")
    print(json.dumps(result, indent=4))