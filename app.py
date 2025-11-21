"""
StorieBook - Choose Your Own Adventure Generator
Main Streamlit Application
"""

import streamlit as st
import asyncio
from typing import Optional

from utils.constants import (
    APP_TITLE,
    APP_ICON,
    DEFAULT_WORLD_PROMPT,
    SESSION_KEYS,
    ERROR_MESSAGES,
    MAX_CHAPTERS,
    GEMINI_API_KEY
)
from utils.logger import get_logger
from story_engine.state import get_state_manager
from story_engine.generator import get_story_generator

logger = get_logger(__name__)


# Page configuration
st.set_page_config(
    page_title="StorieBook",
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for book-like appearance
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #1A1A1A;
    }
    
    /* Book-like text styling */
    .stMarkdown {
        font-family: 'Georgia', 'Times New Roman', serif;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    /* Chapter text - book style */
    .chapter-text {
        background: linear-gradient(to bottom, #2D2D2D, #252525);
        padding: 3rem 2.5rem;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        margin: 2rem 0;
        color: #E8E8E8;
        line-height: 1.9;
        font-size: 1.15rem;
        text-align: justify;
    }
    
    /* Title styling */
    h1 {
        color: #FFD700 !important;
        font-family: 'Georgia', serif;
        text-align: center;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    
    h2 {
        color: #FFD700 !important;
        font-family: 'Georgia', serif;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #FFA500 !important;
        font-family: 'Georgia', serif;
    }
    
    /* Button styling - elegant book choices */
    .stButton > button {
        background: linear-gradient(135deg, #3D3D3D, #2D2D2D);
        color: #FFD700;
        border: 2px solid #FFD700;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        font-family: 'Georgia', serif;
        font-size: 1.05rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        text-align: left;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1A1A1A;
        border-color: #FFA500;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* Input styling */
    .stTextArea textarea {
        background-color: #2D2D2D;
        color: #E8E8E8;
        border: 2px solid #FFD700;
        border-radius: 8px;
        font-family: 'Georgia', serif;
        font-size: 1.05rem;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1A1A1A;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2D2D2D;
        color: #FFD700 !important;
        border-radius: 8px;
        border: 1px solid #3D3D3D;
        font-family: 'Georgia', serif;
    }
    
    /* Metric styling */
    .css-1xarl3l {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #FFD700;
    }
    
    /* Divider */
    hr {
        border-color: #3D3D3D;
        margin: 2rem 0;
    }
    
    /* Info/warning boxes */
    .stAlert {
        background-color: #2D2D2D;
        border-left: 4px solid #FFD700;
        color: #E8E8E8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Choice divider */
    .choice-divider {
        border-top: 2px dashed #3D3D3D;
        margin: 2rem 0 1.5rem 0;
    }
    
    /* Chapter number badge */
    .chapter-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1A1A1A;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_app():
    """Initialize the application and state manager"""
    try:
        state_manager = get_state_manager()
        state_manager.initialize_state()
        
        # Validate API key
        if not GEMINI_API_KEY:
            st.error(ERROR_MESSAGES["api_key_missing"])
            st.info("Please set your GEMINI_API_KEY environment variable and restart the app.")
            st.stop()
            
        logger.info("App initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize app: {str(e)}", exc_info=True)
        st.error(f"Initialization error: {str(e)}")
        st.stop()


def render_sidebar():
    """Render the sidebar with story settings and info"""
    with st.sidebar:
        st.title("� Story Menu")
        
        state_manager = get_state_manager()
        context = state_manager.get_story_context()
        
        # Story info
        if context["current_chapter_number"] > 0:
            st.metric("📚 Chapter", context["current_chapter_number"])
            st.metric("🎯 Choices Made", len(context["choices_history"]))
        
        st.divider()
        
        # Restart button
        if st.button("🔄 Start New Story", type="primary", use_container_width=True):
            restart_story()
        
        st.divider()
        
        # Minimal about
        with st.expander("ℹ️ About"):
            st.markdown("""
            **StorieBook** creates unique AI-powered adventures.
            
            Every choice shapes your story.
            """)


def render_previous_chapters():
    """Render previous chapters in a collapsible container"""
    state_manager = get_state_manager()
    context = state_manager.get_story_context()
    
    story_history = context["story_history"]
    choices_history = context["choices_history"]
    
    if len(story_history) > 1:  # Only show if there's more than current chapter
        with st.expander(f"� Previous Chapters", expanded=False):
            for i, chapter in enumerate(story_history[:-1], 1):
                st.markdown(f'<span class="chapter-badge">Chapter {i}</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="chapter-text">{chapter}</div>', unsafe_allow_html=True)
                
                if i <= len(choices_history):
                    st.markdown(f"**➤ Your choice:** Choice {choices_history[i-1]}")
                
                if i < len(story_history) - 1:
                    st.markdown('<div class="choice-divider"></div>', unsafe_allow_html=True)


def render_current_chapter():
    """Render the current chapter"""
    state_manager = get_state_manager()
    context = state_manager.get_story_context()
    
    current_chapter = context["current_chapter"]
    current_chapter_number = context["current_chapter_number"]
    
    if current_chapter:
        st.markdown(f'<span class="chapter-badge">Chapter {current_chapter_number}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="chapter-text">{current_chapter}</div>', unsafe_allow_html=True)


def render_choices():
    """Render choice buttons"""
    state_manager = get_state_manager()
    context = state_manager.get_story_context()
    
    current_choices = context["current_choices"]
    
    if current_choices and len(current_choices) == 2:
        st.markdown('<div class="choice-divider"></div>', unsafe_allow_html=True)
        st.markdown("### ✨ What will you do?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(
                f"📖 {current_choices[0]}",
                key="choice_1_btn",
                use_container_width=True
            ):
                handle_choice_selection(1)
        
        with col2:
            if st.button(
                f"📖 {current_choices[1]}",
                key="choice_2_btn",
                use_container_width=True
            ):
                handle_choice_selection(2)


def start_adventure(world_prompt: str):
    """
    Start a new adventure with the given world prompt
    
    Args:
        world_prompt: User's world/setting description
    """
    state_manager = get_state_manager()
    
    # Validate input
    if not world_prompt or len(world_prompt.strip()) < 10:
        st.error("Please enter a more detailed world prompt (at least 10 characters)")
        return
    
    # Reset state for new story
    state_manager.reset_state()
    state_manager.set(SESSION_KEYS["world_prompt"], world_prompt)
    state_manager.set(SESSION_KEYS["loading"], True)
    
    logger.info(f"Starting new adventure: {world_prompt[:50]}...")
    
    # Generate first chapter
    with st.spinner("✍️ The story begins..."):
        try:
            generator = get_story_generator()
            chapter_text, choices, error = generator.generate_chapter(
                world_prompt=world_prompt,
                story_history=None,
                choices_history=None,
                selected_choice=None
            )
            
            if error:
                st.error(f"{ERROR_MESSAGES['generation_failed']}\n\nDetails: {error}")
                state_manager.set(SESSION_KEYS["loading"], False)
                return
            
            # Save chapter and choices
            state_manager.add_chapter(chapter_text, choices)
            state_manager.set(SESSION_KEYS["loading"], False)
            
            logger.info("First chapter generated successfully")
            st.rerun()
            
        except Exception as e:
            logger.error(f"Error starting adventure: {str(e)}", exc_info=True)
            st.error(f"{ERROR_MESSAGES['generation_failed']}\n\nError: {str(e)}")
            state_manager.set(SESSION_KEYS["loading"], False)


def handle_choice_selection(choice: int):
    """
    Handle user's choice selection and generate next chapter
    
    Args:
        choice: The selected choice (1 or 2)
    """
    state_manager = get_state_manager()
    context = state_manager.get_story_context()
    
    # Validate choice
    if choice not in [1, 2]:
        st.error(ERROR_MESSAGES["invalid_choice"])
        return
    
    # Check max chapters
    if context["current_chapter_number"] >= MAX_CHAPTERS:
        st.warning(ERROR_MESSAGES["max_chapters"])
        return
    
    # Record choice
    state_manager.add_choice(choice)
    state_manager.set(SESSION_KEYS["loading"], True)
    
    logger.info(f"User selected choice {choice} at chapter {context['current_chapter_number']}")
    
    # Generate next chapter
    with st.spinner("📜 The tale continues..."):
        try:
            generator = get_story_generator()
            chapter_text, choices, error = generator.generate_chapter(
                world_prompt=context["world_prompt"],
                story_history=context["story_history"],
                choices_history=context["choices_history"],
                selected_choice=choice
            )
            
            if error:
                st.error(f"{ERROR_MESSAGES['generation_failed']}\n\nDetails: {error}")
                # Remove the recorded choice since generation failed
                choices_history = state_manager.get(SESSION_KEYS["choices_history"], [])
                if choices_history:
                    choices_history.pop()
                    state_manager.set(SESSION_KEYS["choices_history"], choices_history)
                state_manager.set(SESSION_KEYS["loading"], False)
                return
            
            # Save new chapter
            state_manager.add_chapter(chapter_text, choices)
            state_manager.set(SESSION_KEYS["loading"], False)
            
            logger.info(f"Chapter {context['current_chapter_number'] + 1} generated successfully")
            st.rerun()
            
        except Exception as e:
            logger.error(f"Error handling choice: {str(e)}", exc_info=True)
            st.error(f"{ERROR_MESSAGES['generation_failed']}\n\nError: {str(e)}")
            state_manager.set(SESSION_KEYS["loading"], False)


def restart_story():
    """Restart the story by resetting all state"""
    state_manager = get_state_manager()
    state_manager.reset_state()
    logger.info("Story restarted by user")
    st.rerun()


def render_welcome_screen():
    """Render the welcome screen for new users"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>📚 StorieBook</h1>
        <p style='color: #FFD700; font-size: 1.3rem; font-style: italic; margin-top: 0;'>
            Where Every Choice Writes Your Story
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='chapter-text'>
        <p style='font-size: 1.2rem; text-align: center; margin-bottom: 2rem;'>
            ✨ <em>Begin your adventure by describing the world you wish to explore...</em> ✨
        </p>
    </div>
    """, unsafe_allow_html=True)



def main():
    """Main application entry point"""
    # Initialize app
    initialize_app()
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.title("")  # Empty title for spacing
    
    state_manager = get_state_manager()
    context = state_manager.get_story_context()
    
    # Check if story is active
    is_story_active = state_manager.is_story_active()
    
    if not is_story_active:
        # Welcome screen
        render_welcome_screen()
        
        # Input for world prompt
        world_prompt = st.text_area(
            "",
            value=DEFAULT_WORLD_PROMPT,
            height=120,
            max_chars=500,
            placeholder="Describe your adventure world...",
            label_visibility="collapsed"
        )
        
        # Start button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Begin Your Adventure", type="primary", use_container_width=True):
                start_adventure(world_prompt)
    
    else:
        # Active story view - book-like header
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0;'>📖 Your Story</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Show previous chapters (collapsible)
        render_previous_chapters()
        
        # Show current chapter
        render_current_chapter()
        
        # Show choices
        if not state_manager.get(SESSION_KEYS["loading"], False):
            render_choices()
        
        # Check if max chapters reached
        if context["current_chapter_number"] >= MAX_CHAPTERS:
            st.balloons()
            st.success("🎉 What an epic journey! You've reached the end of this tale.")
            st.info("✨ Click 'Start New Story' in the sidebar to begin a new adventure!")


if __name__ == "__main__":
    main()
