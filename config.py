"""
Configuration management for Dukan
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    # Claude API
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dukan.db")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ["TELEGRAM_BOT_TOKEN", "CLAUDE_API_KEY"]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate on import
Config.validate()
