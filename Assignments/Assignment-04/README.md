
# 🎨 AI Image Studio (Assignment 4)

## MirAI School of Technology
### Virtual Summer Internship 2026 – AI Builder Track

## 📌 Assignment Objective

Upgrade the AI Image Studio built during the live session into a more polished SaaS-style application by fixing existing bugs, improving the user experience, and implementing new creative features.

---

# 🚀 Features

## ✅ Task 1 – Fixed Broken Image Size Sliders

Previously, the width and height sliders existed only in the UI and did not affect the generated image.

The application now passes the selected width and height as HTTP query parameters to the Pollinations AI API.

Example:

```
?width=512&height=768
```

---

## ✅ Task 2 – Improved Image Download

Fixed the download button so images are saved with the correct `.png` extension.

Implemented dynamic filenames based on the selected art style.

Example:

```
cyberpunk_image.png
anime_manga_image.png
watercolor_image.png
```

---

## ✅ Task 3 – Magic Enhance ✨

Added a sidebar checkbox that automatically improves prompts.

When enabled, the application secretly appends professional-quality prompt keywords before sending the request.

Example additions:

- masterpiece
- 8k resolution
- highly detailed
- trending on ArtStation
- Unreal Engine 5 render

This improves image quality without requiring the user to write complex prompts.

---

## ✅ Task 4 – Surprise Me 🎲

Added a creative prompt generator.

The application randomly selects one prompt from a curated list and instantly generates an image.

Examples include:

- An astronaut riding a horse on Mars
- A cyberpunk street food vendor in Tokyo
- A floating castle above the clouds
- A giant dragon protecting a futuristic city
- A neon jungle with glowing animals

---

# ⭐ Additional Improvements

Besides the required tasks, several usability improvements were implemented.

### Persistent Gallery

Used Streamlit Session State to store previously generated images.

Users can revisit earlier generations without regenerating them.

---

### Chat-style Interface

Replaced the traditional layout with a conversational interface using:

- `st.chat_message()`
- `st.chat_input()`

This creates a cleaner AI experience.

---

### Download Previous Images

Every generated image includes its own download button, even after page interactions.

---

### Rate Limiting

Implemented a simple generation limit of **7 images**.

This prevents excessive API requests and demonstrates session management.

---

### Clear Gallery

Added a sidebar button to clear the stored image history and restart the session.

---

### Better Error Handling

Handles:

- API timeout
- Pollinations busy server (429)
- Other request failures

with user-friendly messages.

---

### Dynamic Image Seeds

A random seed is generated for every request to increase image uniqueness.

---

### Loading Indicators

Added custom loading animations using:

```
st.spinner()
```

to improve user experience while waiting for image generation.

---

# 🛠️ Technologies Used

- Python
- Streamlit
- Pollinations AI API
- Requests
- Session State
- urllib.parse
- Random
- Time

---

# 📂 Project Structure

```
Assignment-04/
│
├── app.py
├── README.md
└── requirements.txt
```

---

# ▶️ Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Run

```
streamlit run app.py
```

---

# 📚 Concepts Learned

During this assignment, I learned how to:

- Build a complete Streamlit application
- Work with REST APIs
- Send HTTP GET requests
- Pass URL query parameters
- Encode URLs using `urllib.parse.quote()`
- Generate AI images using Pollinations AI
- Store data using Streamlit Session State
- Build chat-style interfaces
- Create persistent galleries
- Implement download functionality
- Handle API errors gracefully
- Improve prompt engineering
- Generate random prompts
- Improve user experience with Streamlit components
- Implement simple rate limiting
- Organize a production-style Streamlit project

---

# 🎯 Outcome

This assignment transformed a basic AI image generator into a more polished and interactive application by fixing bugs, improving usability, and integrating Streamlit session management concepts learned during the internship.
````

---

# 📖 What I Learned (Detailed Notes)

### Streamlit

* Sidebar components (`st.sidebar`)
* Sliders
* Select boxes
* Checkboxes
* Buttons
* Chat UI (`st.chat_message`)
* Chat input (`st.chat_input`)
* Download button
* Spinner
* Session State
* `st.rerun()`
* `st.stop()`

---

### Python

* Random module
* Lists
* Conditional statements
* Exception handling
* Dictionary manipulation
* String formatting (f-strings)

---

### APIs

* HTTP GET requests
* Query parameters
* Status codes
* Timeouts
* Error handling

---

### Prompt Engineering

* Improving prompts automatically
* Art styles
* Prompt enhancement
* Better image generation through descriptive keywords

---

### Session Management

* Maintaining gallery history
* Counting generated images
* Rate limiting
* Clearing session data

---

### Software Engineering Concepts

* Debugging an existing application
* Enhancing UX
* Feature additions without breaking existing functionality
* Writing maintainable Streamlit applications
* Building beyond minimum assignment requirements

---
