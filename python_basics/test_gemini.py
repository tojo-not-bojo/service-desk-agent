"""Check that the Gemini API key and network connection work, without ADK."""
import os

from dotenv import load_dotenv
from google import genai

load_dotenv("agents/service_desk/.env")   # load the same key ADK uses

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Say hello in five words.",
)
print(response.text)