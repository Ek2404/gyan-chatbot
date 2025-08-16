import json
import os

# Load school data
def get_school_info(query):
    try:
        with open(os.path.join(os.path.dirname(__file__), "school_data.json")) as f:
            data = json.load(f)
        
        query_lower = query.lower()

        # 1. Match location
        for key, value in data.get("locations", {}).items():
            if key.lower() in query_lower or query_lower in key.lower():
                return f"The location of {key} is as follows; {value}."

        # 2. Match infrastructure
        for key, value in data.get("infrastructure", {}).items():
            if key.lower() in query_lower:
                return f"{key}: {value}"

        # 3. Match co-curricular
        for key, value in data.get("co_curricular", {}).items():
            if key.lower() in query_lower:
                return f"{key} activity: {value}"

        # 4. Match mission & vision
        mv = data.get("mission_vision", {})
        if "vision" in query_lower:
            return f"Our vision: {mv.get('vision')}"
        elif "mission" in query_lower:
            return f"Our mission: {mv.get('mission')}"
        elif "core values" in query_lower or "values" in query_lower:
            return "Our core values include: " + ", ".join(mv.get("core_values", []))

        # 5. Match staff queries
        staff = data.get("staff", {})
        if "principal" in query_lower:
            return f"The principal is {staff.get('principal')}"
        elif "teachers" in query_lower or "staff" in query_lower:
            return staff.get("teaching_staff_overview", "")
        elif "senior teacher" in query_lower or "faculty" in query_lower:
            return "Key faculty members include: " + ", ".join(staff.get("key_faculty_members", []))
        elif "teacher training" in query_lower:
            return staff.get("facilities_for_teacher_training", "")

    except Exception as e:
        print("Error loading school data:", e)
    
    return None
