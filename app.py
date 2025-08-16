from flask import Flask, render_template, request, jsonify
import os

print("✅ Flask app starting...")

# Importing support modules with debug
try:
    from ai_response import get_response
    print("✅ Loaded ai_response.py")
except Exception as e:
    print("❌ Error in ai_response:", e)
from flask import Flask, render_template, request, jsonify, session
from uuid import uuid4
import os

print("✅ Flask app starting...")

# Importing support modules with debug
try:
    from ai_response import get_response
    print("✅ Loaded ai_response.py")
except Exception as e:
    print("❌ Error in ai_response:", e)

try:
    from automation import get_school_info
    print("✅ Loaded automation.py")
except Exception as e:
    print("❌ Error in automation:", e)

try:
    from conclave_response import answer_conclave_query
    print("✅ Loaded conclave_response.py")
except Exception as e:
    print("❌ Error in conclave_response:", e)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")  # required for sessions

# 📝 In-memory chat history for each user session
chat_history = {}

@app.before_request
def assign_session_id():
    """Assign a unique session ID if not already set"""
    if "session_id" not in session:
        session["session_id"] = str(uuid4())
        chat_history[session["session_id"]] = []

@app.route('/')
def home():
    print("✅ Root URL '/' was accessed.")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get("query", "").strip()
    session_id = session["session_id"]

    print("\n🔍 New Query Received:")
    print("📥 Query:", user_query)
    print("🆔 Session:", session_id)

    if not user_query:
        return jsonify({"answer": "Please ask something meaningful."})

    # ✅ 1. Check school_data.json
    school_info = get_school_info(user_query)
    if school_info:
        print("📚 Answered using school_data.json")
        chat_history[session_id].append({"role": "user", "content": user_query})
        chat_history[session_id].append({"role": "assistant", "content": school_info})
        return jsonify({"answer": school_info})

    # ✅ 2. Check conclave_data.json
    conclave_info = answer_conclave_query(user_query)
    if conclave_info:
        print("🎤 Answered using conclave_data.json")
        chat_history[session_id].append({"role": "user", "content": user_query})
        chat_history[session_id].append({"role": "assistant", "content": conclave_info})
        return jsonify({"answer": conclave_info})

    # ✅ 3. Fallback to AI with chat history
    chat_history[session_id].append({"role": "user", "content": user_query})
    ai_answer = get_response(chat_history[session_id])  # pass full conversation
    print("🤖 Answered using OpenRouter AI")

    chat_history[session_id].append({"role": "assistant", "content": ai_answer})
    return jsonify({"answer": ai_answer})

if __name__ == '__main__':
    print("🚀 Running Flask server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    print("✅ Flask app is running on port", port)
    print("✅ Ready to handle queries!")

try:
    from automation import get_school_info
    print("✅ Loaded automation.py")
except Exception as e:
    print("❌ Error in automation:", e)

try:
    from conclave_response import answer_conclave_query
    print("✅ Loaded conclave_response.py")
except Exception as e:
    print("❌ Error in conclave_response:", e)

app = Flask(__name__)

@app.route('/')
def home():
    print("✅ Root URL '/' was accessed.")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    print("\n🔍 New Query Received:")
    print("📥 Query:", user_query)

    if not user_query:
        return jsonify({"answer": "Please ask something meaningful."})

    # ✅ 1. Check school_data.json
    school_info = get_school_info(user_query)
    if school_info:
        print("📚 Answered using school_data.json")
        return jsonify({"answer": school_info})

    # ✅ 2. Check conclave_data.json
    conclave_info = answer_conclave_query(user_query)
    if conclave_info:
        print("🎤 Answered using conclave_data.json")
        return jsonify({"answer": conclave_info})

    # ✅ 3. Fallback to AI
    ai_answer = get_response(user_query)
    print("🤖 Answered using OpenRouter AI")
    return jsonify({"answer": ai_answer})

if __name__ == '__main__':
    print("🚀 Running Flask server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
print("✅ Flask app is running on port", port)
print("✅ Ready to handle queries!")