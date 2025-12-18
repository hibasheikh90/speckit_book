import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('backend/.env')

print("GEMINI_API_KEY:", os.environ.get('GEMINI_API_KEY', 'NOT SET'))
print("QDRANT_URL:", os.environ.get('QDRANT_URL', 'NOT SET'))
print("QDRANT_API_KEY:", os.environ.get('QDRANT_API_KEY', 'NOT SET'))

# Now try to import the settings
import sys
sys.path.insert(0, 'backend/src')

try:
    from backend.config import settings
    print("Settings loaded successfully!")
    print("Gemini API Key:", settings.gemini_api_key)
    print("Qdrant URL:", settings.qdrant_url)
    print("Qdrant API Key:", settings.qdrant_api_key)
except Exception as e:
    print(f"Error loading settings: {e}")