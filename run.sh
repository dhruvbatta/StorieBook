#!/bin/bash

# StorieBook Quick Start Script

echo "📚 Starting StorieBook..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your GEMINI_API_KEY"
    echo "Then run this script again."
    exit 1
fi

# Check if API key is set
if grep -q "your_gemini_api_key_here" .env; then
    echo "⚠️  Warning: GEMINI_API_KEY not configured in .env"
    echo "Please edit .env and add your actual API key"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo ""
echo "✅ Environment ready!"
echo "🚀 Launching StorieBook on http://localhost:8501"
echo ""

# Run Streamlit
streamlit run app.py
