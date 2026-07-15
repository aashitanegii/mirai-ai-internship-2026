
---

# 📒 MirAI Internship – Session 5 Notes

**Topic:** AI Image Generation with Streamlit, Pollinations AI, REST APIs, API Requests & Responses, Binary Data, MIME Types & Real-World AI Applications

---

# 🎯 Session Objective

In this session, we learned how to:

* Build an AI Image Generation application using **Streamlit**.
* Generate images using **Pollinations AI**.
* Understand REST APIs and HTTP communication.
* Learn API request and response structures.
* Handle binary image data.
* Work with MIME types.
* Add image download functionality.
* Handle API failures and server overload.
* Explore Hugging Face and Grok AI.
* Build a complete real-world AI application.

---

# 📝 Homework Review

* Reviewed Assignment 3.
* Discussed improvements to previous projects.
* Transitioned from **LLM Chatbots** to **AI Image Generation**.

---

# 🖼️ What is AI Image Generation?

AI Image Generation converts a natural language prompt into an image.

Instead of predicting text tokens like an LLM, the model predicts pixels that match the prompt.

Example Prompt:

> "A majestic black dragon flying above an ancient castle during a thunderstorm, cinematic lighting, ultra realistic, 8K."

Workflow

```text
User Prompt
      ↓
Prompt Engineering
      ↓
Image Generation Model
      ↓
Binary Image
      ↓
Display in Streamlit
```

---

# 🤗 Hugging Face

Hugging Face is one of the world's largest AI communities.

It provides:

* Open-source AI models
* Datasets
* Spaces
* APIs
* Transformers Library
* Model Hub

Developers can:

* Download models
* Deploy models
* Fine-tune models
* Use hosted inference APIs

Popular Models

* Stable Diffusion
* FLUX
* Llama
* Mistral
* Whisper
* BLIP
* CLIP

---

# 🎨 Pollinations AI

Pollinations AI is a free AI Image Generation API.

Why we used it

* Free
* Beginner-friendly
* No authentication required
* Fast integration
* Simple REST API
* Perfect for Streamlit projects

Example Endpoint

```text
https://image.pollinations.ai/prompt/A%20black%20dragon
```

Additional Parameters

```text
width
height
model
seed
nologo
enhance
```

Example

```text
https://image.pollinations.ai/prompt/dragon
?width=512
&height=512
&model=flux
&seed=12345
```

---

# 🌐 REST API

REST stands for

**Representational State Transfer**

It is a standard architecture that allows applications to communicate using HTTP.

Workflow

```text
Client
      ↓
HTTP Request
      ↓
REST API
      ↓
Server
      ↓
HTTP Response
      ↓
Client
```

Examples

* Gemini API
* Pollinations AI
* Grok API
* GitHub API
* OpenWeather API

---

# 🌐 HTTP Methods

## GET

Retrieves data.

Used in our Pollinations Image API.

Example

```text
GET /prompt/dragon
```

---

## POST

Sends new data.

Example

```text
Chatbot Prompt
```

---

## PUT

Updates existing data.

---

## DELETE

Deletes existing resources.

---

# 📤 API Request

An API Request asks another server to perform a task.

Our application sends

* Prompt
* Width
* Height
* Model
* Seed

to Pollinations AI.

Workflow

```text
Streamlit
      ↓
HTTP Request
      ↓
Pollinations Server
```

---

# 📦 Parts of an API Request

## 1. URL (Endpoint)

The destination of the request.

Example

```text
https://image.pollinations.ai/prompt/dragon
```

---

## 2. Query Parameters

Extra values appended to the URL.

Example

```text
?width=512
&height=512
&model=flux
&seed=12345
```

These customize the generated image.

---

## 3. Headers

Headers contain metadata about the request.

Common Headers

```text
Authorization
Content-Type
Accept
User-Agent
```

Example

```text
Authorization:
Bearer YOUR_API_KEY
```

Pollinations usually doesn't require authentication, while Gemini and Grok do.

---

## 4. Request Body

The Body contains the main data sent to the server.

Mostly used with

* POST
* PUT

Example JSON

```json
{
  "prompt":"dragon",
  "style":"anime",
  "width":512
}
```

Since Pollinations uses GET, our project passed information through the URL instead of the request body.

---

# 📥 API Response

The server processes the request and sends a response.

A response contains

* Status Code
* Headers
* Body

---

## Response Headers

Examples

```text
Content-Type
Content-Length
Retry-After
```

---

## Response Body

Contains the returned data.

Text APIs

```json
{
   "reply":"Hello"
}
```

Image APIs

Binary Image Data

---

# 🖼️ Binary Data

Images are transferred as **bytes**, not plain text.

Workflow

```text
AI Model
      ↓
Binary Bytes
      ↓
Python
      ↓
Pillow
      ↓
Display Image
```

---

# 📄 MIME Types

MIME = **Multipurpose Internet Mail Extensions**

MIME tells the browser what type of file is being transferred.

Examples

```text
image/png
image/jpeg
image/webp
application/json
text/plain
text/html
application/pdf
```

When downloading images

```python
mime="image/png"
```

---

# 🌐 HTTP Status Codes

Common Status Codes

```text
200  OK
201  Created
400  Bad Request
401  Unauthorized
403  Forbidden
404  Not Found
429  Too Many Requests
500  Internal Server Error
```

