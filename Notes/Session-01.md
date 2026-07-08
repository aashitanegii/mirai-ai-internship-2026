# 📒 MirAI Internship – Session 1 Notes

**Topic:** Foundations of AI, LLMs & APIs

---

# 🌍 What is Artificial Intelligence (AI)?

Artificial Intelligence is the field of creating machines that can perform tasks requiring human intelligence.

Examples:

- Chatbots
- Image generation
- Speech recognition
- Code generation
- Translation
- Recommendations

---

# 🧠 What is a Large Language Model (LLM)?

An LLM (Large Language Model) is an AI model trained on massive amounts of text to understand and generate human-like language.

Examples:

- GPT (OpenAI)
- Gemini (Google)
- Claude (Anthropic)
- Llama (Meta)

LLMs can:

- Answer questions
- Generate code
- Write emails
- Summarize documents
- Translate languages
- Brainstorm ideas

---

# 🤖 Integrating AI into Applications

Modern applications don't build AI models from scratch. Instead, they **integrate existing AI models** using APIs.

Examples:

- AI chatbot in a website
- AI-powered resume generator
- AI code assistant
- AI travel planner
- AI document summarizer

The workflow is:

```
User
   ↓
Your Application
   ↓
AI API (Gemini/OpenAI/Claude)
   ↓
AI Model
   ↓
Response
   ↓
Your Application
   ↓
User
```

This allows developers to add AI capabilities to their own projects without training an AI model.

---

# ⚙️ How an AI App Works

```
User
   ↓
Frontend (Your App)
   ↓
API Request
   ↓
LLM (Gemini/GPT/Claude)
   ↓
API Response
   ↓
Frontend
   ↓
User
```

Your application **doesn't contain the AI model**. It sends requests to an AI service through an API.

---

# 🔌 What is an API?

**API = Application Programming Interface**

An API is a bridge that allows two software applications to communicate.

Example:

Your chatbot → Gemini API → Gemini Model → Response → User

Without APIs, your app cannot interact with AI models hosted by companies like Google or OpenAI.

---

# 🔑 API Key

An API key is a unique secret key that authenticates your application when making API requests.

Purpose:

- Identifies your application
- Grants access to the AI model
- Tracks API usage
- Helps prevent unauthorized access

⚠️ Never expose your API key publicly or upload it to GitHub.

---

# 💬 Prompt

A **prompt** is the instruction or question you send to the AI.

Example:

> Explain recursion in simple terms.

The quality of the prompt directly affects the quality of the response.

---

# 🪟 Context Window

The context window is the amount of information an AI model can "remember" during a conversation.

It includes:

- Previous messages
- Instructions
- Current prompt

If the context exceeds the model's limit, older information may be forgotten.

---

# 🧩 Tokens

LLMs process **tokens**, not words.

A token can be:

- A word
- Part of a word
- A punctuation mark

Approximation:

> **1 token ≈ 4 characters (English)**

More tokens generally mean:

- Higher API usage
- Potentially higher cost

---

# 🌡️ Temperature

Temperature controls the randomness of the AI's responses.

**Low Temperature (0–0.3)**

- More accurate
- More consistent
- Better for coding and factual tasks

**High Temperature (0.8–1.0)**

- More creative
- More diverse
- Better for brainstorming and storytelling

---

# ☁️ AI Infrastructure

Most LLMs run on cloud servers.

Your application:

- Sends a request
- The cloud-hosted AI processes it
- Returns the response

You don't run the complete AI model on your own computer.

---

# 🤖 Popular LLMs

- GPT – OpenAI
- Gemini – Google
- Claude – Anthropic
- Llama – Meta

---

# 💡 Real-World Applications

- AI Chatbots
- Coding Assistants
- Customer Support Bots
- Resume Builders
- Document Summarizers
- Translation Tools
- AI Search
- Personal AI Assistants

---

# ⭐ Key Takeaways

- AI features are added to applications using **LLM APIs**, not by training your own model.
- APIs enable communication between your application and cloud-hosted AI models.
- API keys authenticate your application.
- Prompts guide the model's response.
- Tokens determine how much text the model processes and influence API costs.
- The context window defines how much information the model can use while responding.
- Temperature controls the balance between accuracy and creativity.
