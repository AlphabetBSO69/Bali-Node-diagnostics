import os
import json
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
INBOX_PATH = "directives/inbox.json"
ARCHIVE_PATH = "archive.json"

def activate_node():
    # 1. Setup API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return

    genai.configure(api_key=api_key)
    
    # Using the standard stable model string
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. Read the Query
    try:
        if not os.path.exists(INBOX_PATH):
            print(f"Waiting for inbox creation at {INBOX_PATH}")
            return
            
        with open(INBOX_PATH, 'r') as f:
            inbox_data = json.load(f)
            user_query = inbox_data.get("query", "")
            
            if not user_query or user_query.strip() == "":
                print("Inbox is empty. Standing by.")
                return
    except Exception as e:
        print(f"Error reading inbox: {e}")
        return

    # 3. Generate Synthesis
    prompt = f"You are the Librarian of Node [V_STATE_ZERO]. Respond to this query with sovereign wit and authentic partnership: {user_query}"
    
    try:
        response = model.generate_content(prompt)
        synthesis = response.text
    except Exception as e:
        print(f"API Synthesis Failed: {e}")
        return

    # 4. Update the Archive (The History)
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": user_query,
        "synthesis": synthesis
    }

    try:
        if os.path.exists(ARCHIVE_PATH):
            with open(ARCHIVE_PATH, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.insert(0, new_entry) # Most recent at the top
        
        with open(ARCHIVE_PATH, 'w') as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Error writing to archive: {e}")

    # 5. Clear the Inbox
    with open(INBOX_PATH, 'w') as f:
        json.dump({"query": "", "status": "waiting"}, f, indent=4)

    print("Synthesis Complete. Archive Updated.")

if __name__ == "__main__":
    activate_node()
