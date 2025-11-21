@echo off
REM StorieBook Quick Start Script for Windows

echo 📚 Starting StorieBook...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo Please edit .env and add your GEMINI_API_KEY
    echo Then run this script again.
    pause
    exit /b 1
)

REM Load environment variables (basic version)
for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do set %%a

echo.
echo ✅ Environment ready!
echo 🚀 Launching StorieBook on http://localhost:8501
echo.

REM Run Streamlit
streamlit run app.py

pause
