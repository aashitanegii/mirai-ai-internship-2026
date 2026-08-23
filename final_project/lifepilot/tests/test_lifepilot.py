import json
import sys
import unittest
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.analytics import (
    completion_percentage,
    overdue_task_count,
    workload_by_category,
    workload_by_priority,
)
from modules.task_parser import TASK_COLUMNS, TaskParseError, parse_schedule, parse_tasks


class LifePilotTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {
                "Task": "Study OS",
                "Duration_Min": 60,
                "Priority": "High",
                "Deadline": "2026-08-23",
                "Category": "Academic",
                "Status": "Not Started",
            },
            {
                "Task": "Gym",
                "Duration_Min": 30,
                "Priority": "Medium",
                "Deadline": "",
                "Category": "Health",
                "Status": "Completed",
            },
        ]

    def test_task_parser_valid_json_and_fence(self):
        frame = parse_tasks("```json\n" + json.dumps(self.tasks) + "\n```")
        self.assertEqual(list(frame.columns), TASK_COLUMNS)
        self.assertEqual(frame.iloc[0]["Task"], "Study OS")

    def test_task_parser_malformed_json(self):
        with self.assertRaises(TaskParseError):
            parse_tasks("not json")

    def test_duplicate_schedule_task_rejected(self):
        block = {"start": "09:00", "end": "10:00", "task": "Study OS", "priority": "High", "reason": "Deadline"}
        payload = {"schedule": [block, block], "deferred_tasks": [], "summary": "x"}
        with self.assertRaises(TaskParseError):
            parse_schedule(json.dumps(payload), self.tasks[:1], 3)

    def test_schedule_validation(self):
        payload = {
            "schedule": [{"start": "09:00", "end": "10:00", "task": "Study OS", "priority": "High", "reason": "Deadline"}],
            "deferred_tasks": [],
            "summary": "Focused",
        }
        result = parse_schedule(json.dumps(payload), self.tasks[:1], 2)
        self.assertEqual(result["schedule"][0]["Start"], "09:00")

    def test_capacity_validation(self):
        payload = {
            "schedule": [{"start": "09:00", "end": "10:00", "task": "Study OS", "priority": "High", "reason": "Deadline"}],
            "deferred_tasks": [],
            "summary": "Focused",
        }
        with self.assertRaises(TaskParseError):
            parse_schedule(json.dumps(payload), self.tasks[:1], 0.5)

    def test_completion_percentage(self):
        frame = pd.DataFrame(self.tasks)
        self.assertEqual(completion_percentage(frame), 50)

    def test_overdue_task_calculation(self):
        frame = pd.DataFrame(self.tasks)
        self.assertEqual(overdue_task_count(frame, date(2026, 8, 24)), 1)

    def test_workload_calculations(self):
        frame = pd.DataFrame(self.tasks)
        self.assertEqual(set(workload_by_category(frame)["Category"]), {"Academic", "Health"})
        self.assertEqual(set(workload_by_priority(frame)["Priority"]), {"High", "Medium"})

    def test_empty_analytics_state(self):
        frame = pd.DataFrame(columns=TASK_COLUMNS)
        self.assertEqual(completion_percentage(frame), 0)
        self.assertTrue(workload_by_category(frame).empty)
        self.assertTrue(workload_by_priority(frame).empty)


if __name__ == "__main__":
    unittest.main()
