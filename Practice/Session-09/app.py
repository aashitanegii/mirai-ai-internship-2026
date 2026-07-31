import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FOOTBALL ANALYTICS")
st.write("Interactive Player Performance Dashboard")

# ---------------- SIDEBAR ----------------

st.sidebar.header("MATCH CONTROLS")

player = st.sidebar.selectbox(
    "SELECT PLAYER",
    [
        "Lionel Messi",
        "Cristiano Ronaldo",
        "Kylian Mbappe",
        "Erling Haaland"
    ]
)

minutes_played = st.sidebar.slider(
    "MINUTES PLAYED",
    min_value=1,
    max_value=90,
    value=45
)

# ---------------- PLAYER DATA ----------------

player_data = {
    "Lionel Messi": {
        "goals_rate": 0.75,
        "passes_rate": 0.72,
        "accuracy": 91
    },
    "Cristiano Ronaldo": {
        "goals_rate": 0.82,
        "passes_rate": 0.48,
        "accuracy": 86
    },
    "Kylian Mbappe": {
        "goals_rate": 0.78,
        "passes_rate": 0.55,
        "accuracy": 88
    },
    "Erling Haaland": {
        "goals_rate": 0.85,
        "passes_rate": 0.42,
        "accuracy": 84
    }
}

data = player_data[player]

# ---------------- CALCULATIONS ----------------

goals = round((minutes_played / 90) * data["goals_rate"] * 2)

passes = int(minutes_played * data["passes_rate"])

pass_accuracy = data["accuracy"]

performance_score = int(
    (goals * 20) +
    (passes * 0.5) +
    (pass_accuracy * 0.5)
)

performance_score = min(performance_score, 100)

# ---------------- LIVE STATS ----------------

st.subheader(f"📊 LIVE STATS: {player}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="GOALS",
        value=goals,
        delta="Goal Impact"
    )

with col2:
    st.metric(
        label="PASSES",
        value=passes,
        delta=f"{passes - 25} vs Average"
    )

with col3:
    st.metric(
        label="PASS ACCURACY",
        value=f"{pass_accuracy}%",
        delta=f"{pass_accuracy - 85}%"
    )

with col4:
    st.metric(
        label="PERFORMANCE SCORE",
        value=f"{performance_score}/100",
        delta="Above Average" if performance_score >= 60 else "Below Average"
    )

# ---------------- MATCH PERFORMANCE ----------------

st.divider()

st.subheader("📈 MATCH PERFORMANCE")

# NumPy generates sample performance data
np.random.seed(10)

performance_data = (
    np.random.randn(minutes_played, 1) * 3 + 8
)

# Convert NumPy data into Pandas DataFrame
chart_data = pd.DataFrame(
    performance_data,
    columns=["Performance"]
)

st.line_chart(chart_data)

# ---------------- PLAYER ACTIVITY ----------------

st.divider()

st.subheader("⚡ PLAYER ACTIVITY")

activity = np.random.randn(minutes_played, 1) * 2 + 6

activity_data = pd.DataFrame(
    activity,
    columns=["Activity Level"]
)

st.line_chart(activity_data)

# ---------------- PERFORMANCE SUMMARY ----------------

st.divider()

st.subheader("🏆 PERFORMANCE SUMMARY")

if performance_score >= 80:
    st.success(
        f"{player} is having an excellent match! 🔥"
    )

elif performance_score >= 60:
    st.info(
        f"{player} is performing above average."
    )

else:
    st.warning(
        f"{player} can improve their match performance."
    )

# ---------------- DATA TABLE ----------------

st.divider()

st.subheader("📋 PLAYER DATA")

summary_data = pd.DataFrame({
    "Metric": [
        "Minutes Played",
        "Goals",
        "Passes",
        "Pass Accuracy",
        "Performance Score"
    ],
    "Value": [
        minutes_played,
        goals,
        passes,
        f"{pass_accuracy}%",
        f"{performance_score}/100"
    ]
})

st.dataframe(summary_data, use_container_width=True)