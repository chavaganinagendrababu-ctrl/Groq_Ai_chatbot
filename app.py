import os
import streamlit as st
# pyrefly: ignore [missing-import]
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


# Set page config for a premium feel
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global Styles
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    
    /* Global overrides */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Clean chat input styling */
    .stChatInput {
        border-radius: 12px;
    }
    
    /* Status Badge styling */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .status-active {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-missing {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .status-unknown {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Banner
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 30px; border-radius: 16px; margin-bottom: 25px; text-align: center; box-shadow: 0 10px 20px -5px rgba(124, 58, 237, 0.3);">
        <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;">🤖 Groq Intelligence Hub</h1>
        <p style="color: #c7d2fe; margin: 8px 0 0 0; font-size: 1.15rem; font-weight: 400; opacity: 0.95;">An ultra-fast, highly configurable real-time AI assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Configuration
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 1.6rem; font-weight: 600; color: #4f46e5;">🛠️ Control Panel</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.7;">Tune parameters and manage session</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);"/>
    </div>
    """,
    unsafe_allow_html=True
)

# 1. API Key handling
# Get it from environment (.env file)
api_key = os.environ.get("GROQ_API_KEY", "")

# 2. Connection status checks and client initialization
client = None
status_html = ""
can_query = False

if not api_key:
    status_html = '<span class="status-badge status-missing">🔴 API Key Missing</span>'
else:
    try:
        client = Groq(api_key=api_key)
        # Verify connectivity by attempting to list models
        # This checks if the key is valid
        models_data = client.models.list()
        can_query = True
        status_html = '<span class="status-badge status-active">🟢 Connected to Groq</span>'
    except Exception as e:
        status_html = '<span class="status-badge status-unknown">🟡 Connection Error / Invalid Key</span>'
        client = None

st.sidebar.markdown(status_html, unsafe_allow_html=True)

# 3. Model selection
default_models = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "mixtral-8x7b-32768"
]

selected_model = None

if client and can_query:
    try:
        # Fetch active models dynamically from Groq
        fetched_models = client.models.list()
        # Filter out audio/Whisper models
        model_list = [
            m.id for m in fetched_models.data 
            if not any(x in m.id.lower() for x in ["whisper", "audio", "guard"])
        ]
        # Sort models to keep featured ones at top
        model_list.sort()
        
        # Ensure we have our main recommended models first if they exist
        featured_models = [m for m in default_models if m in model_list]
        other_models = [m for m in model_list if m not in default_models]
        final_model_list = featured_models + other_models
        
        selected_model = st.sidebar.selectbox(
            "Select Model",
            options=final_model_list,
            index=0 if final_model_list else None,
            help="Dynamic models loaded directly from your Groq account."
        )
    except Exception:
        # Fallback to curated static list
        selected_model = st.sidebar.selectbox("Select Model", options=default_models, index=0)
else:
    selected_model = st.sidebar.selectbox("Select Model", options=default_models, index=0)

# 4. Parameters
st.sidebar.markdown('<p style="font-weight:600; margin-bottom: 5px;">Parameters</p>', unsafe_allow_html=True)
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Higher values make output more random, lower values more deterministic."
)

max_tokens = st.sidebar.slider(
    "Max Completion Tokens",
    min_value=256,
    max_value=8192,
    value=4096,
    step=256,
    help="The maximum number of tokens to generate in the completion."
)

# 5. System Prompt Customization
system_prompt = st.sidebar.text_area(
    "System Instruction",
    value="You are a helpful, friendly, and knowledgeable AI assistant.",
    help="Set the behavior, persona, or context for the AI assistant."
)

st.sidebar.markdown("<br/>", unsafe_allow_html=True)

# 6. Session management - Clear chat button
if st.sidebar.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# --- Main App Chat Interface ---

# Welcome screen when no messages are present
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown(
        """
        <div style="background-color: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 30px; border-radius: 12px; margin-top: 10px;">
            <h3>👋 Welcome to the Chatbot!</h3>
            <p>This workspace is ready for your conversations. Here are a few things you can do:</p>
            <ul>
                <li>Type your message in the chat input at the bottom.</li>
                <li>Adjust parameters like <b>temperature</b> or the <b>system instruction</b> in the sidebar to shape responses.</li>
                <li>Switch LLM models dynamically from the model selection list.</li>
            </ul>
            <p style="font-size: 0.9rem; opacity: 0.6; margin-top: 15px;"><i>Note: Please ensure your Groq API key is configured in the `.env` file in the workspace directory.</i></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Render existing message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
user_input = st.chat_input("Message the chatbot...")

if user_input:
    # 1. Render user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Check key and client readiness
    if not api_key:
        with st.chat_message("assistant"):
            st.error("🔑 API Key is missing. Please set your Groq API Key in the `.env` file.")
    elif client is None:
        with st.chat_message("assistant"):
            st.error("❌ Connection failed. Please check if your Groq API Key is valid and try again.")
    else:
        # 3. Stream assistant response from Groq
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Construct standard message format with system instructions
            messages_payload = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages:
                messages_payload.append({"role": msg["role"], "content": msg["content"]})
                
            try:
                # API Call with streaming
                completion_stream = client.chat.completions.create(
                    model=selected_model,
                    messages=messages_payload,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                # Iterate and stream tokens
                for chunk in completion_stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                # Set final text without blinking cursor
                response_placeholder.markdown(full_response)
                
                # Append assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                # Handle API exceptions gracefully
                err_msg = str(e)
                st.error(f"⚠️ Groq API Error: {err_msg}")
                if "rate_limit" in err_msg.lower():
                    st.info("💡 You may have exceeded your Groq rate limits. Please wait a moment before trying again.")
                elif "authentication" in err_msg.lower() or "api_key" in err_msg.lower():
                    st.info("💡 Please verify that your Groq API key is correct and active.")
