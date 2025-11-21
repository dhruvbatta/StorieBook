# 📚 StorieBook - AI-Powered Choose Your Own Adventure

A scalable Streamlit application that generates dynamic "Choose Your Own Adventure" stories using Google Gemini Flash. Create unique, personalized narratives where every choice matters and shapes your journey.

## ✨ Features

- 🎭 **Dynamic Story Generation**: Powered by Google Gemini 1.5 Flash
- 🔄 **Full Narrative Continuity**: Each chapter builds on previous choices
- 🎯 **Meaningful Choices**: Two distinct paths at every decision point
- 🎨 **Clean, Intuitive UI**: Easy-to-use Streamlit interface
- 💾 **Persistent State**: Session-based state management (scalable to Firestore/Redis/Supabase)
- 🛡️ **Safety Guardrails**: Content filtering to prevent inappropriate content
- 📊 **Modular Architecture**: Clean separation of concerns for easy maintenance
- 🚀 **Production-Ready**: Comprehensive error handling and logging

## 🏗️ Architecture

```
StorieBook/
├── app.py                      # Main Streamlit application
├── story_engine/              # Core story generation logic
│   ├── __init__.py
│   ├── generator.py           # Gemini API integration
│   ├── prompts.py             # Prompt templates and engineering
│   └── state.py               # State management (session/DB)
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── constants.py           # App configuration
│   └── logger.py              # Logging utilities
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download the repository**

2. **Set up environment variables**

   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

   Or export directly:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```

5. **Open your browser**

   The app will automatically open at `http://localhost:8501`

## 🎮 How to Use

1. **Enter a World Prompt**: Describe the adventure world and your role
   - Example: *"Take me through an adventure like I am a wizard in the Harry Potter world with King Arthur era elements"*

2. **Click "Start Adventure"**: The AI generates your first chapter

3. **Make Choices**: Select from two options at the end of each chapter

4. **Shape Your Story**: Your choices influence the narrative direction

5. **Restart Anytime**: Use the "Restart Story" button to begin a new adventure

## 🎯 Example Prompts

- *"I'm a space explorer discovering ancient alien ruins on a distant planet"*
- *"I'm a detective in 1920s New York City solving supernatural mysteries"*
- *"I'm a chef competing in a magical cooking competition"*
- *"I'm a pirate captain searching for legendary treasure in a world of myths"*

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |

### Application Settings

Edit `utils/constants.py` to customize:

- `GEMINI_MODEL`: AI model to use
- `MAX_CHAPTERS`: Maximum chapters per story (default: 50)
- `TEMPERATURE`: Creativity level (0.0-1.0, default: 0.85)
- `MAX_TOKENS`: Maximum tokens per chapter (default: 2048)

## 🔐 Safety & Content Filtering

The application includes multiple safety layers:

- **Gemini Safety Settings**: Blocks harassment, hate speech, sexually explicit, and dangerous content
- **Prompt Engineering**: Instructs the model to avoid inappropriate content
- **Content Validation**: Checks chapter length and structure

## 📦 State Management

### Current: Session-Based

State is stored in `st.session_state` for the current session:
- ✅ No external dependencies
- ✅ Fast and simple
- ❌ Lost on page refresh
- ❌ Not persistent across devices

### Future: Database Integration

The architecture supports easy migration to:

**Firestore**
```python
# In utils/constants.py
DB_CONFIG = {
    "type": "firestore",
    "firestore": {"enabled": True}
}
```

**Redis**
```python
DB_CONFIG = {
    "type": "redis",
    "redis": {
        "host": "your-redis-host",
        "port": 6379,
        "enabled": True
    }
}
```

**Supabase**
```python
DB_CONFIG = {
    "type": "supabase",
    "supabase": {
        "url": "your-supabase-url",
        "key": "your-supabase-key",
        "enabled": True
    }
}
```

## 🚢 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `GEMINI_API_KEY` in Secrets:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
5. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t storiebook .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key storiebook
```

### Railway / Render / Heroku

1. Add a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Set environment variable `GEMINI_API_KEY`

3. Deploy using platform-specific instructions

## 🧪 Development

### Project Structure

- **app.py**: Main UI and orchestration
- **story_engine/generator.py**: Gemini API calls and chapter generation
- **story_engine/prompts.py**: Prompt engineering and templates
- **story_engine/state.py**: State management with DB abstraction
- **utils/constants.py**: Configuration and constants
- **utils/logger.py**: Structured logging

### Adding Features

1. **Custom Endings**: Modify `prompts.py` to detect story conclusions
2. **Save/Load Stories**: Implement database methods in `state.py`
3. **Multiple Models**: Add model selection in `constants.py` and `generator.py`
4. **Story Analytics**: Extend `state.py` to track metrics

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Log important events and errors

## 📊 Monitoring & Logging

Logs are written to stdout with configurable levels:

```python
# Set log level
export LOG_LEVEL=DEBUG

# View logs
streamlit run app.py 2>&1 | tee app.log
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Database backend implementations (Firestore, Redis, Supabase)
- Story export/import functionality
- Multiple language support
- Advanced prompt engineering
- Story branching visualization
- User authentication
- Story sharing features

## ⚠️ Limitations

- Stories are lost on page refresh (until database integration)
- Maximum 50 chapters per story (configurable)
- Dependent on Gemini API availability and rate limits
- Content quality depends on prompt engineering and model capabilities

## 📝 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Inspired by classic Choose Your Own Adventure books

## 📧 Support

For issues or questions:
1. Check the logs for error messages
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check Gemini API status

---

**Built with ❤️ for storytellers and adventure seekers everywhere**
