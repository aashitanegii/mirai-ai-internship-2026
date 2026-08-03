import random
from datetime import datetime, timedelta

import pandas as pd

# -----------------------------------------------------------
# Generate a realistic synthetic screen time dataset
# -----------------------------------------------------------
random.seed(42)

apps = {
    "Instagram": "Social Media",
    "TikTok": "Social Media",
    "X": "Social Media",
    "YouTube": "Entertainment",
    "Netflix": "Entertainment",
    "Duolingo": "Education",
    "Notion": "Productivity",
    "VS Code": "Coding",
    "GitHub": "Coding",
}

start_date = datetime.now() - timedelta(days=13)
data = []

for offset in range(14):
    current_date = (start_date + timedelta(days=offset)).strftime("%Y-%m-%d")
    daily_apps = random.sample(list(apps.keys()), random.randint(5, 7))

    for app_name in daily_apps:
        category = apps[app_name]
        if category == "Social Media":
            minutes_used = random.randint(30, 180)
        elif category == "Coding":
            minutes_used = random.randint(60, 240)
        elif category == "Productivity":
            minutes_used = random.randint(15, 90)
        elif category == "Education":
            minutes_used = random.randint(20, 80)
        else:
            minutes_used = random.randint(15, 120)

        data.append([current_date, app_name, category, minutes_used])

# Save to CSV in the current project folder
output_df = pd.DataFrame(data, columns=["Date", "App_Name", "Category", "Minutes_Used"])
output_df.to_csv("screentime.csv", index=False)
print("✅ screentime.csv generated successfully with 14 days of synthetic data.")
