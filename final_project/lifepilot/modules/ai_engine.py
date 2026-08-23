"""Gemini communication for LifePilot task extraction."""

import json
from datetime import datetime
from typing import Any

import streamlit as st
from google import genai
from google.genai import types

from .task_parser import parse_tasks

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are LifePilot's task extraction engine.

Your job is to transform messy natural-language brain dumps into clear, actionable tasks.
Extract only tasks that the user actually mentions or clearly implies. Do not invent tasks.
For each task determine the task name, estimated duration in minutes, priority, deadline if mentioned,
category, and status. Normalize vague language intelligently. Convert relative dates using the current date.
Use only these categories: Academic, Work, Personal, Health, Errands, Other.
Use only these priorities: High, Medium, Low.
Use only these statuses: Not Started, In Progress, Completed. Status should initially be Not Started.
If no deadline is mentioned, use an empty string. If duration is unknown, estimate 15 to 180 minutes.
Return ONLY a valid JSON array. Do not return Markdown or explanations outside the JSON."""


def get_gemini_client() -> genai.Client:
    """Create the SDK client from the local Streamlit secret."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception as exc:
        raise RuntimeError("GEMINI_API_KEY is missing from Streamlit secrets.") from exc
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from Streamlit secrets.")
    return genai.Client(api_key=api_key)


def extract_tasks(
    brain_dump: str,
    *,
    available_hours: float,
    energy_level: str,
    existing_tasks: list[dict[str, Any]],
) -> Any:
    """Call Gemini once for a submitted brain dump and validate its response."""
    now = datetime.now()
    prompt = f"""
Current date: {now.date().isoformat()}
Current time: {now.strftime('%H:%M')}
Available hours today: {available_hours}
Energy level: {energy_level}

Existing tasks:
{json.dumps(existing_tasks, default=str)}

User brain dump:
{brain_dump}

Return a JSON array with exactly these fields for every task:
Task, Duration_Min, Priority, Deadline, Category, Status
"""

    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    response_text = getattr(response, "text", None)
    if not response_text:
        raise RuntimeError("Gemini returned an empty response.")
    return parse_tasks(response_text)


VOICE_SYSTEM_PROMPT = """You are LifePilot's voice task extraction engine.

Convert the user's spoken brain dump into structured actionable tasks. Ignore filler speech and
conversational noise. Extract only genuine tasks, commitments, deadlines, and priorities. Do not
invent information. If a deadline or priority is unclear, leave it blank or use the existing
default. Use LifePilot's existing task schema and return only valid JSON: an array containing
Task, Duration_Min, Priority, Deadline, Category, and Status for every task."""


def extract_tasks_from_audio(
    audio_bytes: bytes,
    mime_type: str,
    *,
    available_hours: float,
    energy_level: str,
    existing_tasks: list[dict[str, Any]],
) -> Any:
    """Transcribe and extract tasks from one explicitly submitted recording."""
    now = datetime.now()
    prompt = f"""
Current date: {now.date().isoformat()}
Current time: {now.strftime('%H:%M')}
Available hours today: {available_hours}
Energy level: {energy_level}

Existing tasks:
{json.dumps(existing_tasks, default=str)}

Listen to the attached spoken brain dump and return only the structured task JSON array.
"""
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(
            system_instruction=VOICE_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    response_text = getattr(response, "text", None)
    if not response_text:
        raise RuntimeError("Gemini returned an empty voice extraction response.")
    return parse_tasks(response_text)


IMAGE_SYSTEM_PROMPT = """You are LifePilot's visual task extraction engine.

Read the attached handwritten list, whiteboard, notebook page, or screenshot and extract only
actionable tasks. Preserve visible deadlines, assign priority conservatively, and infer duration
only when clearly implied. Never invent unrelated tasks. Return only valid JSON using LifePilot's
existing task schema: Task, Duration_Min, Priority, Deadline, Category, and Status."""


def extract_tasks_from_image(
    image_bytes: bytes,
    mime_type: str,
    *,
    available_hours: float,
    energy_level: str,
    existing_tasks: list[dict[str, Any]],
) -> Any:
    """Extract tasks from one explicitly submitted image."""
    now = datetime.now()
    prompt = f"""
Current date: {now.date().isoformat()}
Current time: {now.strftime('%H:%M')}
Available hours today: {available_hours}
Energy level: {energy_level}

Existing tasks:
{json.dumps(existing_tasks, default=str)}

Inspect the attached image and return only the structured task JSON array.
"""
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(
            system_instruction=IMAGE_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    response_text = getattr(response, "text", None)
    if not response_text:
        raise RuntimeError("Gemini returned an empty image extraction response.")
    return parse_tasks(response_text)
