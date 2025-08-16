# 🚀 GYAN Chatbot Setup Guide

## **Problem Fixed: "Error Talking to Server"**

The main issues that were causing the "Error talking to server" problem have been resolved:

1. ✅ **Duplicate code in app.py** - Cleaned up conflicting routes
2. ✅ **JavaScript conflicts** - Removed duplicate event listeners
3. ✅ **Better error handling** - Added proper try-catch blocks
4. ✅ **Configuration management** - Centralized environment variables
5. ✅ **Server validation** - Added startup checks
6. ✅ **Chat History Persistence** - Added persistent chat session storage

## **📋 Setup Steps**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Set Environment Variables**
Create a `.env` file in your project root (or set these in your system):

```bash
# Required for AI responses
OPENROUTER_API_KEY=your_actual_api_key_here

# Optional - Flask configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
PORT=5000
```

**⚠️ Important:** You need an OpenRouter API key for AI responses to work. Get one from [OpenRouter](https://openrouter.ai/).

### **Step 3: Run the Server**
```bash
python app.py
```

You should see:
```
✅ Flask app starting...
✅ Configuration loaded
✅ Loaded chat history manager
✅ Loaded ai_response.py
✅ Loaded automation.py
✅ Loaded conclave_response.py
🚀 Running Flask server...
✅ Flask app is running on port 5000
✅ Ready to handle queries!
💾 Chat history will be saved to 'chat_sessions' directory
🔧 Admin interface available at: /admin
```

### **Step 4: Test the Server**
Open a new terminal and run:
```bash
python test_server.py
```

This will verify that your server is working correctly.

### **Step 5: Open in Browser**
Navigate to: `http://localhost:5000`

## **💾 Chat History Features**

### **Automatic Session Storage**
- Every chat conversation is automatically saved to disk
- Sessions persist across server restarts
- Each user gets a unique session ID
- Messages include timestamps

### **Admin Interface**
Access the admin panel at: `http://localhost:5000/admin`

Features:
- 📊 View all chat sessions
- 📖 Read full conversation history
- 🗑️ Delete specific sessions
- 📈 Session statistics
- 🔄 Real-time updates

### **Command Line Management**
Use the session manager utility:

```bash
# Interactive mode
python manage_sessions.py

# Command line mode
python manage_sessions.py list
python manage_sessions.py view <session_id>
python manage_sessions.py delete <session_id>
python manage_sessions.py cleanup 30
python manage_sessions.py stats
```

### **Storage Location**
Chat sessions are stored in the `chat_sessions/` directory:
```
chat_sessions/
├── session_abc123.json
├── session_def456.json
└── session_ghi789.json
```

Each file contains:
- Session metadata (creation time, message count)
- Complete message history with timestamps
- User and assistant messages

## **🔧 Troubleshooting**

### **If you still get "Error talking to server":**

1. **Check if server is running:**
   - Look for the startup messages in your terminal
   - Make sure no other process is using port 5000

2. **Check browser console:**
   - Press F12 → Console tab
   - Look for any JavaScript errors

3. **Check server logs:**
   - Look at the terminal where you ran `python app.py`
   - Check for any error messages

4. **Test with curl:**
   ```bash
   curl -X POST http://localhost:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"query":"Hello"}'
   ```

### **Common Issues:**

- **Port already in use:** Change `PORT=5001` in your `.env` file
- **API key missing:** Set `OPENROUTER_API_KEY` in your `.env` file
- **Module import errors:** Make sure all Python files are in the same directory
- **Chat history not saving:** Check if `chat_sessions/` directory exists and is writable

## **📁 File Structure**
```
gyan-chatbot-main/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── chat_history.py     # Chat session storage manager
├── manage_sessions.py  # Command-line session manager
├── ai_response.py      # AI service integration
├── automation.py       # School data handling
├── conclave_response.py # Conclave data handling
├── requirements.txt    # Python dependencies
├── test_server.py      # Server testing script
├── static/
│   ├── script.js       # Frontend JavaScript
│   └── style.css       # Frontend styling
├── templates/
│   ├── index.html      # Main HTML template
│   └── admin.html      # Admin interface
└── chat_sessions/      # Chat history storage (auto-created)
```

## **🎯 What Was Fixed**

1. **Removed duplicate Flask routes** that were causing conflicts
2. **Cleaned up JavaScript** to prevent multiple event listeners
3. **Added proper error handling** in both frontend and backend
4. **Centralized configuration** for easier management
5. **Added server validation** to catch startup issues early
6. **Improved error messages** to help with debugging
7. **Added persistent chat history** storage system
8. **Created admin interface** for session management
9. **Added command-line tools** for session management

## **🚀 Next Steps**

After following this setup guide:
1. Your chatbot should work without the "Error talking to server" message
2. You can test with questions about school data or general queries
3. AI responses will work if you have a valid OpenRouter API key
4. Voice input and text-to-speech should function properly
5. **All chat conversations will be automatically saved**
6. **You can view and manage chat sessions via the admin interface**
7. **Use command-line tools to manage sessions programmatically**

## **🔧 Advanced Features**

### **Session Cleanup**
Automatically clean up old sessions:
```bash
python manage_sessions.py cleanup 7  # Remove sessions older than 7 days
```

### **Session Export**
View detailed session information:
```bash
python manage_sessions.py view <session_id>
```

### **Statistics**
Get overview of all sessions:
```bash
python manage_sessions.py stats
```

If you encounter any issues, check the troubleshooting section above or run the test script to diagnose problems.
