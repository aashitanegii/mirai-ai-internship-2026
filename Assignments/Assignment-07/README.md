# Assignment 07 — Life-OS Wellbeing Dashboard

This project is a Streamlit-based capstone dashboard that visualizes synthetic screen time data, gives AI-powered coaching advice, and shows a dynamic guilt-trip avatar based on the user's daily performance.

LIVE DEPLOYMENT LINK - https://life-os-ai-dashboard-mirai.streamlit.app/

## Files included
- app.py — the full Streamlit dashboard
- generate_data.py — creates a synthetic screentime.csv file
- screentime.csv — generated dataset (created after running the generator)
- requirements.txt — Python dependencies
- .gitignore — ignores local secrets and Python artifacts

## 1. Create the synthetic dataset
Run the generator once:

```bash
python generate_data.py
```

This creates a file named screentime.csv with 14 days of realistic synthetic data.

## 2. Run the app locally
Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

## 3. Add your Gemini API key locally
Create a local file at .streamlit/secrets.toml with:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

## 4. Deploy to Streamlit Community Cloud
1. Push this project to a public GitHub repository.
2. Open Streamlit Community Cloud.
3. Choose "Deploy a app" and connect your repository.
4. Set the main file path to app.py.
5. In Advanced Settings, add the secret:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

6. Click Deploy.
