from flask import Flask, render_template, request, jsonify
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