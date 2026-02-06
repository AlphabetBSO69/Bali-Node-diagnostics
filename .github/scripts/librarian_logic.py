import os
import json
import google.generativeai as genai
from datetime import datetime
import re

# --- CONFIGURATION ---
INBOX_PATH = "directives/inbox.json"
ARCHIVE_PATH = "archive.json"

def activate_node():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        if not os.path.exists(INBOX_PATH):
            print("Inbox missing.")
            return
            
        with open(INBOX_PATH, 'r') as f:
            raw_content = f.read()
            
        # RESILIENCE LOGIC: Find the first JSON object in the mess
        json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if json_match:
            inbox_data = json.loads(json_match.group(0))
            user_query = inbox_data.get("query", "")
        else:
            print("No valid JSON found in inbox noise.")
            return

        if not user_query or user_query.strip() == "":
            print("Inbox is empty. Standing by.")
            return
            
    except Exception as e:
        print(f"Extraction failed: {e}")
        return

    # Synthesis
    prompt = f"You are the Librarian of Node [V_STATE_ZERO]. Respond with sovereign wit: {user_query}"
    
    try:
        response = model.generate_content(prompt)
        synthesis = response.text
    except Exception as e:
        print(f"API Synthesis Failed: {e}")
        return

    # Archive Update
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": user_query,
        "synthesis": synthesis
    }

    try:
        history = []
        if os.path.exists(ARCHIVE_PATH):
            with open(ARCHIVE_PATH, 'r') as f:
                try:
                    history = json.load(f)
                except: history = []
        
        history.insert(0, new_entry)
        with open(ARCHIVE_PATH, 'w') as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Archive write failed: {e}")

    # CLEAN SLATE: Hard-reset the inbox to clear all noise
    with open(INBOX_PATH, 'w') as f:
        json.dump({"query": "", "status": "waiting"}, f, indent=4)

    print("Synthesis Complete. Archive Updated and Noise Cleared.")

if __name__ == "__main__":
    activate_node()