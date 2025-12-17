#!/usr/bin/env python3
"""Start backend server with proper environment loading."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
backend_dir = Path(__file__).parent
env_file = backend_dir / ".env"
load_dotenv(env_file)

print(f"Loading environment from: {env_file}")
print(f"GEMINI_API_KEY loaded: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"QDRANT_URL loaded: {'Yes' if os.getenv('QDRANT_URL') else 'No'}")
print("=" * 60)

# Add src to path
src_path = backend_dir / "src"
sys.path.insert(0, str(src_path))

print("Starting backend server on http://localhost:8000")
print("Press Ctrl+C to stop")
print("=" * 60)

try:
    import uvicorn
    from backend.main import app

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
