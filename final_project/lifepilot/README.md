# LifePilot

## AI Personal Decision & Execution Engine

Turn messy thoughts, interruptions, and constraints into a plan you can actually execute.

## Demo

[Live App](#) - deployment URL will be added after deployment.

## Why LifePilot?

Real days contain scattered commitments, shifting energy, interruptions, and more work than available time. LifePilot turns that human input into a transparent, editable plan rather than another generic chatbot conversation.

## Core Features

- Multimodal task capture: text, voice, and camera
- Gemini structured task extraction
- Constraint-aware daily scheduling
- Replan My Day after disruptions
- Editable tasks and schedules
- Analytics command center
- AI reasoning and trade-off explanations

## Usage

1. Capture tasks with a text brain dump, microphone recording, camera image, or Quick Add.
2. Review and edit the validated task DataFrame before planning.
3. Set available hours and energy level, then select **Generate My Plan**.
4. Use **Replan My Day** when an interruption changes the available capacity.
5. Review the before/after schedule, deferred work, decision reasons, and analytics.

For an evaluator walkthrough, use the sidebar's explicitly labeled **DEMO MODE** controls. **Load Demo Day** adds a local sample scenario; **Clear Demo** returns to an empty state. Demo loading never calls Gemini.

The sidebar's **Planning Preference** is included in the scheduling and replanning context alongside available hours and energy level.

## Screenshots

Add final screenshots here before submission. Recommended captures:

- LifePilot command center with KPI cards and capture controls
- Today's Mission schedule with AI explanation expanded
- Replan My Day before/after comparison
- LifeLoad analytics with task and schedule data

## How It Works

```text
Text / Voice / Camera -> Gemini -> Validated JSON -> Pandas Tasks
    -> Constraints -> Schedule -> Execute / Replan / Analytics
```

## Tech Stack

Python, Streamlit, Pandas, Altair, Pillow, and the Google Gemini API through `google-genai`.

## Project Structure

```text
lifepilot/
|-- app.py
|-- requirements.txt
|-- README.md
|-- TECHNICAL_DESIGN.md
|-- modules/
|   |-- __init__.py
|   |-- ai_engine.py
|   |-- task_parser.py
|   |-- scheduler.py
|   |-- constraints.py
|   `-- analytics.py
`-- tests/
    `-- test_lifepilot.py
```

## Local Setup

```text
$ git clone <repository-url>
$ cd mirai-ai-internship-2026/final_project/lifepilot
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` locally:

```toml
GEMINI_API_KEY = "your-key-here"
```

Never commit `.env` or `.streamlit/secrets.toml`. On Streamlit Community Cloud, add `GEMINI_API_KEY` in the app's Secrets settings.

## Run

```text
$ streamlit run app.py
```

## Deployment

Create a Streamlit Community Cloud app from the repository, set the main file to `final_project/lifepilot/app.py`, and add the Gemini key in Advanced settings under Secrets. Install dependencies from `final_project/lifepilot/requirements.txt` or deploy from this directory as the app root.

## Security

The Gemini key is loaded only through Streamlit secrets. Secret files are excluded from Git, and no key is present in Python source or documentation.

## Future Scope

- Calendar integration with explicit user approval
- Persistent storage with user-controlled export
- More detailed long-term workload trends
- Accessibility and keyboard workflow improvements
