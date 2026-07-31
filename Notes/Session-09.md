# 📒 MirAI Internship – Session 9 Notes

**Session:** AI Resume Optimizer + Data Dashboards with Streamlit

## 1. AI Resume Optimizer

We learned the concept of building an **AI Resume Optimizer**—an application that analyzes a resume and provides useful feedback instead of simply generating resume content.

Basic workflow:

```text
Resume
   ↓
Extract Resume Information
   ↓
Analyze Resume
   ↓
Calculate ATS Score
   ↓
Generate Feedback
   ↓
Improve Resume
```

An AI Resume Optimizer can analyze:

* Skills
* Keywords
* Experience
* Projects
* Education
* Resume formatting
* Relevance to a particular job description
* Overall ATS compatibility

The idea is to turn AI-generated analysis into **structured and measurable information** that can be presented to the user.

---

## 2. ATS — Applicant Tracking System

**ATS stands for Applicant Tracking System.**

Companies use ATS software to manage and filter job applications.

An ATS may examine information such as:

```text
Resume
   ↓
Skills
Keywords
Education
Experience
Job Titles
Projects
Formatting
Job Relevance
```

This means that having relevant information and keywords in a resume can affect how effectively it is processed by an ATS.

---

## 3. Building an ATS Scoring System

We learned how a resume-analysis application could assign scores to different parts of a resume.

Example:

```text
Skills Match       → Score
Keyword Match      → Score
Experience         → Score
Projects           → Score
Formatting         → Score
                      ↓
                Overall Score
```

The important programming idea is that raw information can be converted into **metrics**, making results easier for users to understand.

An AI system could first analyze the resume and then the application could display those results through a dashboard.

---

# 4. Creating Data Dashboards with Streamlit

A major practical topic was building **interactive dashboards using Streamlit**.

A dashboard generally follows:

```text
User Controls
      ↓
Input Values
      ↓
Python Logic
      ↓
Data Processing
      ↓
Metrics + Charts
      ↓
Interactive Dashboard
```

We used a **Sports Analytics dashboard** as the practical example.

The same concepts could later be applied to the AI Resume Optimizer.

---

# 5. Sports Analytics Dashboard

We created/worked through a Streamlit dashboard that displayed sports statistics.

The dashboard contained a sidebar with controls such as:

* Player selection
* Overs played

The main page then displayed live calculated statistics such as:

```text
SPORTS ANALYTICS

LIVE STATS: Virat Kohli

TOTAL RUNS            STR
42                    142

Above Average         -2
```

The important idea was that the displayed data was **dynamic**.

When the input changed, Python recalculated the values and Streamlit automatically updated the dashboard.

---

# 6. Interactive Dashboard Controls

We learned how Streamlit widgets can control dashboard data.

### `st.selectbox()`

Used to allow the user to select an option.

Example:

```python
player = st.selectbox(
    "SELECT PLAYER",
    ["Virat Kohli", "Rohit Sharma"]
)
```

The selected value can then be used elsewhere:

```python
st.subheader(f"LIVE STATS: {player}")
```

So the flow becomes:

```text
Select Player
      ↓
player variable
      ↓
Python calculations
      ↓
Updated dashboard
```

---

### `st.slider()`

A slider allows the user to select a numerical value.

For example:

```python
match_phase = st.slider("OVERS PLAYED")
```

The value can then directly affect calculations:

```python
runs = match_phase * 7
```

Therefore, moving the slider changes the dashboard results.

---

# 7. Streamlit Columns

We learned how to organize dashboard elements horizontally using:

```python
st.columns()
```

Example:

```python
col1, col2 = st.columns(2)
```

Then components can be placed inside each column:

```python
with col1:
    ...

with col2:
    ...
```

Result:

```text
┌──────────────────┬──────────────────┐
│    TOTAL RUNS    │       STR        │
│        42        │       142        │
└──────────────────┴──────────────────┘
```

This is especially useful for dashboards because multiple KPIs can be displayed together instead of stacking everything vertically.

---

# 8. `st.metric()` — Displaying Important Data

One of the main Streamlit components learned was:

```python
st.metric()
```

`st.metric()` is useful for displaying **KPIs or important numerical information**.

Example from the sports dashboard:

```python
runs = match_phase * 7

st.metric(
    label="TOTAL RUNS",
    value=runs,
    delta="Above Average"
)
```

The metric contains three useful pieces of information:

```text
Label  → What the number represents
Value  → Current value
Delta  → Change/comparison/context
```

---

# 9. Calculating Dynamic Metrics

Instead of hardcoding values, dashboard metrics can be calculated using user input.

Example:

```python
runs = match_phase * 7
```

Another calculation demonstrated was:

```python
strike_rate = 130 + (match_phase * 2)
```

Then:

```python
st.metric(
    label="STR",
    value=strike_rate,
    delta="-2"
)
```

So:

```text
User changes slider
        ↓
match_phase changes
        ↓
Calculation runs again
        ↓
Metric changes
```

This is the core principle behind an interactive dashboard.

---

# 10. Understanding `delta` in `st.metric()`

The `delta` parameter gives additional context about a metric.

Example:

```python
st.metric(
    label="TOTAL RUNS",
    value=runs,
    delta="Above Average"
)
```

A numerical delta can also be shown:

```python
st.metric(
    label="STR",
    value=strike_rate,
    delta="-2"
)
```

We also saw:

```python
delta_color="inverse"
```

This allows the normal positive/negative color interpretation to be reversed when necessary.

This is useful when **a decrease is actually desirable** for a particular metric.

---

# 11. Creating Sections with Streamlit

We used:

```python
st.divider()
```

to visually separate different dashboard sections.

For example:

```python
st.divider()
st.subheader("RUN RATE")
```

This improves dashboard organization and makes the UI easier to read.

