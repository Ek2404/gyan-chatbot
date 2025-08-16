import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")  # get from environment on Render
API_URL = "https://openrouter.ai/api/v1/chat/completions"

print("🔐 API Key Found:", bool(API_KEY), "| Length:", len(API_KEY) if API_KEY else 0)
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY environment variable is not set. Please set it before running the app.")

def get_response(messages):
    """
    messages should be a list of dicts like:
    [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
        {"role": "user", "content": "What about timings?"}
    ]
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://gyan-chatbot.onrender.com"  # 👈 required by OpenRouter
    }

    # If no system message yet, prepend one
    if not any(msg["role"] == "system" for msg in messages):
        messages.insert(0, {
            "role": "system",
            "content": "Answer briefly, clearly, and only what is asked. Keep responses under 40 words."
        })

    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": messages,
    }

    response = requests.post(API_URL, json=data, headers=headers)
    try:
        resp_json = response.json()
    except Exception:
        print("API did not return JSON:", response.text)
        return "Sorry, I couldn't get an answer from the AI service."

    # Handle rate limit error
    if response.status_code == 429 or ('error' in resp_json and resp_json.get('error', {}).get('code') == 429):
        return "Sorry, the AI service is temporarily busy. Please try again later."

    if response.status_code == 200:
        return resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return f"Error: {resp_json}"
