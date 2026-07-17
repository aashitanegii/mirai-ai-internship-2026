import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# Gemini Client
# -----------------------------
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_ai_client()

# -----------------------------
# Session State Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )

# -----------------------------
# App Title
# -----------------------------
st.title("💬 Gemini Chatbot")

# -----------------------------
# Display Previous Messages
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# User Input
# -----------------------------
if user_message := st.chat_input("Say something..."):

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Generate AI response
    with st.spinner("Thinking..."):
        response = st.session_state.gemini_chat.send_message(user_message)

    # Display AI response
    with st.chat_message("assistant"):
        st.write(response.text)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text,
        }
    )