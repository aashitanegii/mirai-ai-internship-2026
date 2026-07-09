# 📒 MirAI Internship – Session 3 Notes
**Topic:** Building AI Applications with Streamlit, Secure API Integration & Networking Basics

---

# 🎯 Session Objective
In this session, we learned how to:

- Understand basic networking concepts used in AI applications.
- Secure API keys using **Environment Variables (`.env`)**.
- Connect a Streamlit application with the **Gemini API**.
- Build an AI-powered Character Chatbot.
- Follow best practices for secure AI application development.

---

# 🌐 Networking Basics
Every AI application communicates with servers using networking protocols.

## HTTP (HyperText Transfer Protocol)

- Used for transferring web pages and data.
- Communication is **not encrypted**.
- Default Port: **80**

---

## HTTPS (HyperText Transfer Protocol Secure)

- Secure version of HTTP.
- Encrypts data using SSL/TLS.
- Protects passwords, API requests, and sensitive information.
- Used by modern websites such as Google, GitHub, and banking applications.
- Default Port: **443**

---

## SMTP (Simple Mail Transfer Protocol)
SMTP is used for sending emails.

Examples:

- Gmail
- Outlook
- Email notifications

Default Port:

```text
25
```

---

## DNS (Domain Name System)
DNS converts a website name into its IP address.

Example:

```text
google.com
      ↓
142.xxx.xxx.xxx
```
Without DNS, users would need to remember IP addresses instead of domain names.

Default Port:

```text
53
```

---

# 🔐 Environment Variables (.env)
Sensitive information should never be written directly inside source code.

Instead, store it inside a **`.env`** file.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

### Benefits

- Keeps API keys secure.
- Separates secrets from source code.
- Makes projects easier to maintain.
- Prevents accidental exposure on GitHub.

---

# 📦 python-dotenv
The **python-dotenv** library loads variables from a `.env` file into Python.

Install:

```bash
pip install python-dotenv
```

Load variables:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
```

---

# 🚫 Protecting API Keys
Never upload your `.env` file to GitHub.

Add the following to `.gitignore`:

```text
.env
```

This prevents sensitive information from being pushed to your repository.

---

# 🤖 Integrating AI with Streamlit
Once the UI is built, connect it to the Gemini API.

Workflow:

```text
User
      ↓
Streamlit Interface
      ↓
User Prompt
      ↓
Gemini Client
      ↓
Gemini API
      ↓
LLM
      ↓
AI Response
      ↓
Display on Streamlit
```

---

# 🔑 Initializing the Gemini Client
Before sending prompts, initialize the AI client using your API key.

```python
from google import genai

client = genai.Client(api_key=api_key)
```

The client establishes communication between your application and the Gemini model.

---

# 📨 Sending a Prompt to Gemini
Example:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
```

The model processes the prompt and returns an AI-generated response.

---

# 🧰 Streamlit Components Used

### `st.title()`
Displays the main page heading.

```python
st.title("Character Chatbot")
```

---

### `st.write()`
Displays text, variables, tables, and other objects.

```python
st.write("Welcome!")
```

---

### `st.text_input()`
Accepts single-line user input.

```python
name = st.text_input("Enter your Name")
```

---

### `st.text_area()`
Accepts multi-line input.

Useful for:

- Long prompts
- Stories
- Paragraphs

Example:

```python
prompt = st.text_area("Enter your Prompt")
```

---

### `st.selectbox()`
Creates a dropdown menu.

Example:

```python
personality = st.selectbox(
    "Choose a Personality",
    ["Teacher", "Friend", "Motivational Coach"]
)
```

Used to allow users to choose the chatbot's personality.

---

### `st.button()`
Executes code only when clicked.

```python
if st.button("Generate"):
```

---

# 🧵 f-Strings
An **f-string** is an easy way to insert variables or expressions into a string.

Example:

```python
name = "Aashita"

print(f"Hello {name}")
```

Output:

```text
Hello Aashita
```

---

# 🛠️ Project 1 – Custom Personality Chatbot

### Objective
Build an AI chatbot that responds according to the selected personality.

### Features

- Select a personality from a dropdown.
- Enter a prompt.
- Send the prompt to Gemini.
- Generate an AI response.
- Display the response in Streamlit.

Possible personalities:

- Teacher
- Friendly Assistant
- Motivational Coach
- Pirate
- Shakespeare
- Custom Character

---

# 💡 Best Practices

- Store API keys in `.env`.
- Never hardcode API keys.
- Add `.env` to `.gitignore`.
- Build the UI before integrating AI.
- Test locally before pushing to GitHub.
- Write clear prompts for better AI responses.
- Keep your project organized with proper folders and documentation.

---

# 🌍 Real-World Applications
The concepts learned in this session can be used to build:

- AI Chatbots
- Customer Support Assistants
- AI Tutors
- Resume Review Tools
- AI Interview Coaches
- AI Content Generators
- Personal Productivity Assistants
- AI Search Applications

---

# ⭐ Key Takeaways

- AI applications communicate with cloud-hosted models through APIs.
- Environment variables (`.env`) securely store sensitive information like API keys.
- `python-dotenv` loads environment variables into Python applications.
- Never upload `.env` files to GitHub—always include them in `.gitignore`.
- **HTTP (80)** transfers web data, **HTTPS (443)** encrypts communication, **SMTP (25)** sends emails, and **DNS (53)** translates domain names into IP addresses.
- Streamlit components such as `st.selectbox()` and `st.text_area()` make applications interactive.
- A complete AI application follows the flow: **User → Streamlit → Gemini API → LLM → Response → User**.
- Session 3 prepared us to build a secure **Custom Personality Chatbot** by combining **Streamlit**, **Gemini API**, secure API management, and prompt engineering.
