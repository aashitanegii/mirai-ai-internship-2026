# ⚽ Football Analytics Dashboard

An interactive **Football Analytics Dashboard** built using **Python, Streamlit, Pandas, and NumPy** as part of **MirAI Internship – Session 9**.

The project demonstrates how user inputs can be converted into dynamic statistics, metrics, and visualizations using Streamlit.

## 📌 Project Overview

The dashboard allows users to select a football player and adjust the number of minutes played in a match.

Based on these inputs, the application dynamically calculates and displays player performance statistics.

### Dashboard Flow

```text
USER INPUT
     ↓
STREAMLIT WIDGETS
     ↓
PYTHON LOGIC
     ↓
DATA PROCESSING
     ↓
PANDAS + NUMPY
     ↓
METRICS + CHARTS
     ↓
INTERACTIVE FOOTBALL DASHBOARD
```

## ✨ Features

* ⚽ Select a football player
* ⏱️ Adjust minutes played using an interactive slider
* 📊 Display dynamically calculated match statistics
* 🎯 Track goals, passes, and pass accuracy
* 🏆 Calculate an overall performance score
* 📈 Visualize match performance using line charts
* ⚡ Display player activity throughout the match
* 📋 View a structured player statistics table
* 💬 Generate a performance summary based on the calculated score

## 🛠️ Technologies Used

* **Python** — Application logic
* **Streamlit** — Interactive dashboard and UI
* **Pandas** — DataFrames and structured data
* **NumPy** — Numerical and simulated performance data

## 🎮 Dashboard Controls

The sidebar contains two main controls:

### Select Player

```python
player = st.sidebar.selectbox(
    "SELECT PLAYER",
    [
        "Lionel Messi",
        "Cristiano Ronaldo",
        "Kylian Mbappe",
        "Erling Haaland"
    ]
)
```

### Minutes Played

```python
minutes_played = st.sidebar.slider(
    "MINUTES PLAYED",
    min_value=1,
    max_value=90,
    value=45
)
```

Changing either input automatically recalculates and updates the dashboard.

## 📊 Performance Metrics

The dashboard displays four major KPIs using `st.metric()`:

* Goals
* Passes
* Pass Accuracy
* Performance Score

Streamlit columns are used to display these metrics horizontally.

```python
col1, col2, col3, col4 = st.columns(4)
```

## 📈 Data Visualization

NumPy is used to generate sample match-performance data.

```python
performance_data = (
    np.random.randn(minutes_played, 1) * 3 + 8
)
```

The generated data is converted into a Pandas DataFrame:

```python
chart_data = pd.DataFrame(
    performance_data,
    columns=["Performance"]
)
```

It is then visualized using Streamlit:

```python
st.line_chart(chart_data)
```

> **Note:** The statistics in this project are simulated for educational purposes and do not represent real-time or official football data.

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Install dependencies

```bash
pip install streamlit pandas numpy
```

### 3. Run the Streamlit application

```bash
streamlit run app.py
```

Streamlit will launch the dashboard in your browser.

## 📚 Concepts Practiced

This project helped practice:

* Streamlit interactive widgets
* `st.selectbox()`
* `st.slider()`
* `st.columns()`
* `st.metric()`
* `st.divider()`
* `st.line_chart()`
* Dynamic Python calculations
* Pandas DataFrames
* NumPy numerical data generation
* Interactive dashboard development
* Converting raw data into understandable KPIs and visualizations

## 🎓 Internship Context

This project was created as part of **MirAI Internship – Session 9: AI Resume Optimizer + Data Dashboards with Streamlit**.

The session introduced the idea of converting data into measurable metrics and presenting those results through interactive dashboards.

The same architecture can later be extended to projects such as an **AI Resume Optimizer**, where metrics like ATS Score, Skills Match, and Keyword Match can replace the football statistics.

## 🔮 Future Improvements

Possible future upgrades include:

* Real football API integration
* Live match statistics
* More players and teams
* Player comparison
* Historical performance analysis
* Additional charts and visualizations
* AI-generated player performance insights

---

### ⚽ Built with Python + Streamlit

**MirAI Internship 2026 — Session 9**
