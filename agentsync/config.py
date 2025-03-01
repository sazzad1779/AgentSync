import os
from dotenv import load_dotenv

# Dynamically get the root directory based on where the user runs the script
PROJECT_ROOT = os.getcwd()

# Define expected locations of .env and credentials
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
CRED_DIR = os.path.join(PROJECT_ROOT, "cred_files/")

# Load environment variables from .env if it exists
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    print(f"⚠️ Warning: No .env file found at {ENV_FILE}. Using system environment variables.")

# Access environment variables, default to empty strings if missing
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", os.path.join(CRED_DIR, "google_service_cred.json"))
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE", os.path.join(CRED_DIR, "client_secret.json"))
SHEET_ID = os.getenv("SHEET_ID", "")
GMAIL_USER_EMAIL = os.getenv("GMAIL_USER_EMAIL", "")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Validate credentials existence
if not GOOGLE_API_KEY:
    print("⚠️ Warning: GOOGLE_API_KEY is not set.")

if not OPENAI_API_KEY:
    print("⚠️ Warning: OPENAI_API_KEY is not set.")

if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
    print(f"⚠️ Warning: Google credentials file not found at {GOOGLE_CREDENTIALS_FILE}")

if not os.path.exists(CLIENT_SECRET_FILE):
    print(f"⚠️ Warning: Client secret file not found at {CLIENT_SECRET_FILE}")
