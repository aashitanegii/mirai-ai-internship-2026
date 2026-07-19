import streamlit as st
import google.generativeai as genai
import requests
import urllib.parse
import json
import io
from gtts import gTTS

# ==========================================
# PHASE 1: UI & CONFIGURATION
# ==========================================
st.set_page_config(page_title="AI Visual Novel Engine", page_icon="📖", layout="centered")

# Animated Background
animated_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(45deg, #0e1117, #1a1a2e, #16213e, #0e1117);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
[data-testid="stSidebar"] {
    background-color: rgba(14, 17, 23, 0.85); 
}
</style>
"""
st.markdown(animated_bg, unsafe_allow_html=True)

# 1. Cache the Gemini Client & Enhanced JSON System Prompt
@st.cache_resource
def load_gemini_client():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    sys_prompt = """You are an interactive RPG visual novel engine.
    Return ONLY valid JSON.
    Do NOT include: Markdown formatting, ```json, explanations, greetings, or notes.
    Your response MUST follow this schema exactly:
    {
      "story_text": "...",
      "image_prompt": "...",
      "options": ["...", "...", "..."],
      "inventory": ["item1", "item2"]
    }
    The options array must contain exactly 3 short action choices.
    The image_prompt should be highly detailed, comma-separated, and optimized for an AI image generator.
    The story_text should be atmospheric, written in second person ('You'), and match the requested length.
    Update the inventory array dynamically if the user picks up or uses an item."""
    
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=sys_prompt
    )

model = load_gemini_client()

# 2. Initialize Session State
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "novel_history" not in st.session_state:
    st.session_state.novel_history = [] 
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# 3. Sidebar Configuration (Updated Header to Match Assignment Wording)
with st.sidebar:
    st.header("📚 Story Settings", divider="violet")
    
    genre = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Cyberpunk", "Horror", "Mystery"])
    art_style = st.selectbox("Art Style", ["Anime", "Hyperrealistic", "Watercolor", "Pixel Art"])
    difficulty = st.select_slider("Difficulty", options=["Story Mode", "Normal", "Hardcore"], value="Normal")
    story_length = st.radio("Pacing", ["Short & Punchy", "Descriptive & Long"])
    
    st.markdown("---")
    st.subheader(f"🎒 Inventory ({len(st.session_state.inventory)})")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.markdown(f"- {item}")
    else:
        st.caption("Your pockets are empty.")
        
    st.markdown("---")
    st.metric("Scenes Played", len(st.session_state.novel_history))
    
    if st.button("🔄 Restart Story", use_container_width=True, type="primary"):
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.novel_history = []
        st.session_state.inventory = []
        st.rerun()

# ==========================================
# CORE ENGINE
# ==========================================
def process_turn(user_input):
    with st.status("🎬 The Director is rendering the next scene...", expanded=True) as status:
        
        status.update(label="Writing narrative and generating choices...")
        try:
            engine_prompt = f"[System Context: Difficulty is {difficulty}, Length is {story_length}. Current Inventory: {st.session_state.inventory}]. User Action: {user_input}"
            
            response = st.session_state.chat.send_message(engine_prompt)
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(raw_text)
            story_text = data.get("story_text", "The story pauses unexpectedly...")
            image_prompt = data.get("image_prompt", "A blank, mysterious void")
            options = data.get("options", ["Look around", "Wait", "Inventory"])
            new_inventory = data.get("inventory", st.session_state.inventory)
            
            # Safeguard: Ensure exactly 3 options
            if not isinstance(options, list) or len(options) != 3:
                options = ["Proceed cautiously", "Investigate further", "Retreat"]
                
            st.session_state.inventory = new_inventory
        except Exception as e:
            status.update(label="❌ Script Error", state="error")
            st.error(f"Failed to parse the AI's response into the game engine. Error: {e}")
            st.stop()

        image_bytes = None
        audio_bytes = None

        status.update(label="Painting the scene...")
        try:
            full_image_prompt = f"{image_prompt}, {art_style} style, masterpiece, high quality"
            encoded_prompt = urllib.parse.quote(full_image_prompt)
            
            # Protected string building to keep URL clean from markdown processing loops
            url_domain = "".join(["https://", "image.pollinations.ai/prompt/"])
            url = (
                f"{url_domain}{encoded_prompt}"
                f"?width=768"
                f"&height=432"
                f"&model=flux"
                f"&nologo=true"
            )
            
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                image_bytes = res.content
            else:
                st.toast("Image server is busy, skipping visual...", icon="⚠️")
        except requests.exceptions.RequestException:
            st.toast("Image server is busy, skipping visual...", icon="⚠️")

        status.update(label="Recording voiceover...")
        try:
            tts = gTTS(text=story_text, lang='en', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            audio_bytes = fp.getvalue()
        except Exception as e:
            st.toast(f"Audio error: {e}", icon="⚠️")

        st.session_state.novel_history.append({
            "story": story_text,
            "image": image_bytes,
            "audio": audio_bytes,
            "options": options,
            "art_style": art_style
        })
        status.update(label="Scene Complete!", state="complete", expanded=False)

# ==========================================
# UI RENDERING
# ==========================================
st.title("📖 :rainbow[AI Visual Novel]")

if len(st.session_state.novel_history) == 0:
    st.markdown("### 🎮 Welcome to the AI Visual Novel Generator")
    st.info("Configure your game settings in the sidebar, then click below to launch your multi-modal adventure.")
    if st.button("🚀 Start New Game", type="primary", use_container_width=True):
        process_turn(f"Start a {genre} story.")
        st.rerun()

for i, scene in enumerate(st.session_state.novel_history):
    st.markdown("---")
    if scene["image"]:
        st.image(scene["image"], use_container_width=True)
        st.download_button(
            label="📥 Save Scene Artwork", 
            data=scene["image"], 
            file_name=f"scene_{i}.png", 
            mime="image/png",
            key=f"download_{i}"
        )
    
    st.markdown(f"### {scene['story']}")
    if scene["audio"]:
        st.audio(scene["audio"], format="audio/mp3")

    if i == len(st.session_state.novel_history) - 1:
        st.write("**Make your choice:**")
        cols = st.columns(len(scene["options"]))
        for idx, option in enumerate(scene["options"]):
            with cols[idx]:
                if st.button(option, key=f"btn_{i}_{idx}", use_container_width=True):
                    process_turn(f"I choose to: {option}")
                    st.rerun()