import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key from .env
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not API_KEY:
    st.error("Set GOOGLE_API_KEY in your .env file.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# Streamlit UI
st.title("🎭 Character Chatbot")

personality = st.selectbox(
    "Who do you want to talk to?",
    [
        "Sherlock Holmes",
        "Iron Man",
        "Harry Potter"
    ]
)

user_message = st.text_input("Say something:")

if st.button("SEND"):
    if user_message:

        ai_instructions = (
            f"You are acting as {personality}. "
            "Stay completely in character while replying."
        )

        with st.spinner("Connecting to the multiverse...."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config={
                    "system_instruction": ai_instructions
                },
                contents=user_message
            )

        st.subheader(f"{personality} says:")
        st.write(response.text)