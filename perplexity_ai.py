import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not API_KEY:
    raise RuntimeError("PERPLEXITY_API_KEY not found (env load failed)")

API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar"


def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that answers questions about a user's task list."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"Perplexity API error {response.status_code}: {response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()




