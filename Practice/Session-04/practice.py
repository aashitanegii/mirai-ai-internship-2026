import streamlit as st
import requests
import urllib.parse
import time
from PIL import Image
from io import BytesIO

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="The AI Image Studio", page_icon="🎨", layout="wide")
st.title("🎨 THE AI IMAGE STUDIO")

# ---------------------------------------------------
# INITIALIZE THE MEMORY VAULT
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# SIDEBAR - CONFIGURATION
# ---------------------------------------------------
st.sidebar.header("Configuration")

art_style = st.sidebar.selectbox(
    "Choose an Art Style",
    ["Photorealistic", "Anime/Manga", "Vintage Victorian", "Cyberpunk", "Watercolor", "3D Render"]
)

# Sliders clamped to 1024 max for better free API stability
width = st.sidebar.slider("Image Width", min_value=512, max_value=1024, value=512, step=64)
height = st.sidebar.slider("Image Height", min_value=512, max_value=1024, value=512, step=64)

# Show the selected resolution in the sidebar
st.sidebar.write(f"🖼️ Selected Resolution: {width} × {height}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Gallery"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------
# RENDER CHAT/GALLERY HISTORY
# ---------------------------------------------------
for idx, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(f"**Prompt:** {message['content']}")
    else:
        with st.chat_message("assistant", avatar="🎨"):
            # Using columns to center and prevent past images from blowing up huge
            h_col1, h_col2, h_col3 = st.columns([1, 2, 1])
            with h_col2:
                st.image(message["content"], caption="Generated Image", use_container_width=True)
                
                # Dynamic unique download key for history persistence
                st.download_button(
                    label="📥 Download Image",
                    data=message["content"],
                    file_name=f"generated_image_{idx}.png",
                    mime="image/png",
                    key=f"download_{idx}"
                )

# ---------------------------------------------------
# HELPER: GENERATE IMAGE (verifies actual returned size)
# ---------------------------------------------------
def generate_image(prompt, width, height, retries=3):
    encoded_prompt = urllib.parse.quote(prompt)

    # Unique seed every call = avoids CDN serving a stale cached image
    seed = int(time.time() * 1000)

    # Pass selected dimensions to the URL parameters
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
        f"&model=flux"
        f"&nologo=true"
        f"&seed={seed}"
    )

    last_error = None
    wait_time = 3

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=90)

            if response.status_code == 200:
                # Verify actual returned dimensions using Pillow
                img = Image.open(BytesIO(response.content))
                actual_size = img.size  # returns tuple (width, height)
                return response.content, actual_size, None

            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                sleep_for = int(retry_after) if retry_after else wait_time
                last_error = "Rate limited (429)"
                time.sleep(sleep_for)
                wait_time *= 2
                continue

            else:
                last_error = f"Status {response.status_code}"
                time.sleep(wait_time)
                wait_time *= 2
                continue

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            time.sleep(wait_time)
            wait_time *= 2
            continue

    return None, None, last_error

# ---------------------------------------------------
# CHAT INPUT & EXECUTION
# ---------------------------------------------------
if user_prompt := st.chat_input("Describe the image you want to generate..."):

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"**Prompt:** {user_prompt}")

    full_prompt = f"""
{user_prompt},
{art_style} style,
cinematic lighting,
ultra realistic,
highly detailed,
professional composition,
8K,
award-winning digital art,
sharp focus,
high quality
"""
    with st.chat_message("assistant", avatar="🎨"):
        # Show the requested size while generating in the spinner
        with st.spinner(f"🎨 Generating {width}×{height} image..."):
            image_bytes, actual_size, error = generate_image(full_prompt, width, height)

            if image_bytes:
                actual_width, actual_height = actual_size
                st.success(f"Requested: {width}×{height} | Received: {actual_width}×{actual_height}")
                
                if actual_size != (width, height):
                    st.warning("⚠️ Pollinations adjusted the resolution size (model minimum constraint/rounding).")
                
                # Using 3 columns to contain the image so it doesn't stretch across the wide layout
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(image_bytes, caption="Generated Image", use_container_width=True)
                    
                    # Live generation download button
                    st.download_button(
                        label="📥 Download Image",
                        data=image_bytes,
                        file_name="generated_image.png",
                        mime="image/png",
                        key=f"download_new_{int(time.time())}"
                    )
                
                final_content = image_bytes
            else:
                st.error(f"Image generation failed after retries: {error}")
                final_content = None

    if final_content:
        st.session_state.messages.append({"role": "assistant", "content": final_content})