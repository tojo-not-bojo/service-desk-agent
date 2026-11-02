"""Send a Gemini request with the requests library, to compare against httpx."""
import os

import requests
from dotenv import load_dotenv

load_dotenv("agents/service_desk/.env")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
response = requests.post(
    url,
    headers={"x-goog-api-key": os.environ["GOOGLE_API_KEY"]},
    json={"contents": [{"parts": [{"text": "Say hello in five words."}]}]},
    timeout=30,
)
print(response.status_code)
print(response.text[:500])