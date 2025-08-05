import requests

API_KEY = "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"  # Replace with your actual API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_response(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": [
            {"role": "system", "content": "Answer briefly, clearly, and only what is asked. Keep responses under 40 words."},
            {"role": "user", "content": query}
        ],
    }
    response = requests.post(API_URL, json=data, headers=headers)
    try:
        resp_json = response.json()
    except Exception:
        print("API did not return JSON:", response.text)
        return "Sorry, I couldn't get an answer from the AI service."

    # Handle rate limit error
    if response.status_code == 429 or ('error' in resp_json and resp_json['error'].get('code') == 429):
        return "Sorry, the AI service is temporarily busy. Please try again later."

    if response.status_code == 200:
        return resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return f"Error: {resp_json}"