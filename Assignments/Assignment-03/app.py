import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES & INITIALIZE GEMINI
# ---------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="Football Legends AI Multiverse",
    page_icon="⚽",
    layout="wide"
)
st.title("⚽ Football Legends AI Multiverse")

# ---------------------------------------------------
# 2. INITIALIZE THE MEMORY VAULT (Task 1)
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# 3. SIDEBAR - PLAYER / PERSONALITY SELECTION
# ---------------------------------------------------
st.sidebar.title("🌍 Football Multiverse")
st.sidebar.markdown("Choose a legend and personality to begin your AI conversation.")

player = st.sidebar.selectbox(
    "Select a player:",
    ["Cristiano Ronaldo", "Lionel Messi", "Pele", "Diego Maradona", "Zinedine Zidane"]
)

personality = st.sidebar.selectbox(
    "Select personality mode:",
    ["Motivational Coach", "Trash Talker", "Humble Legend", "Tactical Analyst"]
)

st.sidebar.markdown("---")
st.sidebar.success(f"🏆 {player}")
st.sidebar.info(f"🎭 {personality}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------
# 4. WELCOME MESSAGE
# ---------------------------------------------------
st.markdown("""
### 🏟️ Welcome to the Football Legends AI Multiverse!
Travel across different football universes and chat with legendary players.
Choose a legend from the sidebar and start your conversation.
""")

# ---------------------------------------------------
# 5. RENDER CHAT HISTORY (Task 2)
# ---------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# 6. CHAT INPUT (Task 3)
# ---------------------------------------------------
if user_message := st.chat_input("Ask your football legend..."):

    # ---- Save + display user message (Task 4) ----
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )
    with st.chat_message("user"):
        st.markdown(user_message)

    # ---- Build the prompt with player + personality context ----
    final_prompt = f"""
    You are {player}.
    Your personality is: {personality}.
    Always remain in character.
    Never mention you are an AI.
    Reply naturally like the real football legend.
    Keep responses under 120 words.
    Use real football knowledge whenever appropriate.
    User:
    {user_message}
    """

    # ---- Call Gemini API ----
    with st.chat_message("assistant"):
        with st.spinner(f"⚽ {player} is preparing a response..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=final_prompt
                )
                reply = response.text
            except Exception as e:
                reply = f"Error: {e}"

            st.markdown(reply)

    # ---- Save AI response (Task 4) ----
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )