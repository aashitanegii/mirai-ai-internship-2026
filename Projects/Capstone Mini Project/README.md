# 📖 AI Visual Novel Engine

An interactive **AI-powered Choose Your Own Adventure** game built as the **Capstone Mini Project** for the **AI Builder Track** at **MirAI School of Technology – Virtual Summer Internship 2026**.

The application combines **Gemini 2.5 Flash**, **Pollinations AI**, **Google Text-to-Speech**, and **Streamlit** to generate a fully interactive, stateful visual novel where every choice changes the story.

---

## 🚀 Features

### 🧠 AI Storytelling
- Powered by **Google Gemini 2.5 Flash**
- Dynamic branching story generation
- Stateful conversations using Streamlit Session State

### 📄 Structured JSON Engine
Gemini returns responses as structured JSON containing:
- Story narration
- AI image prompt
- Three interactive choices
- Inventory updates

The application parses this JSON to dynamically build the game interface.

### 🎨 AI Scene Generation
- Generates artwork using the **Pollinations AI API**
- Every scene receives a unique AI-generated illustration
- Images can be downloaded directly from the app

### 🔊 Voice Narration
- Converts every story scene into speech using **Google Text-to-Speech (gTTS)**
- Narration plays directly inside the browser

### 🎮 Dynamic Gameplay
- Genre selection
- Art style selection
- Difficulty selection
- Story pacing options
- Inventory system
- Restart game functionality

### 🛡️ Error Handling
Gracefully handles API failures using:
- `try...except`
- `st.toast()`
- Status indicators
- Safe JSON parsing

---

# 🏗️ Tech Stack

- Python
- Streamlit
- Google Gemini 2.5 Flash API
- Pollinations AI Image API
- Google Text-to-Speech (gTTS)
- Requests
- JSON

---

# 📂 Project Structure

```
AI-Visual-Novel-Engine/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd AI-Visual-Novel-Engine
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a folder named

```
.streamlit
```

Inside it, create

```
secrets.toml
```

Add your Gemini API key

```toml
GEMINI_API_KEY="YOUR_API_KEY"
```

Run the application

```bash
streamlit run app.py
```

---

# 🎮 How to Play

1. Launch the application.
2. Select your preferred:
   - Genre
   - Art Style
   - Difficulty
   - Story Pacing
3. Click **Start New Game**.
4. Read or listen to the generated story.
5. Choose one of the dynamically generated actions.
6. Continue your adventure as the story evolves.

---

# 📸 Project Highlights

✔️ Stateful AI conversations

✔️ Dynamic JSON parsing

✔️ AI-generated artwork

✔️ Voice narration

✔️ Interactive branching gameplay

✔️ Inventory tracking

✔️ Download scene artwork

✔️ Graceful API error handling

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Prompt Engineering
- Structured JSON Outputs
- REST API Integration
- Streamlit Session State
- Dynamic UI Generation
- AI Image Generation
- Text-to-Speech Integration
- Exception Handling
- Building Multi-Modal AI Applications

---

# 🎓 Internship

This project was developed as the **Capstone Mini Project** for the **AI Builder Track** under the **Virtual Summer Internship 2026** conducted by **MirAI School of Technology**.

---

# 📄 License

This project is intended for educational and portfolio purposes.

---
