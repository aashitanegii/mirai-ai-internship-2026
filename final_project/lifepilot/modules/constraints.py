"""Deterministic task and schedule capacity calculations."""

from typing import Any

import pandas as pd


def calculate_total_task_minutes(tasks_df: pd.DataFrame) -> int:
    if tasks_df.empty or "Duration_Min" not in tasks_df:
        return 0
    return int(pd.to_numeric(tasks_df["Duration_Min"], errors="coerce").fillna(0).sum())


def calculate_available_minutes(available_hours: float) -> int:
    return max(0, int(round(float(available_hours) * 60)))


def calculate_scheduled_minutes(schedule_df: pd.DataFrame) -> int:
    if schedule_df.empty or not {"Start", "End"}.issubset(schedule_df.columns):
        return 0
    starts = pd.to_datetime(schedule_df["Start"].astype(str), errors="coerce")
    ends = pd.to_datetime(schedule_df["End"].astype(str), errors="coerce")
    return int(((ends - starts).dt.total_seconds() / 60).clip(lower=0).fillna(0).sum())


def calculate_deferred_minutes(tasks_df: pd.DataFrame, schedule_df: pd.DataFrame) -> int:
    total = calculate_total_task_minutes(tasks_df)
    scheduled = calculate_scheduled_minutes(schedule_df)
    return max(0, total - scheduled)


def remaining_capacity_minutes(available_hours: float, scheduled_df: pd.DataFrame) -> int:
    return calculate_available_minutes(available_hours) - calculate_scheduled_minutes(scheduled_df)


def has_overload(total_task_minutes: int, available_hours: float) -> bool:
    return total_task_minutes > calculate_available_minutes(available_hours)


def completed_tasks(tasks_df: pd.DataFrame) -> pd.DataFrame:
    if tasks_df.empty:
        return tasks_df.copy()
    return tasks_df[tasks_df["Status"].eq("Completed")].copy()


def high_priority_tasks(tasks_df: pd.DataFrame) -> pd.DataFrame:
    if tasks_df.empty:
        return tasks_df.copy()
    return tasks_df[tasks_df["Priority"].eq("High")].copy()


def clean_task_records(tasks_df: pd.DataFrame) -> list[dict[str, Any]]:
    """Remove blank rows and serialize task values for a prompt."""
    if tasks_df.empty:
        return []
    clean = tasks_df.copy()
    clean = clean[clean["Task"].fillna("").astype(str).str.strip().ne("")]
    return clean.to_dict("records")
