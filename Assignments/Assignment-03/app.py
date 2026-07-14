import os
import time
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
# 2. AVATAR MAP
# ---------------------------------------------------
AVATARS = {
    "Cristiano Ronaldo": "🐐",
    "Lionel Messi": "⚽",
    "Pele": "👑",
    "Diego Maradona": "🔥",
    "Zinedine Zidane": "🎩",
}

# ---------------------------------------------------
# 3. INITIALIZE THE MEMORY VAULT (Task 1)
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# 4. SIDEBAR - PLAYER / PERSONALITY SELECTION
# ---------------------------------------------------
st.sidebar.title("🌍 Football Multiverse")
st.sidebar.markdown("Choose a legend and personality to begin your AI conversation.")

player = st.sidebar.selectbox(
    "Select a player:",
    list(AVATARS.keys())
)

personality = st.sidebar.selectbox(
    "Select personality mode:",
    ["Motivational Coach", "Trash Talker", "Humble Legend", "Tactical Analyst"]
)

commentary_mode = st.sidebar.toggle("🎙️ Match Commentary Mode")

st.sidebar.markdown("---")
st.sidebar.success(f"🏆 {player}")
st.sidebar.info(f"🎭 {personality}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------
# 5. WELCOME MESSAGE
# ---------------------------------------------------
st.markdown("""
### 🏟️ Welcome to the Football Legends AI Multiverse!
Choose a legend from the sidebar and start your conversation.
""")

# ---------------------------------------------------
# 6. RENDER CHAT HISTORY (Task 2)
# ---------------------------------------------------
for message in st.session_state.messages:
    avatar = AVATARS.get(player, "⚽") if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------------------
# 7. CHAT INPUT (Task 3)
# ---------------------------------------------------
if user_message := st.chat_input("Ask your football legend..."):

    # ---- Save + display user message (Task 4) ----
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_message)

    # ---- Build prompt (with optional commentary mode) ----
    mode_instruction = (
        "Describe your answer like a live football match commentator, energetic and dramatic."
        if commentary_mode else ""
    )

    final_prompt = f"""
    You are {player}.
    Your personality is: {personality}.
    Always remain in character.
    Never mention you are an AI.
    Reply naturally like the real football legend.
    Keep responses under 120 words.
    Use real football knowledge whenever appropriate.
    {mode_instruction}
    User:
    {user_message}
    """

    # ---- Call Gemini API with streaming (typewriter effect) ----
    with st.chat_message("assistant", avatar=AVATARS.get(player, "⚽")):
        placeholder = st.empty()
        full_reply = ""
        try:
            stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=final_prompt
            )
            for chunk in stream:
                if chunk.text:
                    full_reply += chunk.text
                    placeholder.markdown(full_reply + "▌")
                    time.sleep(0.01)
            placeholder.markdown(full_reply)
        except Exception as e:
            full_reply = f"Error: {e}"
            placeholder.markdown(full_reply)

    # ---- Save AI response (Task 4) ----
    st.session_state.messages.append(
        {"role": "assistant", "content": full_reply}
    )

# ---------------------------------------------------
# 8. DOWNLOAD CONVERSATION
# ---------------------------------------------------
if st.session_state.messages:
    transcript = "\n\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages
    )
    st.download_button(
        "📥 Download Conversation",
        transcript,
        file_name=f"chat_with_{player.replace(' ', '_')}.txt"
    )