---

# ⚠️ Server Overload (429)

If many users access the API simultaneously

```text
429
Too Many Requests
```

Possible Solutions

* Retry
* Wait
* Exponential Backoff

---

# 🔄 Retry Logic

Instead of stopping

```text
Request
     ↓
429
     ↓
Wait
     ↓
Retry
```

This improves reliability.

---

# 🎲 Seed

A seed controls randomness.

Same Prompt + Same Seed

↓

Nearly identical image

Same Prompt + Different Seed

↓

Different variation

Example

```python
seed = int(time.time()*1000)
```

---

# 📏 Resolution

Resolution means

```text
Width × Height
```

Examples

```text
512 × 512

768 × 768

1024 × 1024
```

Higher resolution generally produces more detailed images but takes longer to generate.

---

# 📷 Pillow (PIL)

Pillow is Python's image processing library.

Used to

* Open images
* Read metadata
* Check dimensions

Example

```python
img = Image.open(BytesIO(image_bytes))
```

Check size

```python
img.size
```

Returns

```text
(width,height)
```

---

# 🔗 URL Encoding

URLs cannot contain spaces directly.

We used

```python
urllib.parse.quote()
```

Example

```python
prompt = "Black Dragon"

encoded = urllib.parse.quote(prompt)
```

Output

```text
Black%20Dragon
```

---

# 🧠 Prompt Engineering

A better prompt generates a better image.

Good prompts include

* Subject
* Style
* Lighting
* Colors
* Camera Angle
* Mood
* Background
* Quality

Example

> A futuristic floating football stadium above the clouds during sunset, cinematic lighting, ultra realistic, 8K, highly detailed, award-winning digital art.

---

# 🖥️ Streamlit Components Used

## Page Configuration

```python
st.set_page_config()
```

Sets

* Title
* Icon
* Layout

---

## Sidebar

```python
st.sidebar
```

Used for

* Settings
* Art Style
* Width
* Height

---

## Select Box

```python
st.selectbox()
```

Choose

* Anime
* Cyberpunk
* Watercolor
* 3D Render
* Photorealistic

---

## Slider

```python
st.slider()
```

Controls

* Width
* Height

---

## Chat Input

```python
st.chat_input()
```

Accepts the image description.

---

## Chat Message

```python
st.chat_message()
```

Displays

* User prompt
* Generated image

---

## Spinner

```python
st.spinner()
```

Shows loading animation while waiting for the API.

---

## Download Button

```python
st.download_button()
```

Allows users to save generated images.

---

## Session State

```python
st.session_state
```

Stores

* Prompt history
* Generated images
* Gallery

Allows data to persist across Streamlit reruns.

---

# 📚 Python Libraries Used

```python
import streamlit as st
import requests
import urllib.parse
import time
from PIL import Image
from io import BytesIO
```

Purpose

| Library      | Purpose                          |
| ------------ | -------------------------------- |
| streamlit    | Build UI                         |
| requests     | Send API requests                |
| urllib.parse | Encode URLs                      |
| time         | Generate unique seeds            |
| Pillow       | Process images                   |
| BytesIO      | Convert bytes into image objects |

---

# 🌍 Real-World Applications

* AI Art Studio
* Logo Generator
* Wallpaper Generator
* Book Covers
* Marketing Posters
* Product Mockups
* Story Illustrations
* Fashion Design
* Interior Design
* Game Assets
* Architecture Concepts
* YouTube Thumbnail Generator

---

# 🔑 Grok API

We also discussed using the Grok API.

Like Gemini

* Uses an API Key
* Authenticates requests
* Returns AI responses
* Can be integrated into Python applications

Workflow

```text
Application
      ↓
API Key
      ↓
Grok API
      ↓
AI Response
```

---

# 🛠️ Project Built – The AI Image Studio

Features

* Streamlit UI
* Sidebar Configuration
* Art Style Selection
* Width Slider
* Height Slider
* Prompt Input
* Pollinations AI Integration
* REST API Communication
* URL Encoding
* Binary Image Processing
* Resolution Verification using Pillow
* Download Button
* Persistent Image Gallery using `st.session_state`
* Retry Logic
* Error Handling
* Unique Seed Generation
* Dynamic Resolution Selection

---

# ⭐ Key Takeaways

* AI image generation transforms text prompts into images using generative models.
* Hugging Face provides thousands of open-source AI models, datasets, and APIs.
* Pollinations AI is a free REST API for AI image generation.
* REST APIs communicate through HTTP requests and responses.
* API requests consist of a URL, query parameters, headers, and sometimes a request body.
* API responses include a status code, headers, and a response body.
* Binary image data must be decoded before it can be displayed.
* MIME types tell applications what type of file is being transferred.
* URL encoding ensures prompts are safe to send inside URLs.
* HTTP status codes help identify whether requests succeeded or failed.
* Retry logic and exponential backoff make applications more robust against temporary failures.
* Prompt engineering plays a major role in the quality of AI-generated images.
* `st.session_state` enables persistent galleries and stateful Streamlit applications.
* Pillow allows verification and processing of returned images.
* Building this project combined **Streamlit, REST APIs, image generation models, networking concepts, prompt engineering, error handling, and Python image processing** into one complete AI application.
