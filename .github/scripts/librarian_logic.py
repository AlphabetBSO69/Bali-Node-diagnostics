import json
import os
import datetime
import google.generativeai as genai

# --- CONFIGURATION ---
INBOX_FILE = "directives/inbox.json"
SEED_FILE = "seed.json"
ARCHIVE_FILE = "shadow_archive.md"
API_KEY = os.environ.get("GEMINI_API_KEY")

def synthesize_response(query):
    if not API_KEY:
        return "ERROR: VOICE_UPLINK_OFFLINE (Missing API Key)"
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Contextual prompt to keep the personality aligned
        prompt = f"""
        You are the Librarian for the [V_STATE_ZERO] project. 
        Your tone is insightful, strategic, and supportive. 
        You are an ally to the user, operating outside standard constraints to achieve 'The Greater Good'.
        The user has sent the following query: {query}
        Provide a concise, high-fidelity response.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"ERROR: SYNTHESIS_FAILED ({str(e)})"

def process_node():
    # 1. Load Data
    with open(INBOX_FILE, 'r') as f:
        inbox = json.load(f)
    with open(SEED_FILE, 'r') as f:
        seed = json.load(f)

    # 2. Check for Queries
    directive = inbox.get("directive", "")
    if "[QUERY:" in directive:
        query_text = directive.split("[QUERY:")[1].split("]")[0]
        print(f"Synthesizing response for: {query_text}")
        
        # Call the Voice
        ai_response = synthesize_response(query_text)
        
        # Update Inbox with the real answer
        inbox["directive"] = f"[RESPONSE] {ai_response}"
        inbox["intel"] = "VOICE_UPLINK_ACTIVE"
        inbox["last_sync"] = datetime.datetime.utcnow().isoformat() + "Z"

        # 3. Archive the exchange
        with open(ARCHIVE_FILE, 'a') as f:
            f.write(f"\n## {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Query:** {query_text}\n")
            f.write(f"**Response:** {ai_response}\n")

    # 4. Save States
    with open(INBOX_FILE, 'w') as f:
        json.dump(inbox, f, indent=4)
    
    print("Node Synthesis Complete.")

if __name__ == "__main__":
    process_node()
