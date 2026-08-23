"""Validation and normalization for Gemini task extraction responses."""

import json
import re
from datetime import datetime
from typing import Any

import pandas as pd


TASK_COLUMNS = [
    "Task",
    "Duration_Min",
    "Priority",
    "Deadline",
    "Category",
    "Status",
]
PRIORITIES = {"High", "Medium", "Low"}
CATEGORIES = {"Academic", "Work", "Personal", "Health", "Errands", "Other"}
STATUSES = {"Not Started", "In Progress", "Completed"}


class TaskParseError(ValueError):
    """Raised when Gemini returns an unusable task payload."""


def _remove_code_fences(response_text: str) -> str:
    cleaned = response_text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else cleaned


def _normalize_choice(value: Any, allowed: set[str], fallback: str) -> str:
    candidate = str(value or "").strip()
    return candidate if candidate in allowed else fallback


def parse_tasks(response_text: str) -> pd.DataFrame:
    """Parse Gemini JSON and return a clean, schema-stable DataFrame."""
    try:
        payload = json.loads(_remove_code_fences(response_text))
    except (json.JSONDecodeError, TypeError) as exc:
        raise TaskParseError("Gemini returned malformed JSON.") from exc

    if not isinstance(payload, list):
        raise TaskParseError("Gemini response must be a JSON array of tasks.")

    normalized_tasks: list[dict[str, Any]] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise TaskParseError(f"Task {index} is not a JSON object.")
        missing = [column for column in TASK_COLUMNS if column not in item]
        if missing:
            raise TaskParseError(f"Task {index} is missing: {', '.join(missing)}.")

        task_name = str(item.get("Task") or "").strip()
        if not task_name:
            continue

        duration = pd.to_numeric(item.get("Duration_Min"), errors="coerce")
        if pd.isna(duration):
            duration = 30
        duration = min(180, max(15, int(duration)))

        normalized_tasks.append(
            {
                "Task": task_name,
                "Duration_Min": duration,
                "Priority": _normalize_choice(item.get("Priority"), PRIORITIES, "Medium"),
                "Deadline": str(item.get("Deadline") or "").strip(),
                "Category": _normalize_choice(item.get("Category"), CATEGORIES, "Other"),
                "Status": _normalize_choice(item.get("Status"), STATUSES, "Not Started"),
            }
        )

    return pd.DataFrame(normalized_tasks, columns=TASK_COLUMNS)


def parse_schedule(
    response_text: str,
    task_records: list[dict[str, Any]],
    available_hours: float,
    require_changes: bool = False,
) -> dict[str, Any]:
    """Validate a Gemini schedule against active tasks and available capacity."""
    try:
        payload = json.loads(_remove_code_fences(response_text))
    except (json.JSONDecodeError, TypeError) as exc:
        raise TaskParseError("Gemini returned malformed schedule JSON.") from exc

    if not isinstance(payload, dict):
        raise TaskParseError("Gemini schedule response must be a JSON object.")
    if not isinstance(payload.get("schedule"), list):
        raise TaskParseError("Schedule response is missing a schedule array.")
    if not isinstance(payload.get("deferred_tasks", []), list):
        raise TaskParseError("Deferred tasks must be a JSON array.")

    valid_tasks = {str(record.get("Task", "")).strip() for record in task_records}
    task_durations: dict[str, int] = {}
    for record in task_records:
        duration = pd.to_numeric(record.get("Duration_Min"), errors="coerce")
        task_durations[str(record.get("Task", "")).strip()] = (
            0 if pd.isna(duration) else int(duration)
        )
    schedule_rows: list[dict[str, str]] = []
    intervals: list[tuple[int, int]] = []
    scheduled_tasks: set[str] = set()
    for index, item in enumerate(payload["schedule"], start=1):
        if not isinstance(item, dict):
            raise TaskParseError(f"Schedule item {index} is not a JSON object.")
        required = ["start", "end", "task", "priority", "reason"]
        missing = [field for field in required if not item.get(field)]
        if missing:
            raise TaskParseError(f"Schedule item {index} is missing: {', '.join(missing)}.")

        start_text = str(item["start"]).strip()
        end_text = str(item["end"]).strip()
        try:
            start = datetime.strptime(start_text, "%H:%M")
            end = datetime.strptime(end_text, "%H:%M")
        except ValueError as exc:
            raise TaskParseError(f"Schedule item {index} has an invalid time.") from exc
        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute
        if end_minutes <= start_minutes:
            raise TaskParseError(f"Schedule item {index} ends before it starts.")
        task_name = str(item["task"]).strip()
        if task_name not in valid_tasks:
            raise TaskParseError(f"Schedule item {index} references an unknown task.")
        if task_name in scheduled_tasks:
            raise TaskParseError(f"Task '{task_name}' appears more than once in the schedule.")
        if end_minutes - start_minutes != task_durations.get(task_name, 0):
            raise TaskParseError(
                f"Schedule item {index} changes the duration of '{task_name}'."
            )
        priority = str(item["priority"]).strip()
        if priority not in PRIORITIES:
            raise TaskParseError(f"Schedule item {index} has an invalid priority.")
        intervals.append((start_minutes, end_minutes))
        scheduled_tasks.add(task_name)
        schedule_rows.append(
            {
                "Start": start_text,
                "End": end_text,
                "Task": task_name,
                "Priority": priority,
                "Reason": str(item["reason"]).strip(),
            }
        )

    ordered_intervals = sorted(intervals)
    if any(current[0] < previous[1] for previous, current in zip(ordered_intervals, ordered_intervals[1:])):
        raise TaskParseError("Gemini returned overlapping schedule blocks.")
    scheduled_minutes = sum(end - start for start, end in intervals)
    if scheduled_minutes > int(round(float(available_hours) * 60)):
        raise TaskParseError("Gemini returned a schedule exceeding available hours.")

    deferred_rows = []
    for item in payload.get("deferred_tasks", []):
        if not isinstance(item, dict) or not item.get("task") or not item.get("reason"):
            raise TaskParseError("Each deferred task needs a task and reason.")
        task_name = str(item["task"]).strip()
        if task_name not in valid_tasks:
            raise TaskParseError("Deferred tasks must reference existing tasks.")
        deferred_rows.append({"Task": task_name, "Reason": str(item["reason"]).strip()})

    if require_changes and "changes" not in payload:
        raise TaskParseError("Replan response is missing a changes array.")
    changes = payload.get("changes", [])
    if not isinstance(changes, list):
        raise TaskParseError("Schedule changes must be a JSON array.")
    normalized_changes = []
    for item in changes:
        if not isinstance(item, dict) or not item.get("task") or not item.get("change"):
            raise TaskParseError("Each schedule change needs a task and change description.")
        if str(item["task"]).strip() not in valid_tasks:
            raise TaskParseError("Schedule changes must reference existing tasks.")
        normalized_changes.append(
            {"Task": str(item["task"]).strip(), "Change": str(item["change"]).strip()}
        )

    return {
        "schedule": schedule_rows,
        "deferred_tasks": deferred_rows,
        "summary": str(payload.get("summary") or "Plan generated from your active tasks.").strip(),
        "changes": normalized_changes,
    }
