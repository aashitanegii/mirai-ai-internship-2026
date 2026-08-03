import streamlit as st
import pandas as pd
import google.generativeai as genai
from urllib.parse import quote

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(page_title="Life-OS Wellbeing Dashboard", page_icon="📱", layout="wide")

# =========================================================
# PHASE 1: THE DATA PIPELINE
# =========================================================
@st.cache_data
def load_data():
    """Load the synthetic screen time dataset from CSV."""
    df = pd.read_csv("screentime.csv")
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df


def summarize_day_usage(day_df):
    """Aggregate the day's usage by category and convert it to a clean string."""
    if day_df.empty:
        return "No data recorded for the selected day."
    summary = (
        day_df.groupby("Category")["Minutes_Used"]
        .sum()
        .reset_index()
        .rename(columns={"Minutes_Used": "Minutes"})
    )
    return summary.to_string(index=False)


try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'screentime.csv' was not found. Please run generate_data.py first.")
    st.stop()

# =========================================================
# PHASE 2: THE COMMAND CENTER UI
# =========================================================
st.sidebar.title("⚙️ Life-OS Controls")
st.sidebar.caption("Tune your goals, inspect your habits, and get brutally honest coaching.")

available_dates = sorted(pd.unique(df["Date"]))
selected_date = st.sidebar.selectbox("Select a day to analyze", available_dates)
daily_goal_mins = st.sidebar.slider(
    "Daily Goal (minutes)",
    min_value=60,
    max_value=600,
    value=240,
    step=30,
)

selected_day_df = df[df["Date"] == selected_date]

total_mins_today = int(selected_day_df["Minutes_Used"].sum())
most_used_app = (
    selected_day_df.loc[selected_day_df["Minutes_Used"].idxmax()]["App_Name"]
    if not selected_day_df.empty
    else "No data"
)
delta_mins = total_mins_today - daily_goal_mins

st.title("📱 Life-OS Wellbeing Dashboard")
st.markdown("Monitor your digital habits, face the truth, and reclaim your time with ruthless clarity.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="⏱ Total Screen Time",
        value=f"{total_mins_today} mins",
        delta=f"{delta_mins:+d} mins vs goal",
        delta_color="inverse",
    )
with col2:
    st.metric(label="📱 Most Used App", value=most_used_app)
with col3:
    st.metric(label="🎯 Daily Goal", value=f"{daily_goal_mins} mins")

if total_mins_today <= daily_goal_mins:
    st.success("✅ Goal achieved or stayed within plan")
elif total_mins_today <= daily_goal_mins + 60:
    st.warning("⚠️ Close to the goal — a small reset would help")
else:
    st.error("🔴 Goal exceeded — the day was too screen-heavy")

st.caption(f"Selected day: {selected_date}")

trend_df = df.groupby("Date")["Minutes_Used"].sum().reset_index()
trend_df.set_index("Date", inplace=True)

chart_col, category_col = st.columns([2, 1])
with chart_col:
    st.subheader("📈 14-Day Screen Time Trend")
    st.line_chart(trend_df)

with category_col:
    st.subheader("📊 By Category")
    category_summary_df = (
        selected_day_df.groupby("Category")["Minutes_Used"]
        .sum()
        .reset_index()
        .rename(columns={"Minutes_Used": "Minutes"})
    )
    if not category_summary_df.empty:
        st.bar_chart(category_summary_df.set_index("Category"), use_container_width=True)
    else:
        st.info("No category data available for this day.")

st.subheader("📋 Today's Data")
st.dataframe(
    selected_day_df[["App_Name", "Category", "Minutes_Used"]]
    .sort_values("Minutes_Used", ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
)

# =========================================================
# PHASE 3: THE AI INTEGRATION
# =========================================================
category_summary_text = summarize_day_usage(selected_day_df)

# Load Gemini API key from Streamlit secrets.
model = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as exc:
    st.caption(f"Secret loading note: {exc}")


def fallback_coaching(total_mins, goal_mins):
    """Provide a safe offline coaching fallback if the Gemini API is unavailable."""
    if total_mins > goal_mins:
        return (
            f"You spent {total_mins} minutes on screens today, which is above your {goal_mins}-minute goal. "
            "Reclaim the next hour with a 20-minute gym block, a walk outside, meal prep for tomorrow, "
            "and ten pages of a physical book. Your body and attention need a reset, not another scroll."
        )
    return (
        f"You stayed within your {goal_mins}-minute goal, which is a strong win. Protect it by adding one offline ritual: "
        "a short walk, a stretch session, or a quiet reading block before bed. Discipline grows from repetition."
    )


def generate_ai_feedback():
    """Generate tailored coaching advice for the selected day."""
    prompt = f"""
You are a brutally honest but fair life coach and digital wellness expert.

Here is the user's screen time summary for the selected day:
{category_summary_text}

The user set a daily goal of {daily_goal_mins} minutes, and their actual usage was {total_mins_today} minutes.

Your job:
1. Analyze the categories and minutes directly and identify the unhealthy patterns.
2. Mention specific categories such as Social Media, Coding, Entertainment, Education, and Productivity, and tie them to the numbers.
3. Suggest specific offline replacements that are physical and real-world, such as a 20-minute gym session, meal prep, walking, stretching, reading a paperback, journaling, or a call with a friend.
4. Avoid generic advice like 'use your phone less.' Be specific, practical, and firm.
Keep the response concise, under three short paragraphs, and sound like a demanding but caring coach.
"""

    if model is None:
        return fallback_coaching(total_mins_today, daily_goal_mins)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return fallback_coaching(total_mins_today, daily_goal_mins)


feedback_key = f"{selected_date}_{daily_goal_mins}"
if "coach_cache" not in st.session_state:
    st.session_state.coach_cache = {}
if feedback_key not in st.session_state.coach_cache:
    st.session_state.coach_cache[feedback_key] = generate_ai_feedback()

ai_feedback = st.session_state.coach_cache[feedback_key]

coach_col, avatar_col = st.columns([2, 1])
with coach_col:
    st.subheader("🧠 AI Life Coach")
    if total_mins_today > daily_goal_mins:
        st.warning(ai_feedback)
    else:
        st.info(ai_feedback)
    st.caption("💡 Small habits repeated daily create lasting change. Today's recommendation is based on the selected day's data.")

with avatar_col:
    st.subheader("🤖 Today's Digital Reflection")
    if total_mins_today > daily_goal_mins:
        image_prompt = (
            "A lazy, exhausted zombie endlessly scrolling a glowing phone inside a dark, messy room, "
            "dramatic lighting, cinematic, 4k"
        )
    else:
        image_prompt = (
            "A disciplined warrior studying peacefully in a bright library with a calm aura, healthy habits, "
            "sunlit nature background, 4k"
        )

    encoded_prompt = quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    st.image(image_url, width=320)
