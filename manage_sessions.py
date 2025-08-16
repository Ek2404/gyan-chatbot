#!/usr/bin/env python3
"""
Command-line utility to manage chat sessions
"""

import os
import sys
import json
from datetime import datetime
from chat_history import chat_manager

def print_header():
    print("=" * 60)
    print("💬 GYAN Chatbot - Session Manager")
    print("=" * 60)

def list_sessions():
    """List all chat sessions"""
    print("\n📋 Listing all chat sessions...")
    
    try:
        sessions = chat_manager.list_all_sessions()
        
        if not sessions:
            print("No chat sessions found.")
            return
        
        for i, session in enumerate(sessions, 1):
            print(f"\n{i}. Session ID: {session['session_id']}")
            print(f"   Created: {format_date(session.get('created_at'))}")
            print(f"   Last Updated: {format_date(session.get('last_updated'))}")
            print(f"   Messages: {session.get('message_count', 0)}")
            
            if session.get('note'):
                print(f"   Note: {session['note']}")
    
    except Exception as e:
        print(f"❌ Error listing sessions: {e}")

def view_session(session_id):
    """View detailed history of a specific session"""
    print(f"\n📖 Viewing session: {session_id}")
    
    try:
        history = chat_manager.load_session_history(session_id)
        
        if not history:
            print("No messages found for this session.")
            return
        
        print(f"Total messages: {len(history)}")
        print("-" * 40)
        
        for i, message in enumerate(history, 1):
            timestamp = format_date(message.get('timestamp'))
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            
            print(f"\n{i}. [{timestamp}] {role.upper()}:")
            print(f"   {content}")
    
    except Exception as e:
        print(f"❌ Error viewing session: {e}")

def delete_session(session_id):
    """Delete a specific session"""
    print(f"\n🗑️  Deleting session: {session_id}")
    
    try:
        if chat_manager.delete_session(session_id):
            print("✅ Session deleted successfully!")
        else:
            print("❌ Session not found or could not be deleted.")
    
    except Exception as e:
        print(f"❌ Error deleting session: {e}")

def cleanup_old_sessions(days=30):
    """Clean up old sessions"""
    print(f"\n🧹 Cleaning up sessions older than {days} days...")
    
    try:
        deleted_count = chat_manager.cleanup_old_sessions(days)
        print(f"✅ Cleaned up {deleted_count} old sessions.")
    
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def show_stats():
    """Show session statistics"""
    print("\n📊 Session Statistics")
    
    try:
        sessions = chat_manager.list_all_sessions()
        
        total_sessions = len(sessions)
        total_messages = sum(session.get('message_count', 0) for session in sessions)
        
        print(f"Total Sessions: {total_sessions}")
        print(f"Total Messages: {total_messages}")
        
        if sessions:
            # Find oldest and newest sessions
            dates = [session.get('created_at') for session in sessions if session.get('created_at')]
            if dates:
                oldest = min(dates)
                newest = max(dates)
                print(f"Oldest Session: {format_date(oldest)}")
                print(f"Newest Session: {format_date(newest)}")
    
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")

def format_date(date_string):
    """Format date string for display"""
    if not date_string:
        return "N/A"
    
    try:
        date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return date_string

def show_help():
    """Show help information"""
    print("\n📖 Available Commands:")
    print("  list                    - List all chat sessions")
    print("  view <session_id>       - View detailed history of a session")
    print("  delete <session_id>     - Delete a specific session")
    print("  cleanup [days]          - Clean up old sessions (default: 30 days)")
    print("  stats                   - Show session statistics")
    print("  help                    - Show this help message")
    print("  exit                    - Exit the program")
    print("\nExamples:")
    print("  python manage_sessions.py list")
    print("  python manage_sessions.py view abc123")
    print("  python manage_sessions.py cleanup 7")

def main():
    print_header()
    
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1].lower()
        
        if command == "list":
            list_sessions()
        elif command == "view" and len(sys.argv) > 2:
            view_session(sys.argv[2])
        elif command == "delete" and len(sys.argv) > 2:
            delete_session(sys.argv[2])
        elif command == "cleanup":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            cleanup_old_sessions(days)
        elif command == "stats":
            show_stats()
        elif command == "help":
            show_help()
        else:
            print("❌ Invalid command or missing arguments.")
            show_help()
    else:
        # Interactive mode
        print("\n💡 Tip: Use 'help' to see available commands")
        print("💡 Tip: Use 'exit' to quit")
        
        while True:
            try:
                command = input("\n🔧 Enter command: ").strip().lower()
                
                if command == "exit" or command == "quit":
                    print("👋 Goodbye!")
                    break
                elif command == "help":
                    show_help()
                elif command == "list":
                    list_sessions()
                elif command.startswith("view "):
                    session_id = command[5:].strip()
                    view_session(session_id)
                elif command.startswith("delete "):
                    session_id = command[7:].strip()
                    delete_session(session_id)
                elif command.startswith("cleanup"):
                    parts = command.split()
                    days = int(parts[1]) if len(parts) > 1 else 30
                    cleanup_old_sessions(days)
                elif command == "stats":
                    show_stats()
                elif command == "":
                    continue
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
