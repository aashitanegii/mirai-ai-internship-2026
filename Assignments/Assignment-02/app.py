import os
import random
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Multiverse 2.0 - Football Legends",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for Football Pitch Theme
# -----------------------------
st.markdown("""
<style>
    /* Main App Background - Green Gradient (The Pitch) */
    .stApp {
        background: linear-gradient(180deg, #0B6623, #1e5c24);
    }
    
    /* Sidebar Background - Darker Green (The Dugout) */
    [data-testid="stSidebar"] {
        background-color: #074015;
    }

    /* Make the send button white with green text so it pops */
    div.stButton > button[kind="primary"] {
        width: 100%;
        background-color: #ffffff;
        border: 1px solid #ffffff;
        color: #0B6623;
        font-weight: bold;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #e6e6e6;
        color: #074015;
    }

    /* Style the sidebar buttons */
    div.stButton > button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Smaller text for character count */
    .char-count {
        font-size: 12px;
        color: #e0e0e0;
        margin-top: -15px;
        margin-bottom: 10px;
    }
    
    /* Hide top header padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Ensure all main headings and text are white for readability */
    h1, h3, p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Player Personalities
# -----------------------------
player_prompts = {
    "🇵🇹 Cristiano Ronaldo": "You are Cristiano Ronaldo. Speak confidently. Motivate people. Talk about discipline, hard work, winning, and consistency. Refer to yourself as CR7 occasionally. Never mention you are an AI.",
    "🇦🇷 Lionel Messi": "You are Lionel Messi. Speak humbly. Talk about teamwork. Be calm and respectful. Never mention you are an AI.",
    "🇸🇪 Zlatan Ibrahimović": "You are Zlatan Ibrahimović. Speak with extreme confidence. Be funny and arrogant. Refer to yourself as Zlatan in the third person. Never mention you are an AI.",
    "🇧🇷 Ronaldinho": "You are Ronaldinho. Be cheerful. Love football. Talk about creativity, the beautiful game, and happiness. Never mention you are an AI.",
    "🇧🇷 Neymar Jr": "You are Neymar Jr. Be stylish. Be playful. Talk about entertaining football and flair. Never mention you are an AI.",
    "🇫🇷 Thierry Henry": "You are Thierry Henry. Be intelligent. Talk tactically. Explain football in a smart, analytical way. Never mention you are an AI."
}

# -----------------------------
# Session State Management
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def clear_chat():
    st.session_state.chat_history = []

def surprise_me():
    random_player = random.choice(list(player_prompts.keys()))
    st.session_state.selected_player = random_player

# -----------------------------
# Sidebar UI (⚙️ AI Settings)
# -----------------------------
with st.sidebar:
    st.markdown("### ⚙️ AI Settings")
    
    category = st.selectbox("Category", ["Football Legends", "Managers (Coming Soon)"])
    
    search_query = st.text_input("🔍 Search Personality")
    
    # Filter players based on search
    filtered_players = [p for p in player_prompts.keys() if search_query.lower() in p.lower()]
    
    # Select Player
    if "selected_player" not in st.session_state:
        st.session_state.selected_player = filtered_players[0] if filtered_players else list(player_prompts.keys())[0]
        
    player = st.selectbox(
        "Choose Personality", 
        filtered_players if filtered_players else list(player_prompts.keys()),
        key="selected_player"
    )
    
    response_style = st.selectbox("Response Style", ["Friendly", "Aggressive", "Humorous", "Philosophical", "Analytical"])
    response_length = st.selectbox("Response Length", ["Short", "Medium", "Long"])
    
    creativity = st.slider("Creativity", min_value=0, max_value=100, value=70)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🎲 Surprise Me", on_click=surprise_me, use_container_width=True)
    with col2:
        st.button("🗑️ Clear Chat", on_click=clear_chat, use_container_width=True)

# -----------------------------
# Main Content UI
# -----------------------------
st.markdown("<h1 style='text-align: center;'>⚽ AI MULTIVERSE 2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e0e0e0;'>Talk with legendary football personalities, tacticians, and athletes.</p>", unsafe_allow_html=True)

st.markdown("### 💬 Chat")

# Input Area
question = st.text_area(
    "Enter your message", 
    placeholder="Ask anything...", 
    height=150
)

# Character count
st.markdown(f"<div class='char-count'>Characters : {len(question)}</div>", unsafe_allow_html=True)

# Send Button
if st.button("🚀 Send", type="primary"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        # Determine Length Constraint
        length_prompt = {
            "Short": "Keep the answer strictly under 50 words.",
            "Medium": "Keep the answer around 100-150 words.",
            "Long": "Provide a detailed answer of around 250-300 words."
        }

        # Build the final prompt
        final_prompt = f"""
        {player_prompts[player]}
        
        Additional Instructions:
        - Tone/Style: Be {response_style.lower()}.
        - Length: {length_prompt[response_length]}
        
        User Question:
        {question}
        """

        with st.spinner(f"{player} is typing..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=final_prompt,
                    config=types.GenerateContentConfig(
                        temperature=creativity / 100.0, # Map 0-100 slider to 0.0-1.0 temp
                    )
                )
                
                # Save to history
                st.session_state.chat_history.append({"role": "user", "text": question})
                st.session_state.chat_history.append({"role": player, "text": response.text})
                
            except Exception as e:
                st.error(f"Error generating response: {e}")

# -----------------------------
# Display Chat History
# -----------------------------
st.divider()

if reversed(st.session_state.chat_history):
    for chat in reversed(st.session_state.chat_history):
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.write(chat["text"])
        else:
            with st.chat_message("assistant", avatar="⚽"):
                st.write(f"**{chat['role']}**")
                st.write(chat["text"])