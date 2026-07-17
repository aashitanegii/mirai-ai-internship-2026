# 📒 MirAI Internship – Session 6 Notes

**Topic:** Building Stateful AI Chatbots, Gemini Chats API, Streamlit Session State, Caching, Chat History & Download Functionality

---

# 🎯 Session Objective

In this session, we learned how to:

* Build a **real conversational AI chatbot** using the Gemini Chats API.
* Understand the difference between **normal response generation** and **persistent chat sessions**.
* Store conversations using **Streamlit Session State**.
* Cache expensive objects like AI clients.
* Maintain chat history across reruns.
* Export the complete conversation as a text file.
* Understand why session management is important in AI applications.

---

# 📝 Homework Review

* Reviewed previous chatbot assignment.
* Discussed improvements to the chatbot UI.
* Learned how to make conversations persistent instead of restarting every message.

---

# 🤖 Gemini Chats API

Instead of calling:

```python
client.models.generate_content()
```

we learned to use:

```python
client.chats.create()
```

This creates a **persistent chat session** where Gemini automatically remembers previous messages.

Workflow:

```text
User
   ↓
Gemini Chat Session
   ↓
Conversation Context
   ↓
AI Response
```

Unlike normal generation, the chat session keeps context throughout the conversation.

---

# 💾 Caching Resources

We learned about:

```python
@st.cache_resource
```

Example:

```python
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=API_KEY)
```

### Why use caching?

Without caching:

* New Gemini client created every rerun.
* Slower performance.
* More unnecessary API initialization.

With caching:

* Client is created once.
* Faster application.
* Efficient resource usage.

---

# 🧠 Session State

We used:

```python
st.session_state
```

to store information that survives Streamlit reruns.

Example:

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

We stored:

* Chat history
* Gemini chat object

---

# 💬 Maintaining Chat History

Every message is stored as a dictionary.

Example:

```python
{
    "role":"user",
    "content":"Hello"
}
```

These dictionaries are stored inside a list.

---

# 🔄 Iterating Through Messages

We learned how to redraw the conversation using a loop.

Example:

```python
for msg in st.session_state.messages:
```

Inside the loop:

```python
st.chat_message(msg["role"])
```

This recreates the full chat every time the page reruns.

---

# 💬 Streamlit Chat Components

## Chat Input

```python
st.chat_input()
```

Provides a modern chat interface for user messages.

---

## Chat Message

```python
st.chat_message()
```

Displays messages with roles like:

* User
* Assistant

---

## Spinner

```python
st.spinner()
```

Displays a loading animation while Gemini generates a response.

---

# 📥 Download Chat Functionality

We built a feature that lets users save the conversation.

Using:

```python
st.download_button()
```

The chat history is converted into a text file.

Example:

```python
chat_history.txt
```

---

# 🔄 Building the Chat Transcript

We used a loop to combine every message.

Example:

```python
chat_text = ""

for msg in st.session_state.messages:
    chat_text += f"{msg['role']}: {msg['content']}\n\n"
```

This demonstrates:

* Iteration
* String concatenation
* Dynamic text generation

---

# 🚦 Rate Limiting (Practice)

We discussed implementing a simple message limit.

Example:

Maximum:

```text
7 user messages
```

On the next message:

```text
⚠️ Token limit reached.
Currently we are rate limited.
Please try again later.
```

Possible implementation:

```python
user_count = sum(
    1 for msg in st.session_state.messages
    if msg["role"] == "user"
)

if user_count >= 7:
    st.warning("⚠️ Token limit reached. Please try again later.")
    st.stop()
```

This simulates real AI services that have usage limits.

---

# 🌐 Real-World Application Example

Many AI applications use persistent chat history, including:

* ChatGPT
* Gemini
* Claude
* Microsoft Copilot
* Customer support chatbots
* AI tutors
* Virtual assistants

They all rely on maintaining conversation context.

---

# ⚙️ MLOps (Machine Learning Operations)

We were introduced to **MLOps**, which is the practice of managing machine learning systems in production.

It includes:

* Model deployment
* Version control
* Monitoring
* Continuous training
* Automation
* Scaling AI applications

MLOps is similar to DevOps but focuses on AI and machine learning workflows.

---

# 🧩 Importance of Context

Context helps AI understand previous messages.

Without context:

```text
User:
My name is Ash.

Later:
What's my name?

AI:
I don't know.
```

With context:

```text
AI:
Your name is Ash.
```

Maintaining context creates natural conversations.

---

# 🌐 Sessions in Web Development

A **session** stores user-specific information while they interact with an application.

Examples:

* Logged-in user
* Shopping cart
* Chat history
* User preferences

In Streamlit, this is handled using:

```python
st.session_state
```

---

# 🔒 Session Security

We discussed why session data should be handled carefully.

Good practices:

* Don't store API keys in session state.
* Keep sensitive information secure.
* Use environment variables (`.env`) for secrets.
* Avoid exposing private user data.

---

# 📊 Data Consistency

Maintaining chat history ensures the application's state remains consistent.

Benefits:

* No lost messages
* Reliable conversations
* Better user experience

---

# 🛠️ Project Built

## 💬 Gemini Stateful Chatbot

### Features

* Gemini 2.5 Flash Chat API
* Persistent chat session
* Session State
* Chat history
* Cached AI client
* Loading spinner
* Download chat as `.txt`
* Message iteration using loops
* Modern chat interface
* Rate limiter concept

---

# 🌍 Real-World Uses

This architecture can be used to build:

* AI Customer Support
* Personal AI Assistant
* AI Study Buddy
* AI Interview Coach
* Mental Wellness Chatbot
* AI Coding Assistant
* Company Help Desk
* Internal Knowledge Assistant

---

# ⭐ Key Takeaways

* `client.chats.create()` creates a persistent AI conversation.
* `@st.cache_resource` improves performance by caching expensive resources.
* `st.session_state` stores data across Streamlit reruns.
* Chat history is maintained using lists of dictionaries.
* `for` loops can iterate through chat history to redraw conversations and create downloadable transcripts.
* `st.chat_input()` and `st.chat_message()` provide a clean chat interface.
* `st.download_button()` allows users to export conversations.
* Context is essential for intelligent AI interactions.
* Sessions help maintain user-specific data in web applications.
* Rate limiting is commonly used in production AI systems to manage usage fairly.
* MLOps focuses on deploying, monitoring, and maintaining machine learning applications at scale.

---
