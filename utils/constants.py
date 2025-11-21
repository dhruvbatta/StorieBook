"""
Application Constants and Configuration
"""

import os
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GEMINI_MODEL: Final[str] = "gemini-2.0-flash"
GEMINI_API_KEY: Final[str] = os.getenv("GEMINI_API_KEY", "")



# Generation Parameters
MAX_TOKENS: Final[int] = 2048
TEMPERATURE: Final[float] = 0.85
TOP_P: Final[float] = 0.95
TOP_K: Final[int] = 40

# Safety Settings
BLOCK_THRESHOLD: Final[str] = "BLOCK_MEDIUM_AND_ABOVE"

# Application Settings
APP_TITLE: Final[str] = "📚 StorieBook - Choose Your Own Adventure"
APP_ICON: Final[str] = "📖"
MAX_CHAPTERS: Final[int] = 50  # Prevent infinite stories
MIN_CHAPTER_LENGTH: Final[int] = 100  # Minimum characters per chapter
MAX_CHAPTER_LENGTH: Final[int] = 1500  # Maximum characters per chapter

# UI Configuration
SIDEBAR_TITLE: Final[str] = "Story Settings"
DEFAULT_WORLD_PROMPT: Final[str] = "I am a wizard in a world where magic and medieval knights coexist, embarking on a quest to find an ancient artifact."

# Session State Keys
SESSION_KEYS: Final[dict] = {
    "story_history": "story_history",
    "choices_history": "choices_history",
    "current_chapter_number": "current_chapter_number",
    "story_id": "story_id",
    "world_prompt": "world_prompt",
    "initialized": "initialized",
    "current_chapter": "current_chapter",
    "current_choices": "current_choices",
    "loading": "loading"
}

# Error Messages
ERROR_MESSAGES: Final[dict] = {
    "api_key_missing": "⚠️ GEMINI_API_KEY not found. Please set it in your environment variables.",
    "generation_failed": "❌ Failed to generate chapter. Please try again.",
    "invalid_choice": "⚠️ Invalid choice selected.",
    "max_chapters": f"🎉 You've reached the maximum of {MAX_CHAPTERS} chapters! What an adventure!",
    "content_blocked": "⚠️ Content was blocked by safety filters. Please try a different prompt.",
    "network_error": "🌐 Network error. Please check your connection and try again."
}

# Database Configuration (for future scaling)
DB_CONFIG: Final[dict] = {
    "type": "session_state",  # Options: session_state, firestore, redis, supabase
    "firestore": {
        "collection": "stories",
        "enabled": False
    },
    "redis": {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "enabled": False
    },
    "supabase": {
        "url": os.getenv("SUPABASE_URL", ""),
        "key": os.getenv("SUPABASE_KEY", ""),
        "enabled": False
    }
}

# Logging Configuration
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
