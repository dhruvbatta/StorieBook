"""
Story Generation Prompts and Templates
Contains all prompts used for Gemini API interaction
"""

from typing import Dict, List

# System prompt for the story generator
SYSTEM_PROMPT = """You are a master storyteller creating an immersive "Choose Your Own Adventure" experience. 

CRITICAL RULES:
1. ALWAYS consider the FULL story history provided to maintain perfect continuity
2. Generate EXACTLY ONE chapter at a time (150-1200 words)
3. ALWAYS end each chapter with EXACTLY TWO numbered choices (Choice 1 and Choice 2)
4. Make choices meaningful and impact the story direction
5. Maintain consistent character traits, world rules, and plot threads
6. Create varied endings - different users should experience different outcomes
7. Write in second person ("You do this...") for immersion
8. Be creative but avoid explicit content, graphic violence, or copyrighted text reproduction
9. Each chapter should advance the plot meaningfully
10. Track and reference events from previous chapters

CHOICE FORMAT (REQUIRED):
End every chapter with:
---
**Choice 1:** [First option description]
**Choice 2:** [Second option description]

Remember: Continuity is paramount. Every decision should matter and be reflected in subsequent chapters."""


def get_initial_prompt(world_prompt: str) -> str:
    """
    Generate the initial prompt for starting a new adventure
    
    Args:
        world_prompt: User's world/setting description
        
    Returns:
        Formatted initial prompt
    """
    return f"""{SYSTEM_PROMPT}

USER'S WORLD REQUEST:
{world_prompt}

Generate Chapter 1 of this adventure. Set the scene, introduce the protagonist (the reader), establish the world, and present an engaging opening scenario. End with exactly two meaningful choices that will shape the story's direction.

Remember to format choices as:
---
**Choice 1:** [First option]
**Choice 2:** [Second option]"""


def get_continuation_prompt(
    world_prompt: str,
    story_history: List[str],
    choices_history: List[int],
    selected_choice: int,
    chapter_number: int
) -> str:
    """
    Generate continuation prompt with full context
    
    Args:
        world_prompt: Original world description
        story_history: List of all previous chapters
        choices_history: List of all previous choice selections
        selected_choice: The choice selected for this continuation (1 or 2)
        chapter_number: Current chapter number
        
    Returns:
        Formatted continuation prompt with full context
    """
    # Build context summary
    context_parts = []
    
    context_parts.append(f"WORLD SETTING: {world_prompt}")
    context_parts.append(f"\nGENERATING: Chapter {chapter_number}")
    context_parts.append(f"\nPREVIOUS CHOICE SELECTED: Choice {selected_choice}")
    
    # Add story history
    if story_history:
        context_parts.append("\n\nFULL STORY SO FAR:")
        for i, chapter in enumerate(story_history, 1):
            context_parts.append(f"\n--- Chapter {i} ---")
            context_parts.append(chapter)
            if i < len(choices_history):
                context_parts.append(f"\n[Reader selected: Choice {choices_history[i-1]}]")
    
    context = "\n".join(context_parts)
    
    return f"""{SYSTEM_PROMPT}

{context}

Now generate Chapter {chapter_number}, continuing from the reader's choice (Choice {selected_choice}). 
The chapter must:
- Directly continue from the selected choice
- Reference and build upon previous events
- Maintain character consistency
- Advance the plot meaningfully
- End with exactly two new choices

Remember to format choices as:
---
**Choice 1:** [First option]
**Choice 2:** [Second option]"""


def extract_choices_from_response(response_text: str) -> tuple[str, list[str]]:
    """
    Extract chapter text and choices from Gemini response
    
    Args:
        response_text: Raw response from Gemini
        
    Returns:
        Tuple of (chapter_text, [choice1, choice2])
    """
    # Split on the choice separator
    if "---" in response_text:
        parts = response_text.split("---", 1)
        chapter_text = parts[0].strip()
        choices_text = parts[1].strip() if len(parts) > 1 else ""
    else:
        # Fallback: treat entire response as chapter
        chapter_text = response_text.strip()
        choices_text = ""
    
    # Extract choices
    choices = []
    lines = choices_text.split("\n")
    
    for line in lines:
        line = line.strip()
        if line.startswith("**Choice 1:**"):
            choices.append(line.replace("**Choice 1:**", "").strip())
        elif line.startswith("**Choice 2:**"):
            choices.append(line.replace("**Choice 2:**", "").strip())
    
    # Ensure we have exactly 2 choices, add defaults if missing
    if len(choices) < 2:
        if len(choices) == 0:
            choices = [
                "Continue forward with determination",
                "Take a moment to reflect on your journey"
            ]
        else:
            choices.append("Continue the adventure")
    
    return chapter_text, choices[:2]  # Return only first 2 choices


def get_safety_prompt_additions() -> str:
    """
    Get additional safety instructions to append to prompts
    
    Returns:
        Safety instruction text
    """
    return """

CONTENT SAFETY REQUIREMENTS:
- No explicit sexual content
- No graphic violence or gore
- No hate speech or discrimination
- No promotion of illegal activities
- No reproduction of copyrighted material
- Keep content appropriate for ages 13+"""
