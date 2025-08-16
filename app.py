from flask import Flask, render_template, request, jsonify, session
from uuid import uuid4
import os

print("✅ Flask app starting...")

# Import configuration with fallback
try:
    from config import Config
    Config.validate()
    print("✅ Configuration loaded")
    SECRET_KEY = Config.SECRET_KEY
    DEBUG_MODE = Config.DEBUG
    PORT = Config.PORT
except Exception as e:
    print("⚠️  Warning: Config import failed, using fallback values")
    print(f"   Error: {e}")
    SECRET_KEY = "supersecret"
    DEBUG_MODE = True
    PORT = 5000

# Import chat history manager
try:
    from chat_history import chat_manager
    print("✅ Loaded chat history manager")
except Exception as e:
    print("❌ Error loading chat history manager:", e)
    chat_manager = None

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
app.secret_key = SECRET_KEY

# 📝 In-memory chat history for each user session (fallback)
chat_history = {}

# 🧠 NEW: Simple context memory - stores last event for each session
session_context = {}

@app.before_request
def assign_session_id():
    """Assign a unique session ID if not already set"""
    if "session_id" not in session:
        session["session_id"] = str(uuid4())
        # Load existing history if available
        if chat_manager:
            existing_history = chat_manager.load_session_history(session["session_id"])
            chat_history[session["session_id"]] = existing_history
        else:
            chat_history[session["session_id"]] = []
        print(f"🆔 New session created: {session['session_id']}")

def save_message_to_history(session_id: str, role: str, content: str):
    """Save message to both memory and persistent storage"""
    # Save to memory
    if session_id not in chat_history:
        chat_history[session_id] = []
    chat_history[session_id].append({"role": role, "content": content})
    
    # Save to persistent storage
    if chat_manager:
        chat_manager.save_message(session_id, role, content)

def get_context_aware_query(session_id: str, user_query: str):
    """NEW: Simple context system - if user asks about timing/prizes/format without mentioning event, use last known event"""
    
    # Check if this is a follow-up question (timing, prizes, format, etc.)
    follow_up_keywords = [
        "timing", "time", "when", "schedule", "date",
        "prizes", "awards", "rewards", "prize",
        "format", "how", "process", "structure",
        "participants", "who", "eligibility", "classes",
        "registration", "deadline", "apply", "venue", "location"
    ]
    
    is_follow_up = any(keyword in user_query.lower() for keyword in follow_up_keywords)
    
    if is_follow_up and session_id in session_context:
        last_event = session_context[session_id]
        print(f"🧠 Context detected! User asking about '{user_query}' - applying context: '{last_event}'")
        
        # Create multiple context-aware query variations for better matching
        context_queries = [
            f"{last_event} {user_query}",           # "scriptorium its timing?"
            f"{user_query} {last_event}",           # "its timing? scriptorium"
            f"{last_event}",                         # Just the event name
            f"{last_event} {user_query.lower()}",   # Lowercase version
            f"{user_query.lower()} {last_event}"    # Lowercase query + event
        ]
        
        print(f"🔍 Context queries to try: {context_queries}")
        return context_queries, True
    
    return [user_query], False

def update_session_context(session_id: str, query: str, response: str):
    """NEW: Update context memory when we find an event"""
    
    # Check if response contains event information from conclave data
    response_lower = response.lower()
    
    # List of all events from conclave_data.json
    events = [
        "plurilogues", "continuum", "quartet", "scriptorium", "sensorium",
        "quest", "crossconnect", "biblioquest", "newstrack", "visual vocabulary",
        "united nations reimagined"
    ]
    
    for event in events:
        if event in response_lower:
            session_context[session_id] = event
            print(f"🧠 Updated context for session {session_id}: {event}")
            return
    
    # Fallback for other events
    if "scriptorium" in response_lower:
        session_context[session_id] = "scriptorium"
        print(f"🧠 Updated context for session {session_id}: scriptorium")
    elif "annual sports meet" in response_lower or "sports meet" in response_lower:
        session_context[session_id] = "annual sports meet"
        print(f"🧠 Updated context for session {session_id}: annual sports meet")

