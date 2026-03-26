"""Main entry point for the backend application."""

import uvicorn
from src.backend.main import app


def main():
    """Main function to run the application."""
    print("Starting Educational AI Tutor with Authentication Service...")
    uvicorn.run(
        "src.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True
    )


if __name__ == "__main__":
    main()
