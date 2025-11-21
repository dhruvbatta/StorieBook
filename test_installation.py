"""
Quick Test Script for StorieBook
Validates the installation and configuration
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("  ✅ streamlit")
    except ImportError as e:
        print(f"  ❌ streamlit: {e}")
        return False
    
    try:
        import google.generativeai
        print("  ✅ google.generativeai")
    except ImportError as e:
        print(f"  ❌ google.generativeai: {e}")
        return False
    
    try:
        from utils.constants import GEMINI_API_KEY
        print("  ✅ utils.constants")
    except ImportError as e:
        print(f"  ❌ utils.constants: {e}")
        return False
    
    try:
        from utils.logger import get_logger
        print("  ✅ utils.logger")
    except ImportError as e:
        print(f"  ❌ utils.logger: {e}")
        return False
    
    try:
        from story_engine.state import get_state_manager
        print("  ✅ story_engine.state")
    except ImportError as e:
        print(f"  ❌ story_engine.state: {e}")
        return False
    
    try:
        from story_engine.prompts import get_initial_prompt
        print("  ✅ story_engine.prompts")
    except ImportError as e:
        print(f"  ❌ story_engine.prompts: {e}")
        return False
    
    try:
        from story_engine.generator import get_story_generator
        print("  ✅ story_engine.generator")
    except ImportError as e:
        print(f"  ❌ story_engine.generator: {e}")
        return False
    
    return True


def test_api_key():
    """Test if API key is configured"""
    print("\n🔑 Testing API key configuration...")
    
    from utils.constants import GEMINI_API_KEY
    
    if not GEMINI_API_KEY:
        print("  ❌ GEMINI_API_KEY not found in environment")
        return False
    
    if GEMINI_API_KEY == "your_gemini_api_key_here":
        print("  ❌ GEMINI_API_KEY not configured (still using placeholder)")
        return False
    
    if len(GEMINI_API_KEY) < 20:
        print("  ⚠️  GEMINI_API_KEY seems too short")
        return False
    
    print(f"  ✅ API key found ({len(GEMINI_API_KEY)} characters)")
    return True


def test_generator_initialization():
    """Test if the generator can be initialized"""
    print("\n🤖 Testing Gemini generator initialization...")
    
    try:
        from story_engine.generator import get_story_generator
        generator = get_story_generator()
        print("  ✅ Generator initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ Generator initialization failed: {e}")
        return False


def test_prompt_generation():
    """Test if prompts can be generated"""
    print("\n📝 Testing prompt generation...")
    
    try:
        from story_engine.prompts import get_initial_prompt, get_continuation_prompt
        
        initial = get_initial_prompt("Test world")
        if initial and len(initial) > 0:
            print("  ✅ Initial prompt generated")
        else:
            print("  ❌ Initial prompt empty")
            return False
        
        continuation = get_continuation_prompt(
            "Test world",
            ["Chapter 1 text"],
            [1],
            1,
            2
        )
        if continuation and len(continuation) > 0:
            print("  ✅ Continuation prompt generated")
        else:
            print("  ❌ Continuation prompt empty")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Prompt generation failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("📚 StorieBook Installation Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("API Key", test_api_key()))
    results.append(("Generator", test_generator_initialization()))
    results.append(("Prompts", test_prompt_generation()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your installation is ready.")
        print("\nTo start the app, run:")
        print("  streamlit run app.py")
        print("\nor use the quick start script:")
        print("  ./run.sh  (macOS/Linux)")
        print("  run.bat   (Windows)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("  2. Check your .env file has GEMINI_API_KEY set")
        print("  3. Verify your Python version is 3.8+")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
