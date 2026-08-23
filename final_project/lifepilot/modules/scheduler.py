"""Gemini-backed constraint-based daily scheduling."""

import json
from datetime import date, time
from typing import Any

import pandas as pd
from google.genai import types

from .ai_engine import get_gemini_client, MODEL_NAME
from .constraints import clean_task_records, calculate_total_task_minutes
from .task_parser import parse_schedule

SCHEDULER_SYSTEM_PROMPT = """You are LifePilot's constraint-based scheduling engine.

Create a realistic daily execution plan from the user's tasks and constraints.
Never schedule more time than the user's available hours. Prioritize High priority tasks,
respect explicit deadlines, and never schedule Completed tasks. Consider energy level:
put demanding academic or deep-work tasks during higher-energy periods and shorter/lighter
tasks during lower-energy periods. Preserve reasonable breaks. If there are more tasks than
available time, explicitly mark lower-priority tasks as deferred. Never invent tasks, change
a user's duration without explaining why, or schedule a task not in the input.
Every scheduled block must reference an existing task. Return ONLY valid JSON with this shape:
{"schedule": [{"start": "09:00", "end": "10:30", "task": "...", "priority": "High", "reason": "..."}],
"deferred_tasks": [{"task": "...", "reason": "..."}], "summary": "..."}"""


def generate_daily_plan(
    tasks_df: pd.DataFrame,
    available_hours: float,
    energy_level: str,
    current_time: time,
    current_date: date,
    planning_preference: str = "Protect deadlines",
) -> dict[str, Any]:
    """Ask Gemini for a plan, then validate it before returning it to the UI."""
    active_tasks = tasks_df[tasks_df["Status"].ne("Completed")].copy()
    task_records = clean_task_records(active_tasks)
    if not task_records:
        return {"schedule": [], "deferred_tasks": [], "summary": "No active tasks to schedule."}

    total_minutes = calculate_total_task_minutes(active_tasks)
    tasks_json = json.dumps(task_records, default=str)
    prompt = f"""
Current date: {current_date.isoformat()}
Current time: {current_time.strftime('%H:%M')}
Available hours today: {available_hours}
Energy level: {energy_level}
Planning preference: {planning_preference}
Total task load: {total_minutes} minutes

Tasks:
{tasks_json}

Return the required schedule JSON now. Use 24-hour HH:MM times and reference only these tasks.
"""

    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SCHEDULER_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    response_text = getattr(response, "text", None)
    if not response_text:
        raise RuntimeError("Gemini returned an empty scheduling response.")
    return parse_schedule(response_text, task_records, available_hours)


REPLAN_SYSTEM_PROMPT = """You are LifePilot's emergency constraint-based replanning engine.

Recalculate the remaining daily schedule after a disruption. Completed tasks are locked and
strict deadlines are protected. Preserve high-priority work whenever possible, compress flexible
tasks only when appropriate, and move lower-priority tasks to deferred_tasks when capacity is
insufficient. Never invent tasks, schedule completed tasks, change a duration without explaining
it in changes, or exceed the remaining available time. Every schedule block must reference an
existing task. Explain trade-offs briefly and return ONLY valid JSON with schedule, deferred_tasks,
summary, and changes arrays/fields as requested."""


def _remaining_hours(disruption: str, available_hours: float) -> float:
    if disruption == "Lost 1 Hour":
        return max(0, available_hours - 1)
    if disruption == "Lost 2 Hours":
        return max(0, available_hours - 2)
    return max(0, available_hours)


def replan_day(
    tasks_df: pd.DataFrame,
    schedule_df: pd.DataFrame,
    disruption: str,
    available_hours: float,
    energy_level: str,
    current_time: time,
    current_date: date,
    planning_preference: str = "Protect deadlines",
) -> dict[str, Any]:
    """Rebuild a schedule after an explicit user disruption."""
    active_tasks = tasks_df[tasks_df["Status"].ne("Completed")].copy()
    task_records = clean_task_records(active_tasks)
    if not task_records:
        return {"schedule": [], "deferred_tasks": [], "summary": "No active tasks to replan.", "changes": []}

    remaining_hours = _remaining_hours(disruption, available_hours)
    prompt = f"""
Current date: {current_date.isoformat()}
Current time: {current_time.strftime('%H:%M')}
Energy level: {energy_level}
Planning preference: {planning_preference}
Available hours today: {available_hours}
Remaining available hours after disruption: {remaining_hours}
Disruption: {disruption}

Existing tasks:
{json.dumps(task_records, default=str)}

Current schedule:
{json.dumps(schedule_df.to_dict('records'), default=str)}

Return the required JSON with schedule, deferred_tasks, summary, and changes.
"""
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=REPLAN_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    response_text = getattr(response, "text", None)
    if not response_text:
        raise RuntimeError("Gemini returned an empty replanning response.")
    return parse_schedule(response_text, task_records, remaining_hours, require_changes=True)
