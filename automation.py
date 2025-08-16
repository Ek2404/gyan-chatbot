import json
import os
import re

# Load school data
def get_school_info(query):
    try:
        with open(os.path.join(os.path.dirname(__file__), "school_data.json"), encoding="utf-8") as f:
            data = json.load(f)
        
        query_lower = query.lower().strip()
        print(f"📚 School info query: '{query}'")

        # --- Helper normalize function ---
        def normalize(text):
            return re.sub(r'[^a-z0-9 ]', '', text.lower().strip())

        query_norm = normalize(query)

        # --- Function to check fuzzy match ---
        def fuzzy_match(key, query):
            key_norm = normalize(key)
            return key_norm in query or query in key_norm

        # 1. Match location
        for key, value in data.get("locations", {}).items():
            if fuzzy_match(key, query_norm):
                print(f"✅ Found location match: {key}")
                return f"The location of {key} is {value}."

        # 2. Match infrastructure
        for key, value in data.get("infrastructure", {}).items():
            if fuzzy_match(key, query_norm):
                print(f"✅ Found infrastructure match: {key}")
                return f"{key}: {value}"

        # 3. Match co-curricular
        for key, value in data.get("co_curricular", {}).items():
            if fuzzy_match(key, query_norm):
                print(f"✅ Found co-curricular match: {key}")
                return f"{key}: {value}"

        # 4. Match mission & vision
        mv = data.get("mission_vision", {})
        if "vision" in query_norm:
            print("✅ Found vision match")
            return f"Our vision: {mv.get('vision')}"
        elif "mission" in query_norm:
            print("✅ Found mission match")
            return f"Our mission: {mv.get('mission')}"
        elif "core values" in query_norm or "values" in query_norm:
            print("✅ Found core values match")
            return "Our core values include: " + ", ".join(mv.get("core_values", []))

        # 5. Match staff queries (FULLY FLEXIBLE 🚀)
        staff = data.get("staff", {})
        for key, value in staff.items():
            if isinstance(value, (str, list)):
                if fuzzy_match(key, query_norm):
                    print(f"✅ Found staff match: {key}")
                    if isinstance(value, list):
                        return f"{key.title()}: {', '.join(value)}"
                    return f"{key.title()}: {value}"

        print("❌ No school info match found")
        return None

    except Exception as e:
        print("Error loading school data:", e)
        return None
