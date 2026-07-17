import streamlit as st
import requests
import random
import urllib.parse
import time

st.set_page_config(page_title="Stateful AI Image Studio", page_icon="🎨", layout="wide")

# ==========================================
# SESSION 6 CONCEPT: Initialize Session State
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# SESSION 6 CONCEPT: Rate Limiting (Max 7 images)
user_count = sum(1 for msg in st.session_state.messages if msg["role"] == "user")

# ---------------------------------------------------------
# Sidebar Settings
# ---------------------------------------------------------
st.sidebar.header("⚙️ Image Settings")

# Core settings
width = st.sidebar.slider("Image Width", min_value=256, max_value=1024, value=512, step=256)
height = st.sidebar.slider("Image Height", min_value=256, max_value=1024, value=512, step=256)
art_style = st.sidebar.selectbox("Art Style", ["Realistic", "Anime_Manga", "Cyberpunk", "Watercolor"])

# Task 3: The "Magic Enhance" Toggle
magic_enhance = st.sidebar.checkbox("☑️ Enable Magic Enhance")
st.sidebar.caption("✨ Secretly adds professional boost keywords to your prompt.")

st.sidebar.markdown("---")

# Task 4: Surprise Me (Moved to sidebar for chat UI compatibility)
surprise_clicked = st.sidebar.button("🎲 Surprise Me!", use_container_width=True)

st.sidebar.markdown("---")

# SESSION 6 CONCEPT: Clear History
if st.sidebar.button("🗑️ Clear Gallery", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------------
# Main Interface & Chat History
# ---------------------------------------------------------
st.title("🎨 Stateful AI Image Studio")
st.write("Generate custom images with a persistent gallery using Streamlit Session State.")

# SESSION 6 CONCEPT: Iterating through chat history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🎨"):
        if msg["role"] == "user":
            st.markdown(f"**Prompt:** {msg['content']}")
        else:
            # Render true to size (no use_container_width)
            st.image(msg["content"], caption=f"🎨 Style: {msg.get('style', 'Custom')}")
            
            # Task 2: File Extension Fix (Historical downloads)
            safe_style = msg.get("style", "ai").lower()
            st.download_button(
                label="📥 Download Image",
                data=msg["content"],
                file_name=f"{safe_style}_image_{idx}.png",
                mime="image/png",
                key=f"dl_history_{idx}"
            )

# SESSION 6 CONCEPT: Rate Limiting Enforcement
if user_count >= 7:
    st.warning("⚠️ Generation limit reached. Please click 'Clear Gallery' in the sidebar to start over.")
    st.stop() # Stops execution so chat input disappears

# ---------------------------------------------------------
# Input Logic (User Input vs Surprise Me)
# ---------------------------------------------------------
prompt_to_process = None

# Check if Surprise Me was clicked
if surprise_clicked:
    surprise_prompts = [
        "An astronaut riding a horse on Mars",
        "A cyberpunk street food vendor in Tokyo",
        "A floating castle above the clouds",
        "A giant dragon protecting a futuristic city",
        "A neon jungle with glowing animals"
    ]
    prompt_to_process = random.choice(surprise_prompts)
else:
    # SESSION 6 CONCEPT: Chat Input
    user_input = st.chat_input("Describe the image you want to create...")
    if user_input:
        prompt_to_process = user_input

# ---------------------------------------------------------
# Generation Execution
# ---------------------------------------------------------
if prompt_to_process:
    # 1. Add user prompt to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"**Prompt:** {prompt_to_process}")
        
    # 2. Build the prompt
    full_prompt = f"{prompt_to_process}, {art_style}"

    # Task 3: Apply the Magic Enhance boost words
    if magic_enhance:
         full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
         
    encoded_prompt = urllib.parse.quote(full_prompt)
    seed = random.randint(1, 1000000)

    # Task 1: The Broken Sliders (URL Parameters Fix)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}"
        f"&height={height}"
        f"&model=flux"
        f"&seed={seed}"
    )

    # 3. Generate and display the assistant response
    with st.chat_message("assistant", avatar="🎨"):
        # Debug text for demo video
        if magic_enhance:
            st.info(f"🕵️‍♂️ **Debug - Sending to AI:** {full_prompt}")
            
        with st.spinner(f"🎨 Generating {width}×{height} image..."):
            try:
                response = requests.get(url, timeout=90)
                
                if response.status_code == 200:
                    image_data = response.content
                    
                    st.image(image_data, caption=f"🎨 Style: {art_style}")
                    
                    # Task 2: File Extension Fix (Live download)
                    st.download_button(
                        label="📥 Download Image",
                        data=image_data,
                        file_name=f"{art_style.lower()}_image.png",
                        mime="image/png",
                        key=f"dl_new_{int(time.time())}"
                    )
                    
                    # Save image to session state history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": image_data,
                        "style": art_style
                    })
                elif response.status_code == 429:
                    st.warning("🚦 Pollinations is currently busy. Please try again.")
                else:
                    st.error("Failed to fetch image. Please try again.")
            except requests.exceptions.Timeout:
                st.error("⏳ The request timed out. The server might be overloaded.")