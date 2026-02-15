from dotenv import load_dotenv
import os

load_dotenv()  # MUST be first

# Get API key from .env
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception("❌ GOOGLE_API_KEY not found! Check your .env file.")

print("API Key Loaded Successfully:", API_KEY)
