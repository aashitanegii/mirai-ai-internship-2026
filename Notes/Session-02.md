# 📒 MirAI Internship – Session 2 Notes

**Topic:** Streamlit, LLM APIs & Building AI Applications

---

# 🎯 Session Objective
Learn how to:

- Build AI web applications using **Streamlit**
- Connect an application with an **LLM API**
- Understand how AI generates responses
- Reduce hallucinations using **RAG**
- Build interactive interfaces entirely with Python

---

# 🌐 What is Streamlit?
**Streamlit** is an open-source Python framework that lets developers build interactive web applications using only Python.

No need for:

- HTML
- CSS
- JavaScript
Used for:

- AI Applications
- Machine Learning Apps
- Dashboards
- Data Science Projects
- Rapid Prototyping

---

# 🚀 Why Streamlit?
Traditional Web Development

```
HTML
+
CSS
+
JavaScript
+
Backend
```
Using Streamlit

```
Python
      ↓
Streamlit
      ↓
Interactive Web App
```
Much faster for AI developers.

---

# 📦 Installation
Install Streamlit

```
pip install streamlit
```
Check installation

```
streamlit --version
```

---

# ▶️ Running a Streamlit App

```
streamlit run app.py
```
Starts a local server.

Example

```
http://localhost:8501
```
Whenever the file is saved, Streamlit automatically refreshes the webpage.

---

# 🌐 What is a Port?
A **port** is a communication endpoint through which applications communicate.

Example:

```
http://localhost:8501
```

- localhost → Your computer
- 8501 → Port number
Every web application runs on a port.

Streamlit uses **8501** by default.

---

# 📁 Basic Project Structure

```
project/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 📥 Import Streamlit

```
import streamlit as st
```
Every Streamlit component starts with

```
st.
```

---

# 🏷️ Title

```
st.title("My AI App")
```
Creates the page heading.

---

# 📝 Display Text

```
st.write("Welcome")
```
Can display

- Text
- Numbers
- Variables
- Lists
- Tables
- DataFrames

---

# ✍️ User Input

```
name = st.text_input("Enter your Name")
```
Returns a string entered by the user.

---

# 🔘 Button

```
st.button("Submit")
```
Usually written as

```
if st.button("Submit"):
```
The code inside executes only when the button is clicked.

---

# 🔀 Conditional Statements

```
if name == "":
    ...
elif message == "":
    ...
else:
    ...
```
Used to validate user input.

---

# 🚨 User Feedback Widgets

### Error

```
st.error("Please enter your name")
```

---

### Warning

```
st.warning("Please enter a message")
```

---

### Success

```
st.success("Submitted Successfully")
```

---

### Information

```
st.info("Estimated Tokens")
```

---

# 🧵 f-Strings
Insert variables into text.

```
name = "Aashita"

st.success(f"Hello {name}")
```

---

# 📏 len()
Returns the number of characters.

```
len(message)
```

---

# 🪙 Token Estimation
Approximation

```
1 Token ≈ 4 Characters
```
Formula

```
token_count = len(message) / 4
```
Display

```
st.info(f"Estimated Tokens: {token_count:.2f}")
```

---

# 🤖 What is RAG?
**RAG = Retrieval-Augmented Generation**

Instead of answering directly from its training data, the LLM first retrieves relevant information from an external source and then generates the response.

Workflow

```
User Question
      ↓
Retriever
(Searches Database/PDF/Documents)
      ↓
Relevant Context
      ↓
LLM
      ↓
Answer
```

---

## Benefits of RAG

- More accurate responses
- Current information
- Less hallucination
- Better for company documents
- Better for PDFs
- Better for knowledge bases

---

# 🎭 What is Hallucination?
A hallucination occurs when an AI confidently generates information that is false or unsupported.

Example

> AI invents a fake research paper or citation.

---

# 🧮 Why do LLMs Hallucinate? (Mathematical View)
LLMs are **next-token prediction models**.

They don't search for truth.

They calculate

[
P(\text{Next Token} \mid \text{Previous Tokens})
]

and choose the token with the highest probability.

Example

```
Input

"The capital of France is"

Predictions

Paris → 99.2%

London → 0.4%

Berlin → 0.2%

Rome → 0.2%
```
The model simply picks the highest probability.

If it lacks knowledge or context, it may still confidently generate an incorrect answer.

---

# 💡 How RAG Reduces Hallucination
Without RAG

```
Question
     ↓
LLM
     ↓
May Guess
```
With RAG

```
Question
     ↓
Retriever
     ↓
Relevant Documents
     ↓
LLM
     ↓
Evidence-Based Answer
```

---

# 🔑 Initializing an AI Client
Before using an LLM, we initialize a client using an API key.

Example

```
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
```
The client connects your application to Google's AI service.

---

# 📨 Sending a Prompt
Example

```
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain recursion in simple terms."
)

print(response.text)
```
Flow

```
Prompt
      ↓
API
      ↓
LLM
      ↓
Generated Response
```

---

# 🪝 Hooks
Hooks are pieces of code that execute automatically before or after a specific event.

Examples

- Logging
- Validation
- Monitoring
- Modifying requests

---

# 🏗️ AI Application Flow

```
User
      ↓
Streamlit UI
      ↓
User enters prompt
      ↓
API Client
(API Key)
      ↓
Gemini API
      ↓
LLM
      ↓
Response
      ↓
Display in Streamlit
```

---

# 📚 Streamlit Widgets Learned

- `st.title()`
- `st.write()`
- `st.text_input()`
- `st.button()`
- `st.error()`
- `st.warning()`
- `st.success()`
- `st.info()`

---

# 📝 Assignment 1 – Identity Echo Interface
Requirements

- Create a title
- Add instructions
- Collect Name
- Collect Message
- Add **Transmit** button
- Validate empty inputs
- Display Error/Warning
- Display personalized Success message
- **Bonus:** Estimate token count

---

# 💡 Real-World Applications

- AI Chatbots
- PDF Summarizers
- Resume Builders
- AI Search Engines
- Customer Support Bots
- AI Coding Assistants
- RAG Applications
- Personal AI Assistants

---

# ⭐ Key Takeaways

- Streamlit allows you to build web applications entirely with Python.
- Every Streamlit application starts from **`app.py`**.
- User interaction is created using widgets like `st.text_input()` and `st.button()`.
- Input validation improves user experience.
- AI applications communicate with LLMs through APIs.
- An API client must be initialized with an API key before sending requests.
- Prompts are sent to the model, which returns generated responses.
- LLMs generate text by predicting the most probable next token—they do **not** inherently verify facts.
- **Hallucinations** occur because of probabilistic next-token prediction, especially when context is insufficient.
- **RAG (Retrieval-Augmented Generation)** improves accuracy by retrieving relevant information before generation.
- Streamlit uses **port 8501** by default to serve local web applications.
- Streamlit is an excellent framework for rapidly building AI-powered applications and prototypes without needing traditional frontend technologies.