@app.route('/')
def home():
    print("✅ Root URL '/' was accessed.")
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Admin interface for managing chat sessions"""
    return render_template('admin.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        user_query = data.get("query", "").strip()
        session_id = session["session_id"]

        print(f"\n🔍 New Query Received:")
        print(f"📥 Query: '{user_query}'")
        print(f"🆔 Session: {session_id}")
        print(f"🧠 Current context: {session_context.get(session_id, 'None')}")

        if not user_query:
            return jsonify({"answer": "Please ask something meaningful."})

        # Save user message
        save_message_to_history(session_id, "user", user_query)

        # NEW: Get context-aware query
        context_queries, is_context_used = get_context_aware_query(session_id, user_query)
        
        print(f"🔍 Processing query: '{context_queries[0]}' (context used: {is_context_used})")

        # ✅ 1. Check school_data.json with context
        try:
            # Try all context queries if available
            for context_query in context_queries:
                school_info = get_school_info(context_query)
                if school_info:
                    print(f"📚 Answered using school_data.json with query: '{context_query}'")
                    save_message_to_history(session_id, "assistant", school_info)
                    update_session_context(session_id, context_query, school_info)
                    return jsonify({"answer": school_info})
        except Exception as e:
            print(f"❌ Error in school_info: {e}")

        # ✅ 2. Check conclave_data.json with context
        try:
            # Try all context queries if available
            for context_query in context_queries:
                conclave_info = answer_conclave_query(context_query)
                if conclave_info:
                    print(f"🎤 Answered using conclave_data.json with query: '{context_query}'")
                    save_message_to_history(session_id, "assistant", conclave_info)
                    update_session_context(session_id, context_query, conclave_info)
                    return jsonify({"answer": conclave_info})
        except Exception as e:
            print(f"❌ Error in conclave_info: {e}")

        # ✅ 3. Fallback to AI with chat history
        try:
            # Get current history for AI context
            current_history = chat_history.get(session_id, [])
            
            # Debug: Show context being sent to AI
            print(f"🧠 Sending context to AI:")
            print(f"   Session: {session_id}")
            print(f"   Messages in context: {len(current_history)}")
            if current_history:
                print(f"   First message: {current_history[0]['content'][:50]}...")
                print(f"   Last message: {current_history[-1]['content'][:50]}...")
            
            ai_answer = get_response(current_history)
            print("🤖 Answered using OpenRouter AI")
            save_message_to_history(session_id, "assistant", ai_answer)
            return jsonify({"answer": ai_answer})
        except Exception as e:
            print(f"❌ Error in AI response: {e}")
            error_msg = "Sorry, I'm having trouble processing your request right now. Please try again later."
            save_message_to_history(session_id, "assistant", error_msg)
            return jsonify({"answer": error_msg})

    except Exception as e:
        print(f"❌ Unexpected error in ask route: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chat-history/<session_id>')
def get_chat_history(session_id):
    """Get chat history for a specific session"""
    try:
        if chat_manager:
            history = chat_manager.load_session_history(session_id)
            return jsonify({"session_id": session_id, "messages": history})
        else:
            # Fallback to memory
            history = chat_history.get(session_id, [])
            return jsonify({"session_id": session_id, "messages": history, "note": "from memory"})
    except Exception as e:
        print(f"❌ Error getting chat history: {e}")
        return jsonify({"error": "Failed to load chat history"}), 500

@app.route('/sessions')
def list_sessions():
    """List all available chat sessions"""
    try:
        if chat_manager:
            sessions = chat_manager.list_all_sessions()
            return jsonify({"sessions": sessions})
        else:
            # Fallback to memory sessions
            memory_sessions = [
                {
                    "session_id": sid,
                    "message_count": len(messages),
                    "note": "in-memory session"
                }
                for sid, messages in chat_history.items()
            ]
            return jsonify({"sessions": memory_sessions, "note": "from memory"})
    except Exception as e:
        print(f"❌ Error listing sessions: {e}")
        return jsonify({"error": "Failed to list sessions"}), 500

@app.route('/clear-session/<session_id>', methods=['DELETE'])
def clear_session(session_id):
    """Clear chat history for a specific session"""
    try:
        if chat_manager:
            success = chat_manager.delete_session(session_id)
            if success:
                print(f"✅ Cleared persistent session: {session_id}")
        else:
            success = False
        
        # Clear from memory
        if session_id in chat_history:
            del chat_history[session_id]
            print(f"✅ Cleared memory session: {session_id}")
            success = True
        
        # Clear context
        if session_id in session_context:
            del session_context[session_id]
            print(f"🧠 Cleared context for session: {session_id}")
            success = True
        
        if success:
            return jsonify({"message": f"Session {session_id} cleared successfully"})
        else:
            return jsonify({"error": "Session not found"}), 404
            
    except Exception as e:
        print(f"❌ Error clearing session: {e}")
        return jsonify({"error": "Failed to clear session"}), 500

if __name__ == '__main__':
    print("🚀 Running Flask server...")
    print(f"✅ Flask app is running on port {PORT}")
    print("✅ Ready to handle queries!")
    print("💾 Chat history will be saved to 'chat_sessions' directory")
    print("🔧 Admin interface available at: /admin")
    print("🧠 NEW: Simple context system enabled!")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG_MODE)
