import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")  # get from environment on Render
API_URL = "https://openrouter.ai/api/v1/chat/completions"

print("🔐 API Key Found:", bool(API_KEY), "| Length:", len(API_KEY) if API_KEY else 0)
if not API_KEY:
    print("⚠️  Warning: OPENROUTER_API_KEY environment variable is not set.")
    print("   AI responses will not work. Please set OPENROUTER_API_KEY environment variable.")
    # Don't raise error, just continue without AI functionality

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
    if not API_KEY:
        return "Sorry, AI service is not configured. Please set OPENROUTER_API_KEY environment variable."
    
    # Debug: Show conversation context
    print(f"🧠 AI Context: Processing {len(messages)} messages")
    if len(messages) > 1:
        print(f"📝 Last user message: {messages[-1]['content'][:100]}...")
        print(f"🔄 Conversation length: {len(messages)} messages")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://gyan-chatbot.onrender.com"  # 👈 required by OpenRouter
    }

    # Enhanced system message for better context handling
    if not any(msg["role"] == "system" for msg in messages):
        system_message = """You are GYAN, a helpful school information chatbot. 
        
IMPORTANT CONTEXT RULES:
1. ALWAYS remember the full conversation history
2. If user asks follow-up questions, refer back to previous context
3. If discussing a specific event, person, or topic, maintain that context
4. Be conversational and reference previous messages when relevant
5. Keep responses clear and helpful, under 60 words
6. If user asks "what about X" or "tell me more about X", connect it to previous context

Example: If user asks about "the science fair" and then asks "what about prizes?", 
you should know they're asking about science fair prizes, not general prizes."""
        
        messages.insert(0, {
            "role": "system",
            "content": system_message
        })

    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": messages,
        "temperature": 0.7,  # Slightly creative but consistent
        "max_tokens": 150    # Reasonable response length
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=30)
        resp_json = response.json()
    except requests.exceptions.Timeout:
        return "Sorry, the AI service is taking too long to respond. Please try again."
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Sorry, I couldn't connect to the AI service. Please check your internet connection."
    except Exception as e:
        print(f"API did not return JSON: {e}")
        return "Sorry, I couldn't get an answer from the AI service."

    # Handle rate limit error
    if response.status_code == 429 or ('error' in resp_json and resp_json.get('error', {}).get('code') == 429):
        return "Sorry, the AI service is temporarily busy. Please try again later."

    if response.status_code == 200:
        ai_response = resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"🤖 AI Response: {ai_response[:100]}...")
        return ai_response
    else:
        error_msg = resp_json.get('error', {}).get('message', 'Unknown error')
        print(f"API Error {response.status_code}: {error_msg}")
        return f"Sorry, the AI service returned an error: {error_msg}"
