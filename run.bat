@echo off
title Streamlit Groq Chatbot Launcher
echo ===================================================
echo   Streamlit Groq Chatbot Setup & Startup Script
echo ===================================================
echo.

:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.11+ and run this script again.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo [INFO] Creating Python virtual environment in .venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install/Upgrade dependencies
echo [INFO] Installing/Checking dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies verified.
echo.

:: Launch Streamlit app
echo [INFO] Launching Streamlit App...
streamlit run app.py
echo.
pause
