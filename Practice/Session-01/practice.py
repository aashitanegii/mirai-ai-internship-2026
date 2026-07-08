import os
from google import genai

API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in your environment before running this script.")

# 1. Initialize the client
client = genai.Client(api_key=API_KEY)

# 2. Send the prompt to the model
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain what an API is in easy words."
)

# 3. Print the result
print(response.text)
