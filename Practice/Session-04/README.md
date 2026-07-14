
---

# 📒 MirAI Internship – Session 4 Practice Notes

**Project:** The AI Image Studio

**Objective:** Build an AI-powered image generation web application using Streamlit and the Pollinations AI API.

---

# 🎯 What We Built

We built an **AI Image Generation Studio** where users can:

* Enter an image prompt.
* Choose an art style.
* Select image resolution.
* Generate AI images.
* View previous generations.
* Download generated images.
* Clear the image gallery.

---

# 📚 Concepts Learned

## 1️⃣ Streamlit Page Configuration

Used

```python
st.set_page_config()
```

Purpose:

* Set page title.
* Set browser icon.
* Set page layout.

Example:

```python
st.set_page_config(
page_title="The AI Image Studio",
page_icon="🎨",
layout="wide"
)
```

---

## 2️⃣ Session State (Memory Vault)

Learned how to store previous prompts and generated images.

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Purpose:

* Keeps gallery history.
* Prevents data from disappearing after reruns.

Without Session State:

```text
Generate Image
↓

Refresh

↓

Everything disappears
```

With Session State:

```text
Generate Image

↓

Refresh

↓

Images remain
```

---

## 3️⃣ Sidebar

Created a configuration panel using

```python
st.sidebar
```

Used for:

* Art Style
* Width
* Height
* Gallery Controls

---

## 4️⃣ Selectbox

Used

```python
st.selectbox()
```

to allow users to choose an art style.

Available styles:

* Photorealistic
* Anime
* Cyberpunk
* Watercolor
* Victorian
* 3D Render

---

## 5️⃣ Sliders

Used

```python
st.slider()
```

to let users choose

* Image Width
* Image Height

Example:

```python
width = st.slider(...)
```

This makes the application interactive.

---

## 6️⃣ Dynamic Text

Displayed the selected resolution.

```python
st.sidebar.write(
f"Selected Resolution: {width} × {height}"
)
```

Learned how to use **f-strings** with Streamlit.

---

## 7️⃣ Buttons

Used

```python
st.button()
```

for

* Clear Gallery

---

## 8️⃣ Rerunning the App

Used

```python
st.rerun()
```

Purpose:

Refresh the application immediately after clearing the gallery.

---

# 🖼️ Rendering Previous Images

Used

```python
for message in st.session_state.messages:
```

to redraw every previous prompt and image.

Learned:

* for loop
* enumerate()
* dictionaries
* session history

---

# 👤 Chat Interface

Instead of a normal textbox, used

```python
st.chat_input()
```

for entering prompts.

Also used

```python
st.chat_message()
```

to display

* User Prompt
* Generated Image

This creates a ChatGPT-like interface.

---

# 🖼️ Displaying Images

Used

```python
st.image()
```

to display AI-generated images.

Also learned

```python
use_container_width=True
```

to make images responsive.

---

# 📥 Download Button

Used

```python
st.download_button()
```

Purpose:

Allow users to download generated images.

Parameters learned:

* label
* data
* file_name
* mime
* key

---

# 🏗️ Creating Functions

Created our own function

```python
generate_image()
```

Purpose:

Keep code reusable and organized.

Instead of repeating code, we simply call

```python
generate_image(...)
```

---

# 🌐 Pollinations AI API

Connected the application to Pollinations AI.

Workflow

```text
User Prompt

↓

Pollinations API

↓

AI Model (FLUX)

↓

Generated Image
```

---

# 🔗 URL Encoding

Used

```python
urllib.parse.quote()
```

Purpose:

Convert prompts into URL-safe format.

Example

```text
Black Dragon

↓

Black%20Dragon
```

---

# 📤 API Request

Constructed an API URL.

Learned about

* Query Parameters
* URL Building

Example

```text
width
height
model
seed
```

---

# 🎲 Seed

Generated

```python
seed = int(time.time()*1000)
```

Purpose:

Generate a unique image every request.

Prevents cached images.

---

# 📡 HTTP Request

Used

```python
requests.get()
```

to communicate with Pollinations AI.

---

# 📥 API Response

Received

```python
response.content
```

which contains the generated image.

---

# 🖼️ Binary Image Data

The API does **not** return text.

Instead it returns

```text
Binary Bytes
```

These bytes represent the generated image.

---

# 📚 Pillow (PIL)

Used

```python
Image.open()
```

to inspect the generated image.

Purpose:

Read the image without displaying it.

---

# 📏 Image Size Verification

Learned

```python
img.size
```

returns

```text
(width,height)
```

Example

```text
Requested

512×512

↓

Received

512×512
```

or

```text
Requested

640×640

↓

Received

768×768
```

This verifies what the API actually returned.

---

# ⚠️ Error Handling

Learned how to detect

```text
HTTP 429
```

Meaning

```text
Too Many Requests
```

Implemented retry logic.

---

# 🔄 Retry Mechanism

Instead of immediately failing,

the app waits

```text
3 sec

↓

6 sec

↓

12 sec
```

and tries again.

---

# ⏳ Time Module

Used

```python
time.sleep()
```

Purpose:

Pause before retrying.

Also used

```python
time.time()
```

for unique seeds.

---

# 📝 Prompt Engineering

Instead of

```text
Black Dragon
```

we improved prompts

```text
Black Dragon,
Photorealistic,
cinematic lighting,
8K,
ultra detailed,
award-winning digital art
```

Result:

Better image quality.

---

# 🧩 Python Concepts Used

* Functions
* Variables
* Lists
* Dictionaries
* Loops
* Conditional Statements
* Exception Handling
* f-Strings
* Modules
* API Calls

---

# 📦 Libraries Used

| Library          | Purpose                                   |
| ---------------- | ----------------------------------------- |
| **streamlit**    | Build the web application                 |
| **requests**     | Send HTTP requests to Pollinations AI     |
| **urllib.parse** | Encode prompts into URL-safe format       |
| **time**         | Generate seeds and retry delays           |
| **Pillow (PIL)** | Read image metadata and dimensions        |
| **BytesIO**      | Convert binary bytes into an image object |

---

# ⭐ Key Learning Outcomes

By completing this Session 4 practice, we learned to:

* Build an AI image generation application using **Streamlit**.
* Design an interactive UI with **sidebar, sliders, buttons, and chat components**.
* Generate AI images through the **Pollinations AI API**.
* Pass parameters like **prompt, art style, width, height, and seed** to an API.
* Handle **HTTP requests**, **responses**, and **binary image data**.
* Verify the actual image resolution using **Pillow**.
* Implement **session state** to maintain image history.
* Add practical features like **download buttons**, **gallery management**, and **retry logic**.
* Improve outputs using **prompt engineering** and manage API limitations with **error handling**.

This practice project ties together the main ideas from Session 4: building a polished AI-powered application that communicates with an image generation model through an API while providing a smooth user experience.
