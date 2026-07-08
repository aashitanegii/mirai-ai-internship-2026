from google import genai

# 1. Initialize the client
client = genai.Client(api_key="REDACTED")

# 2. Send the prompt to the model
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain what an API is in easy words."
)

# 3. Print the result
print(response.text)
