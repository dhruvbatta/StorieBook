# 🚀 StorieBook Setup Guide

This guide will walk you through setting up and running StorieBook on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
   - Check: `python3 --version` or `python --version`
   - Download from: https://www.python.org/downloads/

2. **pip** (Python package manager)
   - Usually comes with Python
   - Check: `pip --version` or `pip3 --version`

3. **Google Gemini API Key**
   - Get one free at: https://makersuite.google.com/app/apikey
   - You'll need a Google account

## 🎯 Quick Start (Recommended)

### Option 1: Using the Run Script (Easiest)

**macOS/Linux:**
```bash
cd /Users/dhruv-mac/Documents/StorieBook
./run.sh
```

**Windows:**
```cmd
cd C:\path\to\StorieBook
run.bat
```

The script will:
- Create a virtual environment
- Install all dependencies
- Check for your API key
- Launch the application

### Option 2: Manual Setup

#### Step 1: Navigate to Project Directory
```bash
cd /Users/dhruv-mac/Documents/StorieBook
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

Your API key is already configured in `.env`, but you can verify:
```bash
cat .env  # macOS/Linux
type .env # Windows
```

Should show:
```
GEMINI_API_KEY=AIzaSyCQCrwdbgiwjrwIxITBIlZySUzEATmOHW4
```

#### Step 5: Run the Application
```bash
streamlit run app.py
```

#### Step 6: Open in Browser

The app will automatically open, or navigate to:
```
http://localhost:8501
```

## 🎮 First Story

1. The app opens with a welcome screen
2. Enter a world prompt (or use the default)
3. Click "🚀 Start Adventure"
4. Read your first chapter
5. Choose between two options
6. Continue your unique adventure!

## 🔧 Troubleshooting

### "Module not found" errors

```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key not found" error

```bash
# Check .env file exists
ls -la .env  # macOS/Linux
dir .env     # Windows

# Verify contents
cat .env  # Should show your API key
```

### Port 8501 already in use

```bash
# Kill existing Streamlit process
pkill -f streamlit  # macOS/Linux

# Or use a different port
streamlit run app.py --server.port=8502
```

### "google.generativeai not found"

```bash
pip install google-generativeai --upgrade
```

## 🎨 Customization

### Change AI Parameters

Edit `utils/constants.py`:
```python
TEMPERATURE = 0.85  # Creativity (0.0-1.0)
MAX_TOKENS = 2048   # Chapter length
MAX_CHAPTERS = 50   # Story limit
```

### Change UI Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"  # Accent color
backgroundColor = "#FFFFFF"
```

### Modify System Prompt

Edit `story_engine/prompts.py`:
```python
SYSTEM_PROMPT = """Your custom instructions..."""
```

## 📊 Project Structure

```
StorieBook/
├── app.py                 # Main application
├── story_engine/          # Core logic
│   ├── generator.py       # AI integration
│   ├── prompts.py         # Prompt engineering
│   └── state.py           # State management
├── utils/                 # Utilities
│   ├── constants.py       # Configuration
│   └── logger.py          # Logging
├── requirements.txt       # Dependencies
├── .env                   # Your API key (DO NOT COMMIT)
└── README.md             # Documentation
```

## 🚀 Deployment

### Streamlit Cloud (Free)

1. Create GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. Visit https://share.streamlit.io

3. Click "New app"

4. Connect your repository

5. Add secrets (Settings → Secrets):
   ```toml
   GEMINI_API_KEY = "AIzaSyCQCrwdbgiwjrwIxITBIlZySUzEATmOHW4"
   ```

6. Deploy!

### Docker

```bash
# Build image
docker build -t storiebook .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=AIzaSyCQCrwdbgiwjrwIxITBIlZySUzEATmOHW4 \
  storiebook
```

## 💡 Tips for Best Stories

### World Prompts

**Good Examples:**
- "I'm a detective in Victorian London solving a mystery involving ancient magic"
- "I'm a chef in a world where cooking can create real magic effects"
- "I'm an astronaut who discovers a civilization living inside a black hole"

**Less Effective:**
- "Adventure" (too vague)
- "Story about magic" (no character/setting)

### During the Story

- **Be patient**: Generation takes 5-15 seconds
- **Make decisive choices**: Both paths are meaningful
- **Restart freely**: Each story is unique
- **Explore**: Try different prompts to see variety

## 🔐 Security Notes

⚠️ **IMPORTANT**: Never commit `.env` to version control!

The `.gitignore` file already excludes it, but verify:
```bash
git status  # .env should NOT appear
```

If deploying:
- Use environment variables or secrets management
- Rotate API keys if exposed
- Monitor usage at: https://console.cloud.google.com

## 📈 Monitoring

View logs:
```bash
# Set debug mode
export LOG_LEVEL=DEBUG

# Run with logs
streamlit run app.py 2>&1 | tee app.log
```

## 🆘 Getting Help

1. **Check logs**: Look for error messages in terminal
2. **Verify API key**: Test at https://makersuite.google.com
3. **Update dependencies**: `pip install -r requirements.txt --upgrade`
4. **Check Python version**: Must be 3.8+

## 🎉 You're Ready!

Run the application and start creating amazing adventures!

```bash
./run.sh        # macOS/Linux
# or
run.bat         # Windows
# or
streamlit run app.py
```

Happy storytelling! 📚✨
