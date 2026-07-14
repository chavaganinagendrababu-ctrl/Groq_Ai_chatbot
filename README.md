# Streamlit Groq Chatbot

A premium, modern chatbot built using Streamlit and powered by the ultra-fast Groq API. It includes options for dynamic model listing, system instructions customization, temperature tuning, and session management.

## Features

- **Dynamic Model Selection**: Connects directly to Groq to retrieve the latest active models (with a curated list fallback).
- **Streaming Responses**: Messages stream in real-time, just like standard chat applications.
- **Advanced Sidebar Settings**:
  - API key configuration (override or set directly).
  - Temperature slider (0.0 to 2.0) to control creativity.
  - Max completion tokens limit selector.
  - System prompt customizer to change the chatbot's personality and instructions.
- **Session Management**: Easy "Clear Chat History" utility to start fresh.
- **Premium Styling**: Glassmorphic layout adjustments, sleek dark mode/gradient accents, and clean layout cards.

## Setup Instructions

### Prerequisites
- Python 3.11 or newer installed on your machine.
- A Groq API Key (get one from the [Groq Console](https://console.groq.com/keys)).

### Automated Setup (Windows)
Double-click `run.bat` to automatically set up the virtual environment, install dependencies, and run the Streamlit app.

### Manual Setup
1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   - Open the `.env` file and set your key: `GROQ_API_KEY=your_actual_api_key_here`
   - Alternatively, you can enter the API key directly in the application's sidebar when it runs.
4. **Run the App**:
   ```bash
   streamlit run app.py
   ```
