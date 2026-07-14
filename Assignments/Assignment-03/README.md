# Assignment 3 — The Memory Vault (Stateful Chatbot)

**MirAI School of Technology — Virtual Summer Internship 2026: AI Builder Track**

## Project: Football Legends AI Multiverse

An upgrade of the Assignment 2 chatbot from a **stateless** app (forgets everything on every rerun) to a **stateful** app that remembers full conversation history using Streamlit's `st.session_state`.

---

## What This Assignment Was About

Streamlit reruns the entire script top-to-bottom on every interaction (button click, dropdown change, chat input). Without a persistence mechanism, that means every previous message gets wiped the moment a new one is sent. This assignment's goal was to fix that using Streamlit's built-in "Memory Vault" — `st.session_state` — and to replace the old text box + button UI with Streamlit's native chat components.

---

## What We Learned

- **`st.session_state` is Streamlit's only way to persist data across reruns.** Any variable not stored in it resets every single time the script executes.
- **Initialization must be guarded.** Using `if "messages" not in st.session_state:` prevents the chat history from being wiped back to `[]` on every rerun — it only initializes once per session.
- **The walrus operator (`:=`)** lets you assign and check a value in one line, which is exactly what `st.chat_input()` needs: `if user_message := st.chat_input(...)`.
- **`st.chat_message()`** is purpose-built for chat UIs — it handles role-based styling (user vs. assistant) and supports custom avatars, which is much cleaner than manually formatting text with `st.write()`.
- **Widgets outside `session_state` (like sidebar dropdowns) don't affect stored data.** Changing the personality or player selector triggers a rerun, but since chat history lives in `session_state`, it survives untouched — this is what proves the app is genuinely stateful.
- **Streaming responses (`generate_content_stream`)** taught us how to update the UI incrementally using `st.empty()` as a placeholder, instead of waiting for the full API response before rendering anything.
- **Error handling matters for API calls.** Wrapping the Gemini call in `try/except` prevents the whole app from crashing if the API key is invalid or a request fails.
- **Less is more.** Adding too many experimental features (multi-agent debates, extra API calls for trivia, toast notifications) increases the risk of bugs right before a submission deadline. A few reliable, well-tested features demonstrate mastery better than many flashy, untested ones.

---

## Core Requirements Implemented

| Task | Implementation |
|---|---|
| **Task 1: Initialize Memory Vault** | `if "messages" not in st.session_state: st.session_state.messages = []` |
| **Task 2: Render Chat History** | `for message in st.session_state.messages:` loop with `st.chat_message()` |
| **Task 3: Upgrade Input UI** | Replaced `st.text_area()` + `st.button()` with `st.chat_input()` |
| **Task 4: Save New Messages** | `st.session_state.messages.append({"role": ..., "content": ...})` after both the user message and the AI response |

---

## Additional Features Added

- **🎙️ Match Commentary Mode** — A sidebar toggle that dynamically changes the prompt sent to Gemini, making the selected legend respond like a live match commentator. Demonstrates conditional prompt engineering based on widget state.
- **📥 Download Conversation** — Exports the full chat transcript as a `.txt` file using `st.download_button()`.
- **🎭 Custom Avatars** — Each football legend has a unique emoji avatar shown in `st.chat_message(role, avatar=...)`.
- **🗑️ Clear Chat Button** — Resets `st.session_state.messages` back to an empty list and calls `st.rerun()`, demonstrating that session state can be manipulated, not just read.
- **⌨️ Typewriter/Streaming Effect** — Uses `generate_content_stream()` with `st.empty()` to render the AI's response incrementally, word by word.

---

## Tech Stack

- **Streamlit** — UI framework and state management
- **Google Gemini API** (`google-genai`) — LLM responses
- **python-dotenv** — Secure API key management via `.env`

---

## Folder Structure

```
Assignment-03-Memory-Vault/
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Add your Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

---

## Demo Flow (Screen Recording)

1. Select a football legend from the sidebar.
2. Send Message 1 → receive AI response.
3. Send Message 2 → receive AI response.
4. Send Message 3 → receive AI response.
5. Toggle Match Commentary Mode.
6. Change the sidebar personality dropdown.
7. Confirm all previous messages are still visible (proves `session_state` persistence).
8. Click Clear Chat → confirm history resets.
9. Download the conversation transcript.