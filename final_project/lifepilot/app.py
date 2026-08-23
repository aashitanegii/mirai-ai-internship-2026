"""LifePilot Phase 1 dashboard foundation."""

from datetime import date, datetime
from pathlib import Path
import sys

import pandas as pd

# Streamlit may execute this entry point from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.ai_engine import extract_tasks, extract_tasks_from_audio, extract_tasks_from_image
from modules.analytics import (
    completed_tasks,
    completion_percentage,
    high_priority_count,
    overdue_task_count,
    scheduled_hours,
    scheduled_vs_unscheduled_minutes,
    total_planned_hours,
    total_tasks,
    workload_by_category,
    workload_by_priority,
)
from modules.constraints import (
    calculate_available_minutes,
    calculate_scheduled_minutes,
    calculate_total_task_minutes,
    has_overload,
)
from modules.scheduler import generate_daily_plan, replan_day
from modules.task_parser import TASK_COLUMNS, TaskParseError

import streamlit as st


st.set_page_config(
    page_title="LifePilot",
    page_icon="LP",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg: #f4f6f3;
            --surface: #ffffff;
            --surface-elevated: #fbfcfa;
            --border: #dfe5df;
            --text: #17221c;
            --muted: #68756d;
            --accent: #267a61;
            --accent-soft: #e4f1eb;
            --success: #21815e;
            --warning: #b87520;
            --danger: #b34d4d;
            --shadow: 0 12px 32px rgba(23, 34, 28, 0.06);
        }
        .stApp { background: var(--bg); color: var(--text); font-family: Georgia, 'Times New Roman', serif; }
        [data-testid="stHeader"] { background: rgba(244, 246, 243, 0.9); }
        [data-testid="stSidebar"] { background: #18231e; border-right: 1px solid #2b3a32; }
        [data-testid="stSidebar"] * { color: #eef5ef; }
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p, [data-testid="stSidebar"] .stCaption { color: #aab9af; }
        [data-testid="stSidebar"] .stButton > button { background: var(--accent); border: 1px solid var(--accent); color: white; }
        [data-testid="stSidebar"] .stButton > button:hover { background: #349373; border-color: #349373; color: white; }
        .side-nav { display: grid; gap: 0.18rem; margin: 0.7rem 0 1.2rem; }
        .side-nav a { border-radius: 6px; color: #c8d7cd !important; display: block; font: 700 0.72rem 'Trebuchet MS', sans-serif; letter-spacing: 0.08em; padding: 0.55rem 0.65rem; text-decoration: none; text-transform: uppercase; }
        .side-nav a:hover { background: #26372e; color: #ffffff !important; }
        [id="overview"], [id="capture"], [id="plan"], [id="adapt"], [id="reflect"] { scroll-margin-top: 5rem; }
        h1, h2, h3, h4 { color: var(--text); letter-spacing: 0; font-family: Georgia, 'Times New Roman', serif; }
        h1 { font-size: clamp(2.2rem, 5vw, 4.5rem); line-height: 0.98; margin: 0; max-width: 10ch; }
        h2 { font-size: 1.55rem; margin: 0; }
        .eyebrow { color: var(--accent); font-family: 'Trebuchet MS', sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.55rem; }
        .subtitle { color: var(--muted); font-family: 'Trebuchet MS', sans-serif; font-size: 0.98rem; line-height: 1.55; margin: 0.6rem 0 0; max-width: 58ch; }
        .hero { 
            align-items: start; 
            background: url("https://images.unsplash.com/photo-1506744626753-f327718029d2?q=80&w=2940&auto=format&fit=crop") center/cover no-repeat; 
            border: 1px solid var(--border); 
            border-radius: 14px; 
            display: flex; 
            justify-content: space-between; 
            min-height: 320px; 
            padding: 2.5rem 3rem; 
            margin: 1.2rem 0 1.4rem; 
            box-shadow: var(--shadow); 
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(90deg, rgba(255,255,255,1) 30%, rgba(255,255,255,0.85) 50%, rgba(255,255,255,0) 100%);
            z-index: 1;
        }
        .hero > div {
            position: relative;
            z-index: 2;
        }
        .hero-status { color: var(--success); font: 700 0.68rem 'Trebuchet MS', sans-serif; letter-spacing: 0.12em; text-transform: uppercase; white-space: nowrap; }
        .hero-date { color: var(--muted); font: 0.8rem 'Trebuchet MS', sans-serif; margin-top: 0.55rem; text-align: right; }
        .hero-state { background: rgba(255, 255, 255, 0.72); border: 1px solid rgba(38, 122, 97, 0.16); border-radius: 10px; margin-top: 1.1rem; min-width: 245px; padding: 1rem 1.1rem; }
        .hero-state-label { color: var(--muted); font: 700 0.65rem 'Trebuchet MS', sans-serif; letter-spacing: 0.13em; text-transform: uppercase; }
        .hero-state-value { color: var(--accent); font: 700 1.45rem Georgia, 'Times New Roman', serif; margin: 0.22rem 0 0.45rem; }
        .hero-state-meta { color: var(--text); font: 0.76rem 'Trebuchet MS', sans-serif; }
        .capacity-track { background: #dbe9df; border-radius: 99px; height: 6px; margin-top: 0.8rem; overflow: hidden; }
        .capacity-fill { background: var(--accent); border-radius: inherit; height: 100%; }
        .section-heading { align-items: center; display: flex; gap: 0.7rem; margin: 2.3rem 0 0.55rem; }
        .section-heading h2 { margin: 0; }
        .section-mark { background: var(--accent); border-radius: 99px; height: 1.6rem; width: 0.28rem; }
        [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; min-height: 105px; padding: 1rem 1.1rem; box-shadow: 0 5px 18px rgba(23, 34, 28, 0.035); }
        [data-testid="stMetricLabel"] { color: var(--muted); }
        [data-testid="stMetricValue"] { color: var(--text); font-family: Georgia, 'Times New Roman', serif; }
        .mission { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 10px; min-height: 120px; padding: 1.05rem 1.2rem; position: relative; box-shadow: 0 5px 18px rgba(23, 34, 28, 0.035); transition: transform 160ms ease, box-shadow 160ms ease; }
        .mission:hover { box-shadow: 0 10px 24px rgba(23, 34, 28, 0.09); transform: translateY(-2px); }
        .mission-title { color: var(--accent); font: 700 0.82rem 'Trebuchet MS', sans-serif; letter-spacing: 0.05em; margin-bottom: 0.35rem; }
        .mission-copy { color: var(--text); font-family: 'Trebuchet MS', sans-serif; line-height: 1.45; margin: 0; }
        .intelligence { background: linear-gradient(120deg, #f5f0fb, #fffaf0); border: 1px solid #dfd3ec; border-radius: 10px; color: #76551d; padding: 1rem 1.25rem; }
        div[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem 1.3rem 0.7rem; box-shadow: 0 5px 18px rgba(23, 34, 28, 0.025); }
        .stButton > button, .stFormSubmitButton > button { border-radius: 6px; font-weight: 600; min-height: 2.55rem; }
        .stFormSubmitButton > button { background: var(--text); border-color: var(--text); color: white; }
        .stFormSubmitButton > button:hover { background: var(--accent); border-color: var(--accent); color: white; }
        [data-testid="stDataEditor"] { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
        [data-testid="stExpander"] { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; }
        [data-testid="stRadio"] label p, [data-testid="stSelectbox"] label p, [data-testid="stTextArea"] label p { font-family: 'Trebuchet MS', sans-serif; }
        [data-testid="stMain"] [data-testid="stRadio"] [role="radio"] { color: #314239; font-weight: 700; }
        textarea, input { color: var(--text) !important; }
        @media (max-width: 720px) { .hero { align-items: start; flex-direction: column; gap: 1.5rem; min-height: auto; padding: 1.5rem; } .hero-date { text-align: left; } }
    </style>
    """,
    unsafe_allow_html=True,
)


if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=TASK_COLUMNS)
if "schedule" not in st.session_state:
    st.session_state.schedule = []
if "schedule_df" not in st.session_state:
    st.session_state.schedule_df = pd.DataFrame(
        columns=["Start", "End", "Task", "Priority", "Reason"]
    )
if "deferred_tasks" not in st.session_state:
    st.session_state.deferred_tasks = []
if "schedule_summary" not in st.session_state:
    st.session_state.schedule_summary = ""
if "replan_history" not in st.session_state:
    st.session_state.replan_history = []
if "last_replan_old_schedule" not in st.session_state:
    st.session_state.last_replan_old_schedule = pd.DataFrame(
        columns=["Start", "End", "Task", "Priority", "Reason"]
    )
if "replan_changes" not in st.session_state:
    st.session_state.replan_changes = []
if "change_log" not in st.session_state:
    st.session_state.change_log = []
if "last_extracted_tasks" not in st.session_state:
    st.session_state.last_extracted_tasks = pd.DataFrame(columns=TASK_COLUMNS)
if "last_extraction_start" not in st.session_state:
    st.session_state.last_extraction_start = None
if "schedule_stale" not in st.session_state:
    st.session_state.schedule_stale = False
if "planning_preference" not in st.session_state:
    st.session_state.planning_preference = "Protect deadlines"


def add_task(task_data: dict) -> None:
    new_task = pd.DataFrame([task_data], columns=TASK_COLUMNS)
    st.session_state.tasks_df = pd.concat(
        [st.session_state.tasks_df, new_task], ignore_index=True
    )
    st.session_state.change_log.append(
        {"action": "task_added", "task": task_data["Task"]}
    )


def merge_extracted_tasks(extracted_tasks: pd.DataFrame, success_message: str) -> None:
    """Append validated extraction results without replacing existing tasks."""
    if extracted_tasks.empty:
        st.info("LifePilot could not find any actionable tasks in that brain dump.")
        st.session_state.last_extracted_tasks = extracted_tasks
        st.session_state.last_extraction_start = None
        return

    extraction_start = len(st.session_state.tasks_df)
    st.session_state.tasks_df = pd.concat(
        [st.session_state.tasks_df, extracted_tasks], ignore_index=True
    )
    st.session_state.last_extracted_tasks = extracted_tasks
    st.session_state.last_extraction_start = extraction_start
    st.session_state.change_log.append(
        {"action": "tasks_extracted", "count": len(extracted_tasks)}
    )
    st.success(success_message.format(count=len(extracted_tasks)))


def load_demo_day() -> None:
    """Load an explicit, local-only scenario for evaluation and screenshots."""
    clear_day_state()
    st.session_state.tasks_df = pd.DataFrame(
        [
            {"Task": "Finish DAA assignment", "Duration_Min": 90, "Priority": "High", "Deadline": date.today(), "Category": "Academic", "Status": "Not Started"},
            {"Task": "Study OS", "Duration_Min": 120, "Priority": "Medium", "Deadline": date.today(), "Category": "Academic", "Status": "Not Started"},
            {"Task": "Work on internship project", "Duration_Min": 90, "Priority": "High", "Deadline": "", "Category": "Work", "Status": "Completed"},
            {"Task": "Reply to professor", "Duration_Min": 15, "Priority": "High", "Deadline": date.today(), "Category": "Academic", "Status": "Completed"},
            {"Task": "Go to the gym", "Duration_Min": 45, "Priority": "Low", "Deadline": "", "Category": "Health", "Status": "Completed"},
            {"Task": "Prepare Friday presentation", "Duration_Min": 60, "Priority": "Medium", "Deadline": "", "Category": "Academic", "Status": "Not Started"},
        ],
        columns=TASK_COLUMNS,
    )


def clear_day_state() -> None:
    """Clear day-level data while preserving the user's planning controls."""
    st.session_state.schedule_df = pd.DataFrame(columns=["Start", "End", "Task", "Priority", "Reason"])
    st.session_state.schedule = []
    st.session_state.deferred_tasks = []
    st.session_state.schedule_summary = ""
    st.session_state.last_extracted_tasks = pd.DataFrame(columns=TASK_COLUMNS)
    st.session_state.last_replan_old_schedule = pd.DataFrame(columns=["Start", "End", "Task", "Priority", "Reason"])
    st.session_state.replan_changes = []
    st.session_state.schedule_stale = False


def clear_demo_day() -> None:
    clear_day_state()
    st.session_state.tasks_df = pd.DataFrame(columns=TASK_COLUMNS)


with st.sidebar:
    st.markdown("## ✦ LifePilot")
    st.caption("AI Personal Decision Engine")
    st.divider()
    st.markdown("**OVERVIEW**")
    st.markdown(
        """
        <nav class="side-nav" aria-label="LifePilot workspaces">
            <a href="#overview">⌂ Overview</a>
            <a href="#capture">✦ Capture</a>
            <a href="#plan">◈ Plan</a>
            <a href="#execute">⚡ Execute</a>
            <a href="#adapt">↻ Adapt</a>
            <a href="#reflect">◫ Reflect</a>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("#### Planning controls")
    available_hours = st.slider(
        "Available Hours Today", min_value=1.0, max_value=16.0, value=8.0, step=0.5
    )
    energy_level = st.select_slider(
        "Energy Level",
        options=["Low", "Steady", "High"],
        value="Steady",
    )
    planning_preference = st.selectbox(
        "Planning Preference",
        ["Protect deadlines", "Match energy", "Balance workload"],
        key="planning_preference",
    )
    st.caption("This preference is included in scheduling decisions.")
    st.markdown("**DEMO MODE**")
    demo_columns = st.columns(2)
    load_demo = demo_columns[0].button("Load Demo Day", width="stretch")
    clear_demo = demo_columns[1].button("Clear Demo", width="stretch")
    if load_demo:
        load_demo_day()
        st.rerun()
    if clear_demo:
        clear_demo_day()
        st.rerun()
    st.write("")
    generate_plan = st.button("Generate My Plan", width="stretch")
    if generate_plan:
        if st.session_state.tasks_df.empty:
            st.warning("Add tasks first, then LifePilot can build your plan.")
        else:
            with st.spinner("LifePilot is balancing your priorities..."):
                try:
                    plan = generate_daily_plan(
                        st.session_state.tasks_df,
                        available_hours,
                        energy_level,
                        planning_preference,
                        datetime.now().time(),
                        date.today(),
                    )
                    st.session_state.schedule_df = pd.DataFrame(
                        plan["schedule"],
                        columns=["Start", "End", "Task", "Priority", "Reason"],
                    )
                    st.session_state.deferred_tasks = plan["deferred_tasks"]
                    st.session_state.schedule_summary = plan["summary"]
                    st.session_state.schedule = plan["schedule"]
                    st.session_state.schedule_stale = False
                    st.session_state.change_log.append(
                        {"action": "plan_generated", "count": len(plan["schedule"])}
                    )
                    st.success("Today's plan is ready.")
                except (TaskParseError, RuntimeError) as exc:
                    st.error(str(exc))
                except Exception:
                    st.error("LifePilot could not generate a plan right now. Please try again.")


tasks_df = st.session_state.tasks_df
total_task_minutes = calculate_total_task_minutes(tasks_df)
available_minutes = calculate_available_minutes(available_hours)
scheduled_minutes = calculate_scheduled_minutes(st.session_state.schedule_df)
completed_count = completed_tasks(tasks_df)
high_priority_total = high_priority_count(tasks_df)
planned_hours = total_planned_hours(tasks_df)
scheduled_hours_value = scheduled_hours(st.session_state.schedule_df)
completion_rate = completion_percentage(tasks_df)
capacity_delta = planned_hours - available_hours
capacity_percent = min(100, max(0, int(round((planned_hours / available_hours) * 100)))) if available_hours else 0
if not tasks_df.empty and capacity_percent >= 100:
    state_label = "OVERLOADED"
elif not tasks_df.empty and capacity_percent >= 90:
    state_label = "AT RISK"
elif not tasks_df.empty and capacity_percent >= 75:
    state_label = "BUSY"
elif not st.session_state.schedule_df.empty:
    state_label = "ON TRACK"
else:
    state_label = "STEADY"

st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="hero">
        <div>
            <div style="font-weight: 700; color: #17221c; font-family: 'Trebuchet MS', sans-serif; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                Good morning, Aashita <span style="font-size: 1.1rem;">👋</span>
            </div>
            <h1 style="color: #17221c; margin-bottom: 0.5rem; line-height: 1.1;">Your day,<br><span style="color: var(--accent);">intelligently<br>navigated.</span></h1>
            <p class="subtitle" style="max-width: 42ch; margin-top: 1rem; color: #404a44;">
                LifePilot turns scattered thoughts, deadlines, and interruptions into a realistic plan — and adapts with you.
            </p>
        </div>
        <div>
            <div class="hero-status">● System ready</div>
            <div class="hero-date">Today · {date.today().strftime("%b %d, %Y")}</div>
            <div class="hero-state">
                <div class="hero-state-label">Today's state</div>
                <div class="hero-state-value">{state_label}</div>
                <div class="hero-state-meta">{total_tasks(tasks_df)} tasks · {planned_hours:.1f}h planned · {high_priority_total} high priority</div>
                <div class="capacity-track"><div class="capacity-fill" style="width: {capacity_percent}%"></div></div>
                <div class="hero-state-meta">Capacity {capacity_percent}%</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="eyebrow">COMMAND CENTER</div>', unsafe_allow_html=True)
kpi_columns = st.columns(4)
kpi_columns[0].metric("TOTAL TASKS", total_tasks(tasks_df))
kpi_columns[1].metric("HIGH PRIORITY", high_priority_total)
kpi_columns[2].metric("COMPLETION", f"{completion_rate:.0f}%", delta=f"{completed_count} completed")
kpi_columns[3].metric(
    "PLANNED HOURS", f"{planned_hours:.1f} h",
    delta=f"{-capacity_delta:.1f} h buffer" if capacity_delta <= 0 else f"+{capacity_delta:.1f} h over",
    delta_color="normal" if capacity_delta <= 0 else "inverse",
)


st.markdown(
    """
    <style>
    .workflow-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 2rem 0; }
    .workflow-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; gap: 0.5rem; text-decoration: none !important; color: inherit !important; transition: transform 0.2s, box-shadow 0.2s; }
    .workflow-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.06); }
    .wf-header { display: flex; align-items: center; gap: 0.5rem; }
    .wf-number { font-size: 0.7rem; font-weight: 700; background: var(--bg); padding: 0.2rem 0.5rem; border-radius: 99px; }
    .wf-title { font-size: 0.75rem; font-weight: 700; font-family: 'Trebuchet MS', sans-serif; letter-spacing: 0.05em; }
    .wf-icon { font-size: 1.8rem; margin: 0.5rem 0; }
    .wf-heading { font-weight: 700; font-family: 'Trebuchet MS', sans-serif; font-size: 0.95rem; line-height: 1.2; margin-bottom: 0.25rem; }
    .wf-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.4; flex-grow: 1; }
    .wf-action { font-size: 0.8rem; font-weight: 700; display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }
    
    .wf-c1 .wf-number { color: #166534; background: #dcfce7; } .wf-c1 .wf-title, .wf-c1 .wf-icon, .wf-c1 .wf-action { color: #166534; }
    .wf-c2 .wf-number { color: #9a3412; background: #ffedd5; } .wf-c2 .wf-title, .wf-c2 .wf-icon, .wf-c2 .wf-action { color: #9a3412; }
    .wf-c3 .wf-number { color: #5b21b6; background: #ede9fe; } .wf-c3 .wf-title, .wf-c3 .wf-icon, .wf-c3 .wf-action { color: #5b21b6; }
    .wf-c4 .wf-number { color: #1e40af; background: #dbeafe; } .wf-c4 .wf-title, .wf-c4 .wf-icon, .wf-c4 .wf-action { color: #1e40af; }
    .wf-c5 .wf-number { color: #0f766e; background: #ccfbf1; } .wf-c5 .wf-title, .wf-c5 .wf-icon, .wf-c5 .wf-action { color: #0f766e; }
    
    @media (max-width: 1024px) { .workflow-grid { grid-template-columns: repeat(3, 1fr); } }
    @media (max-width: 640px) { .workflow-grid { grid-template-columns: 1fr; } }
    </style>
    
    <div class="workflow-grid">
        <a href="#capture" class="workflow-card wf-c1">
            <div class="wf-header"><span class="wf-number">01</span><span class="wf-title">CAPTURE</span></div>
            <div class="wf-icon">💬</div>
            <div class="wf-heading">Get it out of your head</div>
            <div class="wf-desc">Text, voice, or camera. LifePilot turns messy input into structured tasks.</div>
            <div class="wf-action"><span>Start Capturing</span> <span>→</span></div>
        </a>
        <a href="#plan" class="workflow-card wf-c2">
            <div class="wf-header"><span class="wf-number">02</span><span class="wf-title">PLAN</span></div>
            <div class="wf-icon">📅</div>
            <div class="wf-heading">Create your mission</div>
            <div class="wf-desc">AI plans your day around deadlines, energy, and available time.</div>
            <div class="wf-action"><span>View My Plan</span> <span>→</span></div>
        </a>
        <a href="#execute" class="workflow-card wf-c3">
            <div class="wf-header"><span class="wf-number">03</span><span class="wf-title">EXECUTE</span></div>
            <div class="wf-icon">⚡</div>
            <div class="wf-heading">Focus on what matters</div>
            <div class="wf-desc">See what to do now, next, and later. Update progress as you go.</div>
            <div class="wf-action"><span>Open Execute</span> <span>→</span></div>
        </a>
        <a href="#adapt" class="workflow-card wf-c4">
            <div class="wf-header"><span class="wf-number">04</span><span class="wf-title">ADAPT</span></div>
            <div class="wf-icon">🔄</div>
            <div class="wf-heading">When life happens</div>
            <div class="wf-desc">Replan instantly when things change. Stay on track without starting over.</div>
            <div class="wf-action"><span>Replan My Day</span> <span>→</span></div>
        </a>
        <a href="#reflect" class="workflow-card wf-c5">
            <div class="wf-header"><span class="wf-number">05</span><span class="wf-title">REFLECT</span></div>
            <div class="wf-icon">📊</div>
            <div class="wf-heading">Learn & improve</div>
            <div class="wf-desc">See what got done, what remains, and how you can improve tomorrow.</div>
            <div class="wf-action"><span>View Insights</span> <span>→</span></div>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown('<div id="capture"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="eyebrow">01 / CAPTURE</div><div class="section-heading"><span class="section-mark"></span><h2>Get it out of your head.</h2></div>',
    unsafe_allow_html=True,
)
st.caption("Text, voice, or camera. LifePilot turns messy input into structured tasks.")
input_mode = st.radio(
    "Brain dump mode",
    ["Text Brain Dump", "Voice Brain Dump", "Visual Brain Dump"],
    horizontal=True,
)
if input_mode == "Text Brain Dump":
    with st.form("brain_dump_form"):
        brain_dump = st.text_area(
            "Brain dump",
            height=150,
            label_visibility="collapsed",
            placeholder=(
                "I need to finish my DAA assignment tomorrow, study OS for two hours, "
                "work on my internship project, go to the gym, reply to my professor, "
                "and prepare for Friday's presentation."
            ),
        )
        brain_dump_submitted = st.form_submit_button("✨ Extract Tasks", width="stretch")

    if brain_dump_submitted:
        if not brain_dump.strip():
            st.warning("Add a few thoughts to your brain dump before extracting tasks.")
        else:
            try:
                extracted_tasks = extract_tasks(
                    brain_dump.strip(),
                    available_hours=available_hours,
                    energy_level=energy_level,
                    existing_tasks=st.session_state.tasks_df.to_dict("records"),
                )
                merge_extracted_tasks(extracted_tasks, "✨ LifePilot found {count} tasks")
            except (TaskParseError, RuntimeError) as exc:
                st.error(str(exc))
            except Exception:
                st.error("LifePilot could not reach Gemini right now. Please try again.")
elif input_mode == "Voice Brain Dump":
    if not hasattr(st, "audio_input"):
        st.error("Voice input is unavailable in this Streamlit version. Please use text input.")
    else:
        with st.form("voice_brain_dump_form"):
            recording = st.audio_input("Record a quick brain dump")
            voice_submitted = st.form_submit_button(
                "Extract Tasks from Voice", width="stretch"
            )

        if not recording:
            st.info("Record a quick brain dump to turn your thoughts into tasks.")
        if voice_submitted:
            if not recording:
                st.warning("Record a quick brain dump before extracting tasks.")
            else:
                try:
                    with st.spinner("LifePilot is listening..."):
                        extracted_tasks = extract_tasks_from_audio(
                            recording.getvalue(),
                            recording.type or "audio/wav",
                            available_hours=available_hours,
                            energy_level=energy_level,
                            existing_tasks=st.session_state.tasks_df.to_dict("records"),
                        )
                    merge_extracted_tasks(
                        extracted_tasks,
                        "Voice brain dump converted into {count} tasks.",
                    )
                except (TaskParseError, RuntimeError):
                    st.error("Couldn't process that recording. Try again or use text input.")
                except Exception:
                    st.error("Couldn't process that recording. Try again or use text input.")
else:
    if not hasattr(st, "camera_input"):
        st.error("Camera input is unavailable in this Streamlit version. Please use text input.")
    else:
        with st.form("visual_brain_dump_form"):
            image = st.camera_input("Photograph a to-do list, whiteboard, or notebook page")
            image_submitted = st.form_submit_button(
                "Extract Tasks from Image", width="stretch"
            )

        if not image:
            st.info("Take a photo of a task list to turn it into structured tasks.")
        if image_submitted:
            if not image:
                st.warning("Add an image before extracting tasks.")
            else:
                try:
                    with st.spinner("LifePilot is reading your task list..."):
                        extracted_tasks = extract_tasks_from_image(
                            image.getvalue(),
                            image.type or "image/jpeg",
                            available_hours=available_hours,
                            energy_level=energy_level,
                            existing_tasks=st.session_state.tasks_df.to_dict("records"),
                        )
                    merge_extracted_tasks(
                        extracted_tasks,
                        "Visual brain dump converted into {count} tasks.",
                    )
                except (TaskParseError, RuntimeError):
                    st.error("Couldn't process that image. Try again or use text input.")
                except Exception:
                    st.error("Couldn't process that image. Try again or use text input.")

if not st.session_state.last_extracted_tasks.empty:
    with st.expander("How LifePilot interpreted your brain dump", expanded=True):
        st.write(
            "LifePilot separated the actions you mentioned, estimated durations where needed, "
            "and normalized priorities, deadlines, categories, and statuses."
        )
    st.data_editor(
        st.session_state.last_extracted_tasks,
        key="extracted_task_editor",
        hide_index=True,
        width="stretch",
        disabled=["Task"],
        column_config={
            "Duration_Min": st.column_config.NumberColumn("Duration (min)", min_value=1),
            "Priority": st.column_config.SelectboxColumn(
                "Priority", options=["Low", "Medium", "High"]
            ),
            "Category": st.column_config.SelectboxColumn(
                "Category", options=["Academic", "Work", "Personal", "Health", "Errands", "Other"]
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status", options=["Not Started", "In Progress", "Completed"]
            ),
        },
    )


st.markdown(
    '<div class="eyebrow">CAPTURE / QUICK ADD</div><div class="section-heading"><span class="section-mark"></span><h2>Quick Add Task</h2></div>',
    unsafe_allow_html=True,
)
with st.form("quick_add_task", clear_on_submit=True):
    first_row = st.columns([2.5, 1, 1, 1.4])
    task_name = first_row[0].text_input("Task name", placeholder="What needs doing?")
    duration = first_row[1].number_input(
        "Duration (min)", min_value=1, max_value=1440, value=30, step=5
    )
    priority = first_row[2].selectbox("Priority", ["Low", "Medium", "High"], index=1)
    deadline = first_row[3].date_input("Deadline", value=date.today())

    second_row = st.columns([1.4, 1.4, 2.1])
    category = second_row[0].selectbox(
        "Category", ["Academic", "Work", "Personal", "Health", "Errands", "Other"]
    )
    status = second_row[1].selectbox("Status", ["Not Started", "In Progress", "Completed"])
    submitted = second_row[2].form_submit_button("Add Task", width="stretch")

if submitted:
    cleaned_name = task_name.strip()
    if not cleaned_name:
        st.error("Enter a task name before adding it.")
    elif duration <= 0:
        st.error("Duration must be greater than zero minutes.")
    else:
        add_task(
            {
                "Task": cleaned_name,
                "Duration_Min": int(duration),
                "Priority": priority,
                "Deadline": deadline,
                "Category": category,
                "Status": status,
            }
        )
        st.success(f'Added "{cleaned_name}" to your task list.')


if has_overload(total_task_minutes, available_hours):
    st.warning(f"Your workload exceeds today's capacity by {(total_task_minutes - available_minutes) / 60:.1f} hours.")
else:
    st.success(f"Plan fits your available time with {(available_minutes - total_task_minutes) / 60:.1f} hours to spare.")


st.markdown('<div id="execute"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="eyebrow">03 / EXECUTE</div><div class="section-heading"><span class="section-mark"></span><h2>Task Control Center</h2></div>',
    unsafe_allow_html=True,
)
if tasks_df.empty:
    st.info("No tasks yet. Add your first task above to start shaping today's plan.")
else:
    def update_task_status(idx, new_status):
        st.session_state.tasks_df.at[idx, "Status"] = new_status
        if not st.session_state.schedule_df.empty:
            st.session_state.schedule_stale = True
        st.session_state.change_log.append({"action": "status_updated"})
        st.rerun()

    # Determine Current, Next, Later based on schedule order if available, else tasks_df order
    if not st.session_state.schedule_df.empty:
        # Map scheduled tasks back to original tasks_df index by matching Task name
        # We'll prioritize tasks that are scheduled and not completed.
        scheduled_tasks = st.session_state.schedule_df["Task"].tolist()
        ordered_indices = []
        for t_name in scheduled_tasks:
            matches = tasks_df[(tasks_df["Task"] == t_name) & (tasks_df["Status"] != "Completed")].index.tolist()
            for m in matches:
                if m not in ordered_indices:
                    ordered_indices.append(m)
        # Add remaining non-completed tasks
        remaining_indices = tasks_df[~tasks_df.index.isin(ordered_indices) & (tasks_df["Status"] != "Completed")].index.tolist()
        active_indices = ordered_indices + remaining_indices
    else:
        active_indices = tasks_df[tasks_df["Status"] != "Completed"].index.tolist()

    in_progress = tasks_df[tasks_df["Status"] == "In Progress"].index.tolist()
    
    current_idx = None
    if in_progress:
        current_idx = in_progress[0]
    elif active_indices:
        current_idx = active_indices[0]

    st.markdown('<div class="eyebrow" style="margin-top: 1.5rem;">CURRENT</div>', unsafe_allow_html=True)
    if current_idx is not None:
        task = tasks_df.loc[current_idx]
        with st.container(border=True):
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"**{task['Task']}**")
                st.caption(f"{task['Duration_Min']} min · {task['Priority'].upper()} PRIORITY")
            with cols[1]:
                status = st.selectbox(
                    "Status",
                    options=["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress", "Completed"].index(task["Status"]),
                    key=f"status_{current_idx}",
                    label_visibility="collapsed"
                )
                if status != task["Status"]:
                    update_task_status(current_idx, status)
    else:
        st.success("All tasks completed for now! Great job.")

    st.markdown('<div class="eyebrow" style="margin-top: 1.5rem;">NEXT</div>', unsafe_allow_html=True)
    next_indices = [idx for idx in active_indices if idx != current_idx][:3]
    if next_indices:
        for idx in next_indices:
            task = tasks_df.loc[idx]
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{task['Task']}**")
                    st.caption(f"{task['Duration_Min']} min · {task['Priority'].upper()} PRIORITY")
                with cols[1]:
                    status = st.selectbox(
                        "Status",
                        options=["Not Started", "In Progress", "Completed"],
                        index=["Not Started", "In Progress", "Completed"].index(task["Status"]),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    if status != task["Status"]:
                        update_task_status(idx, status)
    else:
        st.caption("No upcoming tasks.")

    st.markdown('<div class="eyebrow" style="margin-top: 1.5rem;">LATER</div>', unsafe_allow_html=True)
    later_indices = [idx for idx in active_indices if idx != current_idx and idx not in next_indices]
    if later_indices:
        for idx in later_indices:
            task = tasks_df.loc[idx]
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{task['Task']}**")
                    st.caption(f"{task['Duration_Min']} min")
                with cols[1]:
                    status = st.selectbox(
                        "Status",
                        options=["Not Started", "In Progress", "Completed"],
                        index=["Not Started", "In Progress", "Completed"].index(task["Status"]),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    if status != task["Status"]:
                        update_task_status(idx, status)
    else:
        st.caption("No remaining active tasks.")

    with st.expander("Full Task Editor (Edit task details)"):
        tasks_for_editor = tasks_df.copy()
        tasks_for_editor["Deadline"] = pd.to_datetime(
            tasks_for_editor["Deadline"], errors="coerce"
        ).dt.date
        edited_tasks = st.data_editor(
            tasks_for_editor,
            key="task_editor",
            hide_index=True,
            width="stretch",
            num_rows="dynamic",
            column_config={
                "Task": st.column_config.TextColumn("Task", required=True),
                "Duration_Min": st.column_config.NumberColumn(
                    "Duration (min)", min_value=1, step=5, required=True
                ),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority", options=["Low", "Medium", "High"], required=True
                ),
                "Deadline": st.column_config.DateColumn("Deadline", format="YYYY-MM-DD"),
                "Category": st.column_config.SelectboxColumn(
                    "Category", options=["Academic", "Work", "Personal", "Health", "Errands", "Other"]
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=["Not Started", "In Progress", "Completed"], required=True
                ),
            },
        )
        if not edited_tasks.equals(st.session_state.tasks_df):
            st.session_state.tasks_df = edited_tasks
            if not st.session_state.schedule_df.empty:
                st.session_state.schedule_stale = True
            st.session_state.change_log.append({"action": "tasks_edited"})
            st.rerun()

if st.session_state.schedule_stale:
    st.warning("Your task list changed. Regenerate the plan to reflect the update.")


st.markdown('<div id="reflect"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="eyebrow">05 / REFLECT</div><div class="section-heading"><span class="section-mark"></span><h2>Your LifeLoad</h2></div>',
    unsafe_allow_html=True,
)
analytics_columns = st.columns(4)
analytics_columns[0].metric("Total Tasks", total_tasks(tasks_df))
analytics_columns[1].metric("Completed", completed_count)
analytics_columns[2].metric("Completion Rate", f"{completion_percentage(tasks_df):.0f}%")
analytics_columns[3].metric("Planned Hours", f"{planned_hours:.1f} h")

category_column, priority_column = st.columns(2)
with category_column:
    st.markdown("#### Workload by Category")
    category_data = workload_by_category(tasks_df).set_index("Category")
    if category_data.empty:
        st.info("Add tasks to see category workload.")
    else:
        st.bar_chart(category_data, y="Minutes", color="#0d9488")
with priority_column:
    st.markdown("#### Priority Breakdown")
    priority_data = workload_by_priority(tasks_df).set_index("Priority")
    if priority_data.empty:
        st.info("Add tasks to see priority workload.")
    else:
        st.bar_chart(priority_data, y="Minutes", color="#d97706")

progress_column, capacity_column = st.columns(2)
with progress_column:
    st.markdown("#### Execution Progress")
    remaining_count = max(0, total_tasks(tasks_df) - completed_count)
    st.progress(completion_percentage(tasks_df) / 100)
    st.caption(f"{completed_count} completed · {remaining_count} remaining · {overdue_task_count(tasks_df, date.today())} overdue")
with capacity_column:
    st.markdown("#### Schedule Capacity")
    schedule_totals = scheduled_vs_unscheduled_minutes(tasks_df, st.session_state.schedule_df)
    remaining_capacity = available_minutes - scheduled_minutes
    st.metric("Available Hours", f"{available_hours:.1f} h")
    st.caption(f"Planned {planned_hours:.1f} h · Scheduled {schedule_totals['Scheduled'] / 60:.1f} h · Remaining capacity {remaining_capacity / 60:.1f} h")
    if capacity_delta > 0:
        st.error("Overloaded")
    elif capacity_delta > -1:
        st.warning("Near capacity")
    else:
        st.success("Under capacity")

with st.expander("Deeper analytics"):
    st.write(
        f"High-priority tasks: {high_priority_total} · Deferred tasks: {len(st.session_state.deferred_tasks)} · "
        f"Scheduled time: {scheduled_hours_value:.1f} h · Unscheduled time: {schedule_totals['Unscheduled'] / 60:.1f} h"
    )


st.markdown('<div id="plan"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="eyebrow">02 / PLAN</div><div class="section-heading"><span class="section-mark"></span><h2>Today\'s Mission</h2></div>',
    unsafe_allow_html=True,
)
if st.session_state.schedule_df.empty:
    st.info("Generate your plan from the sidebar to see your schedule here.")
else:
    mission_columns = st.columns(min(3, len(st.session_state.schedule_df)))
    for index, (_, block) in enumerate(st.session_state.schedule_df.iterrows()):
        with mission_columns[index % len(mission_columns)]:
            st.markdown(
                f"""
                <div class="mission">
                    <div class="mission-title">{block['Start']} &mdash; {block['End']}</div>
                    <p class="mission-copy"><strong>{block['Task']}</strong><br>{str(block['Priority']).upper()} PRIORITY</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.caption(f"Scheduled focus time: {scheduled_hours_value:.1f} hours")

    st.markdown("#### Schedule table")
    schedule_for_editor = st.session_state.schedule_df.copy()
    schedule_for_editor["Start"] = pd.to_datetime(
        schedule_for_editor["Start"], errors="coerce"
    ).dt.time
    schedule_for_editor["End"] = pd.to_datetime(
        schedule_for_editor["End"], errors="coerce"
    ).dt.time
    edited_schedule = st.data_editor(
        schedule_for_editor,
        key="schedule_editor",
        hide_index=True,
        width="stretch",
        column_config={
            "Start": st.column_config.TimeColumn("Start", format="HH:mm"),
            "End": st.column_config.TimeColumn("End", format="HH:mm"),
            "Priority": st.column_config.SelectboxColumn(
                "Priority", options=["Low", "Medium", "High"]
            ),
            "Reason": st.column_config.TextColumn("Reason"),
        },
        disabled=["Reason"],
    )
    if not edited_schedule.equals(st.session_state.schedule_df):
        normalized_schedule = edited_schedule.copy()
        for column in ["Start", "End"]:
            normalized_schedule[column] = normalized_schedule[column].map(
                lambda value: value.strftime("%H:%M") if hasattr(value, "strftime") else str(value)
            )
        st.session_state.schedule_df = normalized_schedule
        st.session_state.schedule = normalized_schedule.to_dict("records")
        st.session_state.change_log.append({"action": "schedule_edited"})

    if st.session_state.deferred_tasks:
        with st.expander("Deferred tasks"):
            st.dataframe(
                pd.DataFrame(st.session_state.deferred_tasks, columns=["Task", "Reason"]),
                hide_index=True,
                width="stretch",
            )


st.markdown('<div id="adapt"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="eyebrow">04 / ADAPT</div><div class="section-heading"><span class="section-mark"></span><h2>Something changed?</h2></div><p class="subtitle">Life happens. Your plan should adapt without starting from zero.</p>',
    unsafe_allow_html=True,
)
with st.form("replan_form"):
    disruption = st.selectbox(
        "What changed?",
        [
            "Lost 1 Hour",
            "Lost 2 Hours",
            "Energy Crash",
            "Surprise Meeting",
            "Unexpected Deadline",
            "Custom Disruption",
        ],
    )
    custom_disruption = ""
    if disruption == "Custom Disruption":
        custom_disruption = st.text_input(
            "Describe what happened", placeholder="A family commitment came up at 3 PM"
        )
    replan_submitted = st.form_submit_button("Replan My Day", width="stretch")

if replan_submitted:
    disruption_details = custom_disruption.strip() if custom_disruption else disruption
    if not st.session_state.tasks_df.shape[0]:
        st.warning("Add tasks first, then LifePilot can rebuild your plan.")
    elif disruption == "Custom Disruption" and not disruption_details:
        st.warning("Describe what changed before replanning your day.")
    else:
        old_schedule = st.session_state.schedule_df.copy()
        with st.spinner("LifePilot is rebuilding your day..."):
            try:
                replanned = replan_day(
                    st.session_state.tasks_df,
                    old_schedule,
                    disruption_details,
                    available_hours,
                    energy_level,
                    datetime.now().time(),
                    date.today(),
                    planning_preference,
                )
                new_schedule = pd.DataFrame(
                    replanned["schedule"],
                    columns=["Start", "End", "Task", "Priority", "Reason"],
                )
                st.session_state.last_replan_old_schedule = old_schedule
                st.session_state.schedule_df = new_schedule
                st.session_state.schedule = replanned["schedule"]
                st.session_state.deferred_tasks = replanned["deferred_tasks"]
                st.session_state.schedule_summary = replanned["summary"]
                st.session_state.replan_changes = replanned["changes"]
                st.session_state.schedule_stale = False
                st.session_state.replan_history.append(
                    {
                        "timestamp": datetime.now().isoformat(timespec="seconds"),
                        "disruption": disruption_details,
                        "summary": replanned["summary"],
                    }
                )
                st.session_state.replan_history = st.session_state.replan_history[-5:]
                st.session_state.change_log.append(
                    {"action": "day_replanned", "disruption": disruption_details}
                )
                st.success("Your plan has been recalculated.")
            except (TaskParseError, RuntimeError) as exc:
                st.error(str(exc))
            except Exception:
                st.error("LifePilot could not rebuild your plan right now. Please try again.")

if not st.session_state.last_replan_old_schedule.empty or st.session_state.replan_changes:
    st.markdown("#### OLD PLAN &rarr; NEW PLAN", unsafe_allow_html=True)
    old_column, new_column = st.columns(2)
    with old_column:
        st.caption("Previous schedule")
        if st.session_state.last_replan_old_schedule.empty:
            st.info("No previous schedule was available.")
        else:
            st.dataframe(
                st.session_state.last_replan_old_schedule[["Start", "End", "Task", "Priority"]],
                hide_index=True,
                width="stretch",
            )
    with new_column:
        st.caption("New schedule")
        st.dataframe(
            st.session_state.schedule_df[["Start", "End", "Task", "Priority"]],
            hide_index=True,
            width="stretch",
        )

    with st.expander("What changed?"):
        if st.session_state.replan_changes:
            st.dataframe(
                pd.DataFrame(st.session_state.replan_changes),
                hide_index=True,
                width="stretch",
            )
        else:
            st.info("No explicit task changes were returned.")

with st.expander("Recent Replans"):
    if st.session_state.replan_history:
        st.dataframe(
            pd.DataFrame(st.session_state.replan_history),
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("No replans yet.")


st.markdown(
    '<div class="section-heading"><span class="section-mark"></span><h2>LifePilot Intelligence</h2></div>',
    unsafe_allow_html=True,
)
if st.session_state.schedule_summary:
    with st.expander("Why did LifePilot make these decisions?", expanded=True):
        st.write(st.session_state.schedule_summary)
        for _, block in st.session_state.schedule_df.iterrows():
            st.markdown(
                f"**{block['Start']} - {block['End']} | {block['Task']}**  \n{block['Reason']}"
            )
else:
    st.markdown(
        '<div class="intelligence">Generate a plan to see the scheduling decisions and trade-offs.</div>',
        unsafe_allow_html=True,
    )
