from google import genai
from google.genai import types

client = genai.Client(http_options=types.HttpOptions(timeout=60000))
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Dis bonjour en une phrase."
)
print(response.text)
