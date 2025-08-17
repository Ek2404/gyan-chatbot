import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Optional

def _iso_utc_now() -> str:
    # Always store timestamps in UTC with Z
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _has_tz(ts: str) -> bool:
    return ts.endswith("Z") or ("+" in ts[-6:] or "-" in ts[-6:])

def _as_utc_string(ts: str) -> str:
    # For old records that lack timezone, assume they were UTC and mark as Z
    if not ts:
        return _iso_utc_now()
    if _has_tz(ts):
        return ts
    # Trim microseconds if present, then append Z
    try:
        # Try parsing naive ISO and set UTC
        dt = datetime.fromisoformat(ts.split("Z")[0])
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except Exception:
        # Fallback: just append Z
        return ts.split(".")[0] + "Z"

class ChatHistoryManager:
    def __init__(self, storage_dir="chat_sessions"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir()
    
    def ensure_storage_dir(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            print(f"✅ Created chat storage directory: {self.storage_dir}")
    
    def get_session_file_path(self, session_id: str) -> str:
        return os.path.join(self.storage_dir, f"session_{session_id}.json")
    
    def save_message(self, session_id: str, role: str, content: str) -> bool:
        try:
            history = self.load_session_history(session_id)

            message = {
                "role": role,
                "content": content,
                "timestamp": _iso_utc_now()   # ✅ UTC with Z
            }
            history.append(message)
            
            return self.save_session_history(session_id, history)
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            return False
    
    def save_session_history(self, session_id: str, history: List[Dict]) -> bool:
        try:
            file_path = self.get_session_file_path(session_id)

            # Preserve existing created_at if the file already exists
            created_at = _iso_utc_now()
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    created_at = _as_utc_string(existing.get("created_at")) or created_at
                except Exception:
                    pass  # if anything fails, keep the fresh created_at

            # Normalize any old message timestamps (no tz -> add Z)
            for m in history:
                if isinstance(m, dict) and "timestamp" in m:
                    m["timestamp"] = _as_utc_string(m.get("timestamp"))

            last_msg_text = ""
            if history:
                last_msg_text = (history[-1].get("content") or "").strip()
                if len(last_msg_text) > 140:
                    last_msg_text = last_msg_text[:137] + "..."

            session_data = {
                "session_id": session_id,
                "created_at": created_at,                    # ✅ preserved
                "last_updated": _iso_utc_now(),              # ✅ UTC with Z
                "message_count": len(history),
                "last_message": last_msg_text,               # ✅ handy for admin preview
                "messages": history
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving session history: {e}")
            return False
    
    def load_session_history(self, session_id: str) -> List[Dict]:
        try:
            file_path = self.get_session_file_path(session_id)
            if not os.path.exists(file_path):
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            messages = session_data.get("messages", [])
            # Normalize timestamps on load (helps old files)
            for m in messages:
                if "timestamp" in m:
                    m["timestamp"] = _as_utc_string(m.get("timestamp"))
            return messages
        except Exception as e:
            print(f"❌ Error loading session history: {e}")
            return []
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        try:
            file_path = self.get_session_file_path(session_id)
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            return {
                "session_id": session_data.get("session_id"),
                "created_at": _as_utc_string(session_data.get("created_at")),
                "last_updated": _as_utc_string(session_data.get("last_updated")),
                "message_count": session_data.get("message_count", 0),
                "last_message": session_data.get("last_message", "")
            }
        except Exception as e:
            print(f"❌ Error getting session info: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
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
        sessions = []
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("session_") and filename.endswith(".json"):
                    session_id = filename[8:-5]
                    info = self.get_session_info(session_id)
                    if info:
                        sessions.append(info)
            sessions.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
        except Exception as e:
            print(f"❌ Error listing sessions: {e}")
        return sessions
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)
        deleted = 0
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("session_") and filename.endswith(".json"):
                    p = os.path.join(self.storage_dir, filename)
                    mtime = datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc)
                    if mtime < cutoff:
                        os.remove(p)
                        deleted += 1
                        print(f"🗑️  Cleaned up old session: {filename}")
            if deleted:
                print(f"✅ Cleaned up {deleted} old sessions")
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")
        return deleted

# Global instance
chat_manager = ChatHistoryManager()
