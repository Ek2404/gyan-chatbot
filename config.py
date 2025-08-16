import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecret")
    DEBUG = os.getenv("FLASK_ENV") == "development"
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 5000))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.OPENROUTER_API_KEY:
            print("⚠️  Warning: OPENROUTER_API_KEY not set. AI responses will not work.")
            print("   Please set OPENROUTER_API_KEY environment variable.")
        return True
