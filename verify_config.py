# verify_config.py
import agentsync.config as config
import os
import json
    # Load JSON files if the filenames are provided
def load_json_file(file_path):
    """Helper function to load a JSON file safely."""
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None  # Return None if file is missing

def main():
    
    print(f"GOOGLE_API_KEY: {config.GOOGLE_API_KEY}")
    print(f"GOOGLE_CREDENTIALS_FILE: {config.GOOGLE_CREDENTIALS_FILE}")
    GOOGLE_CREDENTIALS = load_json_file(config.GOOGLE_CREDENTIALS_FILE)
    print(json.dumps(GOOGLE_CREDENTIALS, indent=4),"\n\n")  

    print(f"CLIENT_SECRET_FILE: {config.CLIENT_SECRET_FILE}")
    CLIENT_SECRET = load_json_file(config.CLIENT_SECRET_FILE)
    print(json.dumps(CLIENT_SECRET, indent=4),"\n\n") 


    print(f"SHEET_ID: {config.SHEET_ID}")
    print(f"GMAIL_USER_EMAIL: {config.GMAIL_USER_EMAIL}")
    print(f"HUNTER_API_KEY: {config.HUNTER_API_KEY}")
    print(f"CHECK_INTERVAL: {config.CHECK_INTERVAL}")
if __name__ == "__main__":
    main()
