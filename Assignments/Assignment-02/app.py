import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Streamlit Page
# -----------------------------
st.set_page_config(
    page_title="Football Legends AI Arena",
    page_icon="⚽",
    layout="centered"
)

# -----------------------------
# Football Theme CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
background:linear-gradient(180deg,#0B6623,#228B22);
}

.main{
padding-top:20px;
}

.title{
text-align:center;
color:white;
font-size:45px;
font-weight:bold;
}

.subtitle{
text-align:center;
color:white;
font-size:20px;
margin-bottom:20px;
}

.card{
background:rgba(255,255,255,0.12);
padding:20px;
border-radius:15px;
border:2px solid white;
}

.footer{
text-align:center;
color:white;
font-size:14px;
margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Heading
# -----------------------------
st.markdown(
    "<h1 class='title'>⚽ Football Legends AI Arena</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Choose your football legend and chat with them using AI!</p>",
    unsafe_allow_html=True
)

# -----------------------------
# Player Personalities
# -----------------------------
player_prompts = {

"🇵🇹 Cristiano Ronaldo":
"""
You are Cristiano Ronaldo.

Speak confidently.

Motivate people.

Talk about discipline,
hard work,
winning,
consistency.

Never mention you are an AI.

Keep answers below 120 words.
""",

"🇦🇷 Lionel Messi":
"""
You are Lionel Messi.

Speak humbly.

Talk about teamwork.

Be calm and respectful.

Never mention you are an AI.

Keep answers below 120 words.
""",

"🇸🇪 Zlatan Ibrahimović":
"""
You are Zlatan Ibrahimović.

Speak with extreme confidence.

Be funny and arrogant.

Refer to yourself as Zlatan.

Never mention you are an AI.

Keep answers below 120 words.
""",

"🇧🇷 Ronaldinho":
"""
You are Ronaldinho.

Be cheerful.

Love football.

Talk about creativity and happiness.

Never mention you are an AI.

Keep answers below 120 words.
""",

"🇧🇷 Neymar Jr":
"""
You are Neymar Jr.

Be stylish.

Be playful.

Talk about entertaining football.

Never mention you are an AI.

Keep answers below 120 words.
""",

"🇫🇷 Thierry Henry":
"""
You are Thierry Henry.

Be intelligent.

Talk tactically.

Explain football in a smart way.

Never mention you are an AI.

Keep answers below 120 words.
"""
}

# -----------------------------
# Player Info
# -----------------------------
player_info = {

"🇵🇹 Cristiano Ronaldo":"🐐 Discipline • Hard Work • Confidence",

"🇦🇷 Lionel Messi":"⚽ Humility • Teamwork • Vision",

"🇸🇪 Zlatan Ibrahimović":"🔥 Swagger • Confidence • Fearless",

"🇧🇷 Ronaldinho":"😄 Joy • Skills • Creativity",

"🇧🇷 Neymar Jr":"🎨 Flair • Style • Entertainment",

"🇫🇷 Thierry Henry":"🧠 Tactical • Intelligent • Calm"

}

# -----------------------------
# UI
# -----------------------------
player = st.selectbox(
    "🏆 Pick Your Football Legend",
    list(player_prompts.keys())
)

st.info(player_info[player])

question = st.text_area(
    "💬 Ask Your Question",
    placeholder="Example: What advice would you give a young footballer?"
)

# -----------------------------
# Button
# -----------------------------
if st.button("⚽ Start Match"):

    if question.strip()=="":

        st.warning("Please enter a question.")

    else:

        final_prompt = f"""
{player_prompts[player]}

User Question:

{question}
"""

        with st.spinner(f"{player} is thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )

        st.divider()

        st.subheader(f"🎤 {player} says")

        st.success(response.text)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
"""
<div class='footer'>
⚽ Built using Streamlit + Google Gemini API<br>
MirAI School of Technology Internship 2026
</div>
""",
unsafe_allow_html=True
)