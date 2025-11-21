# 🚀 StorieBook Quick Reference

## Start the Application

### Simplest Method
```bash
./run.sh
```
Then open: http://localhost:8501

### Alternative Methods
```bash
# Method 1: Direct Streamlit
streamlit run app.py

# Method 2: With virtual environment
source venv/bin/activate
streamlit run app.py

# Method 3: Different port
streamlit run app.py --server.port=8502

# Method 4: Docker
docker-compose up
```

## Stop the Application
Press `Ctrl+C` in the terminal

## File Locations

| What | Where |
|------|-------|
| Main app | `app.py` |
| Configuration | `utils/constants.py` |
| API Key | `.env` |
| Prompts | `story_engine/prompts.py` |
| State logic | `story_engine/state.py` |
| AI integration | `story_engine/generator.py` |
| Theme | `.streamlit/config.toml` |

## Environment Variables

```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Common Tasks

### Change AI Temperature (Creativity)
Edit `utils/constants.py`:
```python
TEMPERATURE = 0.85  # 0.0 = deterministic, 1.0 = creative
```

### Change Max Chapters
Edit `utils/constants.py`:
```python
MAX_CHAPTERS = 50  # Change to desired limit
```

### Change UI Theme Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"     # Buttons, accents
backgroundColor = "#FFFFFF"   # Main background
```

### View Logs
```bash
# Set debug mode
export LOG_LEVEL=DEBUG

# Run with logging
streamlit run app.py 2>&1 | tee app.log
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8501 in use | Use different port: `streamlit run app.py --server.port=8502` |
| API key error | Check `.env` file exists and has valid key |
| Module not found | Run `pip install -r requirements.txt` |
| Virtual env issues | Delete `venv/` and run `./run.sh` again |

## Example Story Prompts

```
✨ Fantasy:
"I'm a dragon rider in a world where dragons are going extinct"

🔮 Sci-Fi:
"I'm a time detective solving crimes across different eras"

🎭 Mystery:
"I'm a ghost who can't remember how they died"

🏰 Historical:
"I'm a samurai in feudal Japan who discovers magic is real"

🌟 Adventure:
"I'm a chef whose food can grant magical abilities"
```

## Keyboard Shortcuts (in app)

- `r` - Rerun the app
- `c` - Clear cache
- `?` - Show keyboard shortcuts

## API Usage

Your API key has quotas. Monitor at:
https://console.cloud.google.com

## Quick Commands

```bash
# Test installation
python test_installation.py

# Update dependencies
pip install -r requirements.txt --upgrade

# Check Python version
python --version

# Check Streamlit version
streamlit --version

# Open in browser manually
open http://localhost:8501  # macOS
```

## Production Deployment

### Streamlit Cloud (Free)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repository
4. Add secret: `GEMINI_API_KEY`
5. Deploy!

### Docker
```bash
docker build -t storiebook .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key storiebook
```

## Files You Can Modify Safely

✅ Safe to edit:
- `utils/constants.py` - Settings
- `story_engine/prompts.py` - Story prompts
- `.streamlit/config.toml` - UI theme
- `.env` - Environment variables

⚠️ Advanced (edit carefully):
- `story_engine/generator.py` - AI logic
- `story_engine/state.py` - State management
- `app.py` - Main application

## Getting Help

1. Check logs in terminal
2. Run test: `python test_installation.py`
3. Verify API key: `cat .env`
4. Check errors in browser console (F12)

## Version Info

- Python: 3.11+
- Streamlit: 1.51.0
- Gemini API: 0.8.5
- Model: gemini-1.5-flash

---

**Questions?** Check README.md and SETUP.md for detailed docs!
