"""
State Management Module
Handles session state with abstraction for future database integration
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st

from utils.constants import SESSION_KEYS, DB_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)


class StateManager:
    """
    Manages application state with support for multiple backends
    Currently uses st.session_state but designed for easy migration to Firestore/Redis/Supabase
    """
    
    def __init__(self, backend: str = "session_state"):
        """
        Initialize state manager
        
        Args:
            backend: Storage backend (session_state, firestore, redis, supabase)
        """
        self.backend = backend
        self._validate_backend()
        
    def _validate_backend(self):
        """Validate that the selected backend is available"""
        if self.backend == "session_state":
            return  # Always available in Streamlit
        
        # Check if other backends are enabled in config
        if self.backend in DB_CONFIG and DB_CONFIG[self.backend].get("enabled", False):
            logger.info(f"Using {self.backend} backend for state management")
        else:
            logger.warning(f"Backend {self.backend} not enabled, falling back to session_state")
            self.backend = "session_state"
    
    def initialize_state(self) -> None:
        """Initialize session state with default values"""
        if not self.get(SESSION_KEYS["initialized"], False):
            logger.info("Initializing new session state")
            
            self.set(SESSION_KEYS["story_history"], [])
            self.set(SESSION_KEYS["choices_history"], [])
            self.set(SESSION_KEYS["current_chapter_number"], 0)
            self.set(SESSION_KEYS["story_id"], self._generate_story_id())
            self.set(SESSION_KEYS["world_prompt"], "")
            self.set(SESSION_KEYS["current_chapter"], "")
            self.set(SESSION_KEYS["current_choices"], [])
            self.set(SESSION_KEYS["loading"], False)
            self.set(SESSION_KEYS["initialized"], True)
            
            logger.info(f"Session initialized with story_id: {self.get(SESSION_KEYS['story_id'])}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from state
        
        Args:
            key: State key
            default: Default value if key doesn't exist
            
        Returns:
            Value from state or default
        """
        if self.backend == "session_state":
            return st.session_state.get(key, default)
        # Add other backend implementations here
        # elif self.backend == "firestore":
        #     return self._get_from_firestore(key, default)
        else:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in state
        
        Args:
            key: State key
            value: Value to set
        """
        if self.backend == "session_state":
            st.session_state[key] = value
        # Add other backend implementations here
        # elif self.backend == "firestore":
        #     self._set_in_firestore(key, value)
    
    def reset_state(self) -> None:
        """Reset all state to initial values"""
        logger.info("Resetting session state")
        
        self.set(SESSION_KEYS["story_history"], [])
        self.set(SESSION_KEYS["choices_history"], [])
        self.set(SESSION_KEYS["current_chapter_number"], 0)
        self.set(SESSION_KEYS["story_id"], self._generate_story_id())
        self.set(SESSION_KEYS["world_prompt"], "")
        self.set(SESSION_KEYS["current_chapter"], "")
        self.set(SESSION_KEYS["current_choices"], [])
        self.set(SESSION_KEYS["loading"], False)
        
        logger.info(f"Session reset with new story_id: {self.get(SESSION_KEYS['story_id'])}")
    
    def add_chapter(self, chapter_text: str, choices: List[str]) -> None:
        """
        Add a new chapter to the story history
        
        Args:
            chapter_text: The chapter content
            choices: List of choices for this chapter
        """
        story_history = self.get(SESSION_KEYS["story_history"], [])
        story_history.append(chapter_text)
        self.set(SESSION_KEYS["story_history"], story_history)
        
        chapter_num = self.get(SESSION_KEYS["current_chapter_number"], 0) + 1
        self.set(SESSION_KEYS["current_chapter_number"], chapter_num)
        self.set(SESSION_KEYS["current_chapter"], chapter_text)
        self.set(SESSION_KEYS["current_choices"], choices)
        
        logger.info(f"Added chapter {chapter_num} to story {self.get(SESSION_KEYS['story_id'])}")
    
    def add_choice(self, choice: int) -> None:
        """
        Record a user's choice
        
        Args:
            choice: The choice number (1 or 2)
        """
        choices_history = self.get(SESSION_KEYS["choices_history"], [])
        choices_history.append(choice)
        self.set(SESSION_KEYS["choices_history"], choices_history)
        
        logger.info(f"User selected choice {choice} for chapter {len(choices_history)}")
    
    def get_story_context(self) -> Dict[str, Any]:
        """
        Get complete story context for generation
        
        Returns:
            Dictionary containing all story context
        """
        return {
            "story_id": self.get(SESSION_KEYS["story_id"], ""),
            "world_prompt": self.get(SESSION_KEYS["world_prompt"], ""),
            "story_history": self.get(SESSION_KEYS["story_history"], []),
            "choices_history": self.get(SESSION_KEYS["choices_history"], []),
            "current_chapter_number": self.get(SESSION_KEYS["current_chapter_number"], 0),
            "current_chapter": self.get(SESSION_KEYS["current_chapter"], ""),
            "current_choices": self.get(SESSION_KEYS["current_choices"], [])
        }
    
    def is_story_active(self) -> bool:
        """Check if a story is currently active"""
        return self.get(SESSION_KEYS["current_chapter_number"], 0) > 0
    
    def _generate_story_id(self) -> str:
        """
        Generate a unique story ID
        
        Returns:
            Unique story identifier
        """
        return f"story_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
    
    # Future database implementation methods (stubs for now)
    
    def save_to_database(self) -> bool:
        """
        Save current state to database (for future implementation)
        
        Returns:
            True if successful
        """
        if self.backend == "session_state":
            return True  # Already persisted in session
        
        # TODO: Implement Firestore/Redis/Supabase persistence
        logger.warning(f"Database persistence not implemented for {self.backend}")
        return False
    
    def load_from_database(self, story_id: str) -> bool:
        """
        Load state from database (for future implementation)
        
        Args:
            story_id: Story ID to load
            
        Returns:
            True if successful
        """
        if self.backend == "session_state":
            return False  # Cannot load from session storage
        
        # TODO: Implement Firestore/Redis/Supabase loading
        logger.warning(f"Database loading not implemented for {self.backend}")
        return False


# Singleton instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """
    Get the singleton state manager instance
    
    Returns:
        StateManager instance
    """
    global _state_manager
    if _state_manager is None:
        backend = DB_CONFIG.get("type", "session_state")
        _state_manager = StateManager(backend=backend)
    return _state_manager
