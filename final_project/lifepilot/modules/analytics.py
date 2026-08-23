"""Dashboard metrics derived from task and schedule DataFrames."""

import pandas as pd

from .constraints import calculate_scheduled_minutes, calculate_total_task_minutes


def total_tasks(tasks_df: pd.DataFrame) -> int:
    return len(tasks_df)


def completed_tasks(tasks_df: pd.DataFrame) -> int:
    return int(tasks_df["Status"].eq("Completed").sum()) if not tasks_df.empty else 0


def high_priority_count(tasks_df: pd.DataFrame) -> int:
    return int(tasks_df["Priority"].eq("High").sum()) if not tasks_df.empty else 0


def total_planned_hours(tasks_df: pd.DataFrame) -> float:
    return calculate_total_task_minutes(tasks_df) / 60


def scheduled_hours(schedule_df: pd.DataFrame) -> float:
    return calculate_scheduled_minutes(schedule_df) / 60


def deferred_count(deferred_tasks: list[dict]) -> int:
    return len(deferred_tasks)


def capacity_difference(tasks_df: pd.DataFrame, available_hours: float) -> float:
    return (calculate_total_task_minutes(tasks_df) / 60) - float(available_hours)


def completion_percentage(tasks_df: pd.DataFrame) -> float:
    return completed_tasks(tasks_df) / total_tasks(tasks_df) * 100 if total_tasks(tasks_df) else 0.0


def total_planned_minutes(tasks_df: pd.DataFrame) -> int:
    return calculate_total_task_minutes(tasks_df)


def overdue_task_count(tasks_df: pd.DataFrame, current_date=None) -> int:
    if tasks_df.empty:
        return 0
    today = pd.Timestamp(current_date).normalize() if current_date else pd.Timestamp.today().normalize()
    deadlines = pd.to_datetime(tasks_df["Deadline"], errors="coerce")
    overdue = deadlines.notna() & deadlines.dt.normalize().lt(today)
    return int((overdue & tasks_df["Status"].ne("Completed")).sum())


def workload_by_category(tasks_df: pd.DataFrame) -> pd.DataFrame:
    if tasks_df.empty:
        return pd.DataFrame(columns=["Category", "Minutes"])
    return tasks_df.groupby("Category", as_index=False)["Duration_Min"].sum().rename(columns={"Duration_Min": "Minutes"})


def workload_by_priority(tasks_df: pd.DataFrame) -> pd.DataFrame:
    if tasks_df.empty:
        return pd.DataFrame(columns=["Priority", "Minutes"])
    return tasks_df.groupby("Priority", as_index=False)["Duration_Min"].sum().rename(columns={"Duration_Min": "Minutes"})


def scheduled_vs_unscheduled_minutes(tasks_df: pd.DataFrame, schedule_df: pd.DataFrame) -> dict[str, int]:
    scheduled = calculate_scheduled_minutes(schedule_df)
    return {"Scheduled": scheduled, "Unscheduled": max(0, calculate_total_task_minutes(tasks_df) - scheduled)}
