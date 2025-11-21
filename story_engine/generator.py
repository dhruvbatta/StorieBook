"""
Story Generator Module
Handles all Gemini API interactions for chapter generation
"""

import asyncio
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

from utils.constants import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    BLOCK_THRESHOLD,
    ERROR_MESSAGES
)
from utils.logger import get_logger
from story_engine.prompts import (
    get_initial_prompt,
    get_continuation_prompt,
    extract_choices_from_response
)

logger = get_logger(__name__)


class StoryGenerator:
    """
    Handles story generation using Google Gemini API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the story generator
        
        Args:
            api_key: Gemini API key (uses env var if not provided)
        """
        self.api_key = api_key or GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError(ERROR_MESSAGES["api_key_missing"])
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model with safety settings
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": BLOCK_THRESHOLD,
                "HARM_CATEGORY_HATE_SPEECH": BLOCK_THRESHOLD,
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": BLOCK_THRESHOLD,
                "HARM_CATEGORY_DANGEROUS_CONTENT": BLOCK_THRESHOLD
            }
        )
        
        logger.info(f"Initialized StoryGenerator with model: {GEMINI_MODEL}")
    
    async def generate_chapter_async(
        self,
        world_prompt: str,
        story_history: Optional[List[str]] = None,
        choices_history: Optional[List[int]] = None,
        selected_choice: Optional[int] = None
    ) -> Tuple[str, List[str], Optional[str]]:
        """
        Asynchronously generate a new chapter
        
        Args:
            world_prompt: Initial world/setting description
            story_history: List of previous chapters (None for first chapter)
            choices_history: List of previous choices (None for first chapter)
            selected_choice: The choice selected (None for first chapter)
            
        Returns:
            Tuple of (chapter_text, [choice1, choice2], error_message)
        """
        try:
            # Determine if this is the first chapter
            is_first_chapter = story_history is None or len(story_history) == 0
            
            # Build the prompt
            if is_first_chapter:
                prompt = get_initial_prompt(world_prompt)
                chapter_number = 1
                logger.info("Generating first chapter")
            else:
                chapter_number = len(story_history) + 1
                prompt = get_continuation_prompt(
                    world_prompt=world_prompt,
                    story_history=story_history,
                    choices_history=choices_history or [],
                    selected_choice=selected_choice or 1,
                    chapter_number=chapter_number
                )
                logger.info(f"Generating chapter {chapter_number} after choice {selected_choice}")
            
            # Generate content asynchronously
            response = await asyncio.to_thread(
                self._generate_content,
                prompt
            )
            
            if response is None:
                logger.error("Received None response from Gemini")
                return "", [], ERROR_MESSAGES["generation_failed"]
            
            # Extract chapter and choices
            chapter_text, choices = extract_choices_from_response(response)
            
            # Validate response
            if not chapter_text or len(chapter_text) < 50:
                logger.error(f"Generated chapter too short: {len(chapter_text)} chars")
                return "", [], ERROR_MESSAGES["generation_failed"]
            
            if len(choices) < 2:
                logger.warning(f"Only {len(choices)} choices extracted, using defaults")
            
            logger.info(f"Successfully generated chapter {chapter_number} ({len(chapter_text)} chars)")
            
            return chapter_text, choices, None
            
        except Exception as e:
            logger.error(f"Error generating chapter: {str(e)}", exc_info=True)
            return "", [], str(e)
    
    def generate_chapter(
        self,
        world_prompt: str,
        story_history: Optional[List[str]] = None,
        choices_history: Optional[List[int]] = None,
        selected_choice: Optional[int] = None
    ) -> Tuple[str, List[str], Optional[str]]:
        """
        Synchronous wrapper for generate_chapter_async
        
        Args:
            world_prompt: Initial world/setting description
            story_history: List of previous chapters (None for first chapter)
            choices_history: List of previous choices (None for first chapter)
            selected_choice: The choice selected (None for first chapter)
            
        Returns:
            Tuple of (chapter_text, [choice1, choice2], error_message)
        """
        try:
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.generate_chapter_async(
                    world_prompt,
                    story_history,
                    choices_history,
                    selected_choice
                )
            )
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in synchronous generation: {str(e)}", exc_info=True)
            return "", [], str(e)
    
    def _generate_content(self, prompt: str) -> Optional[str]:
        """
        Internal method to call Gemini API
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text or None if failed
        """
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "top_k": TOP_K,
                "max_output_tokens": MAX_TOKENS,
            }
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Check for safety blocks
            if hasattr(response, 'prompt_feedback'):
                if response.prompt_feedback.block_reason:
                    logger.warning(f"Content blocked: {response.prompt_feedback.block_reason}")
                    return None
            
            # Extract text
            if response.text:
                return response.text
            else:
                logger.error("No text in response")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
            raise


# Singleton instance
_generator: Optional[StoryGenerator] = None


def get_story_generator(api_key: Optional[str] = None) -> StoryGenerator:
    """
    Get the singleton story generator instance
    
    Args:
        api_key: Optional API key override
        
    Returns:
        StoryGenerator instance
    """
    global _generator
    if _generator is None or api_key is not None:
        _generator = StoryGenerator(api_key=api_key)
    return _generator
