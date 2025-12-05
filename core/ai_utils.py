import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_rfp_structure(user_text):
    """
    Takes natural language text and returns a Python dictionary (JSON).
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # This prompt is the secret sauce. It strictly forbids markdown or extra text.
    prompt = f"""
    You are a procurement assistant. Extract structured data from this request.
    Return ONLY valid JSON. No markdown formatting, no backticks.
    
    User Request: "{user_text}"
    
    Required JSON Structure:
    {{
        "title": "Short summary of request",
        "budget": 0,
        "currency": "USD",
        "items": [
            {{ "name": "item name", "quantity": 0, "specs": "details" }}
        ],
        "timeline_days": 30,
        "warranty_years": 1
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        
        # Cleanup: Sometimes AI adds ```json at the start. We remove it.
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        
        # Convert string to actual Python Dictionary
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"AI Error: {e}")
        # Return a blank structure so the app doesn't crash
        return {"error": str(e)}
    
def parse_vendor_response(email_text):
    """
    Analyzes a vendor's email and extracts price, timeline, and a score.
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    You are a procurement expert. Analyze this vendor email proposal.
    Return ONLY valid JSON.
    
    Vendor Email: "{email_text}"
    
    Required JSON Structure:
    {{
        "total_price": 0, (Numeric value of the total cost found)
        "currency": "USD",
        "delivery_time": "e.g. 2 weeks",
        "warranty": "e.g. 1 year",
        "score": 0, (Rate this proposal 0-100 based on clarity and value)
        "rationale": "One short sentence explaining the score"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"AI Parse Error: {e}")
        return {"total_price": 0, "score": 0, "rationale": "Error parsing"}