---

# 12. Introduction to Pandas

We were introduced to **Pandas**, one of Python's main libraries for working with structured data.

Standard import:

```python
import pandas as pd
```

Pandas is commonly used for:

* Data manipulation
* Data analysis
* Tabular data
* Cleaning datasets
* Organizing information
* Preparing data for visualization

One of the most important Pandas objects is the:

```text
DataFrame
```

A DataFrame organizes information into **rows and columns**, similar to an Excel spreadsheet.

---

# 13. Introduction to NumPy

We also learned about **NumPy**.

Standard import:

```python
import numpy as np
```

NumPy is primarily used for numerical computing.

It can be used for:

* Arrays
* Mathematical calculations
* Numerical operations
* Random number generation
* Simulations
* Data processing

Pandas and NumPy are often used together.

```text
NumPy
   ↓
Numerical Data
   ↓
Pandas
   ↓
Structured DataFrame
   ↓
Analysis / Visualization
```

---

# 14. Generating Sample Data with NumPy

In the dashboard, NumPy was used to generate numerical data.

Example:

```python
np.random.randn(match_phase, 1)
```

`np.random.randn()` generates random numerical values.

The session then modified those values:

```python
np.random.randn(match_phase, 1) * 3 + 8
```

This created sample data that could represent values such as **runs per over**.

This was useful for learning visualization without needing a real external dataset yet.

---

# 15. Creating a Pandas DataFrame

The generated NumPy data was converted into a DataFrame:

```python
chart_data = pd.DataFrame(
    np.random.randn(match_phase, 1) * 3 + 8,
    columns=["Runs PER OVER"]
)
```

Breaking it down:

```python
np.random.randn(match_phase, 1)
```

→ generates numerical data.

```python
* 3 + 8
```

→ modifies/scales the generated values.

```python
pd.DataFrame(...)
```

→ converts the values into structured tabular data.

```python
columns=["Runs PER OVER"]
```

→ assigns a meaningful column name.

---

# 16. Data Visualization with `st.line_chart()`

After creating the DataFrame, we displayed it as a chart using:

```python
st.line_chart(chart_data)
```

This showed how easily Streamlit can convert structured data into a visual dashboard.

Complete pipeline:

```text
NumPy
   ↓
Generate Data
   ↓
Pandas
   ↓
Create DataFrame
   ↓
Streamlit
   ↓
st.line_chart()
   ↓
Data Visualization
```

---

# 17. Connecting User Input to Data Visualization

The most useful concept from the practical dashboard was connecting **UI → calculations → data → visualization**.

For example:

```text
Overs Played Slider
        ↓
match_phase
        ↓
Runs Calculation
        ↓
NumPy Data Generation
       ↙ ↘
st.metric()  Pandas DataFrame
                 ↓
           st.line_chart()
```

This means a dashboard isn't simply displaying information—it can respond to the user and regenerate its analysis dynamically.

---

# 18. Streamlit Components Learned

Important Streamlit components covered:

```python
st.selectbox()    # Dropdown/select input

st.slider()       # Numerical interactive input

st.subheader()    # Section heading

st.columns()      # Horizontal dashboard layout

st.metric()       # KPI/statistic display

st.divider()      # Visual section separator

st.line_chart()   # Data visualization
```

Data libraries:

```python
import pandas as pd
import numpy as np
```

---

# 19. Applying the Dashboard Concept to the AI Resume Optimizer

The sports dashboard was useful because the exact same architecture can be adapted for the resume project.

For example:

```text
                 RESUME
                    ↓
               AI Analysis
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
     Skills      Keywords   Experience
        ↓           ↓           ↓
      Score       Score       Score
        └───────────┼───────────┘
                    ↓
              Overall Score
                    ↓
          Streamlit Dashboard
              ↙           ↘
          Metrics         Charts
```

Instead of showing:

```text
Runs | Strike Rate
```

a resume dashboard could show:

```text
ATS Score | Keyword Match | Skills Match
```

This is the bigger engineering lesson: **the dashboard components stay similar while the underlying data and use case change.**

---

# 20. Session 9 — What We Learned

By the end of this session, we had moved beyond simply displaying AI-generated text and learned how to create **data-driven interactive applications**.

The major concepts learned were:

* Understanding the idea behind an AI Resume Optimizer
* Understanding ATS and ATS-style resume scoring
* Converting information into measurable scores and KPIs
* Creating interactive dashboards with Streamlit
* Using sidebar controls to manipulate application data
* Dynamically updating dashboard values
* Using `st.columns()` to design dashboard layouts
* Using `st.metric()` to display KPIs
* Understanding metric values, deltas, and `delta_color`
* Separating dashboard sections with `st.divider()`
* Introduction to Pandas
* Understanding Pandas DataFrames
* Introduction to NumPy
* Generating sample numerical data with NumPy
* Converting NumPy-generated data into a DataFrame
* Visualizing DataFrames using `st.line_chart()`
* Connecting user input → Python logic → metrics → charts
* Understanding how these dashboard concepts can later be combined with AI-generated analysis

### Core learning pipeline

```text
USER INPUT
     ↓
STREAMLIT WIDGETS
     ↓
PYTHON LOGIC
     ↓
DATA PROCESSING
     ↓
PANDAS / NUMPY
     ↓
METRICS + CHARTS
     ↓
INTERACTIVE DASHBOARD
```

And when AI is added:

```text
USER / DATA
     ↓
AI ANALYSIS
     ↓
STRUCTURED RESULTS
     ↓
PYTHON DATA PROCESSING
     ↓
STREAMLIT DASHBOARD
     ↓
METRICS + VISUALIZATIONS
```

That was the central progression of Session 9: **from building AI features to building interfaces that can analyze, quantify, and visually communicate data.**
