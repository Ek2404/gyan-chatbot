import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ChatHistoryManager:
    def __init__(self, storage_dir="chat_sessions"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir()
    
    def ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            print(f"✅ Created chat storage directory: {self.storage_dir}")
    
    def get_session_file_path(self, session_id: str) -> str:
        """Get the file path for a specific session"""
        return os.path.join(self.storage_dir, f"session_{session_id}.json")
    
    def save_message(self, session_id: str, role: str, content: str) -> bool:
        """Save a single message to the session history"""
        try:
            # Load existing history
            history = self.load_session_history(session_id)
            
            # Add new message with timestamp
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
            history.append(message)
            
            # Save back to file
            return self.save_session_history(session_id, history)
            
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            return False
    
    def save_session_history(self, session_id: str, history: List[Dict]) -> bool:
        """Save entire session history to file"""
        try:
            file_path = self.get_session_file_path(session_id)
            
            # Create session data with metadata
            session_data = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "message_count": len(history),
                "messages": history
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving session history: {e}")
            return False
    
    def load_session_history(self, session_id: str) -> List[Dict]:
        """Load session history from file"""
        try:
            file_path = self.get_session_file_path(session_id)
            
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            return session_data.get("messages", [])
            
        except Exception as e:
            print(f"❌ Error loading session history: {e}")
            return []
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get session metadata without loading all messages"""
        try:
            file_path = self.get_session_file_path(session_id)
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Return metadata only (exclude messages for performance)
            return {
                "session_id": session_data.get("session_id"),
                "created_at": session_data.get("created_at"),
                "last_updated": session_data.get("last_updated"),
                "message_count": session_data.get("message_count", 0)
            }
            
        except Exception as e:
            print(f"❌ Error getting session info: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session and its history"""
        try:
            file_path = self.get_session_file_path(session_id)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Deleted session: {session_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error deleting session: {e}")
            return False
    
    def list_all_sessions(self) -> List[Dict]:
        """List all available sessions with basic info"""
        sessions = []
        
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("session_") and filename.endswith(".json"):
                    session_id = filename[8:-5]  # Remove "session_" prefix and ".json" suffix
                    session_info = self.get_session_info(session_id)
                    if session_info:
                        sessions.append(session_info)
            
            # Sort by last updated (newest first)
            sessions.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
            
        except Exception as e:
            print(f"❌ Error listing sessions: {e}")
        
        return sessions
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Clean up sessions older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("session_") and filename.endswith(".json"):
                    file_path = os.path.join(self.storage_dir, filename)
                    
                    # Check file modification time
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_mtime < cutoff_date:
                        os.remove(file_path)
                        deleted_count += 1
                        print(f"🗑️  Cleaned up old session: {filename}")
            
            if deleted_count > 0:
                print(f"✅ Cleaned up {deleted_count} old sessions")
                
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")
        
        return deleted_count

# Global instance
chat_manager = ChatHistoryManager()
