import json
import os
import difflib

def get_school_info(query):
    try:
        base_path = os.path.dirname(__file__)

        with open(os.path.join(base_path, "school_data.json")) as f:
            school_data = json.load(f)
        with open(os.path.join(base_path, "conclave_data.json")) as f:
            conclave_data = json.load(f)

        def normalize(text):
            text = text.lower().replace("-", "").replace(" ", "")
            num_map = {
                "first": "1", "1st": "1", "one": "1",
                "second": "2", "2nd": "2", "two": "2",
                "third": "3", "3rd": "3", "three": "3",
                "fourth": "4", "4th": "4", "four": "4",
                "fifth": "5", "5th": "5", "five": "5",
                "sixth": "6", "6th": "6", "six": "6",
                "seventh": "7", "7th": "7", "seven": "7",
                "eighth": "8", "8th": "8", "eight": "8",
                "ninth": "9", "9th": "9", "nine": "9",
                "tenth": "10", "10th": "10", "ten": "10",
                "eleventh": "11", "11th": "11", "eleven": "11",
                "twelfth": "12", "12th": "12", "twelve": "12"
            }
            for word, digit in num_map.items():
                if word in text:
                    text = text.replace(word, digit)
            return text

        query_lower = query.lower()
        norm_query = normalize(query)

        # Locations
        for key, value in school_data.get("locations", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
                if isinstance(value, list):
                    return f"The location of {key} is: {', '.join(value)}."
                else:
                    return f"The location of {key} is: {value}."

        # Infrastructure
        for key, value in school_data.get("infrastructure", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
                return f"{key}: {value}"

        # Co-curricular
        for key, value in school_data.get("co_curricular", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
                return f"{key}: {value}"

        # Mission & Vision
        mv = school_data.get("mission_vision", {})
        if "vision" in query_lower:
            return f"Our vision: {mv.get('vision')}"
        elif "mission" in query_lower:
            return f"Our mission: {mv.get('mission')}"
        elif "core values" in query_lower or "values" in query_lower:
            return "Our core values: " + ", ".join(mv.get("core_values", []))

        # Staff
        staff = school_data.get("staff", {})
        if "contactdetails" in norm_query:
            return "Contact Details:\n" + "\n".join(staff.get("contact details", []))
        if "assistantviceprincipal" in norm_query:
            return f"The Assistant Vice Principal is {staff.get('assistant vice principal')}"
        if "viceprincipal" in norm_query:
            return f"The Vice Principal is {staff.get('vice principal')}"
        if "principal" in norm_query:
            return f"The Principal is {staff.get('principal')}"
        if "coordinator" in norm_query:
            return f"The School Co-ordinator is {staff.get('school co-ordinator')}"
        if "outsideschoolincharge" in norm_query:
            return f"The Outside School Incharge is {staff.get('outside school incharge')}"
        if "eventincharge" in norm_query:
            return f"The Events Incharge is {staff.get('events incharge')}"
        if "registrationincharge" in norm_query:
            return f"The Registration Incharge is {staff.get('registration incharge')}"
        if "vicecaptain" in norm_query:
            return f"The School Vice Captain is {staff.get('school vice captain')}"
        if "captain" in norm_query and "vice" not in norm_query:
            return f"The School Captain is {staff.get('school captain')}"
        if "studentvolunteer" in norm_query or "volunteer" in norm_query:
            return "Volunteers: " + ", ".join(staff.get("student volunteers", []))
        if "teacher" in norm_query or "staff" in norm_query:
            return staff.get("teaching_staff_overview", "")
        if "faculty" in norm_query:
            return "Key faculty: " + ", ".join(staff.get("key_faculty_members", []))
        if "teachertraining" in norm_query:
            return staff.get("facilities_for_teacher_training", "")
        if "developer" in norm_query or "ekanshgarg" in norm_query:
            dev = staff.get("chatbot-developer", {})
            return f"Chatbot Developer: {dev.get('name')} ({dev.get('email')})"

        # Conclave events
        for event_key, event_data in conclave_data.items():
            if (
                event_key.lower() in query_lower
                or normalize(event_key) in norm_query
                or event_data["event_name"].lower() in query_lower
                or normalize(event_data["event_name"]) in norm_query
            ):
                return f"{event_data['event_name']} ({event_data['class_range']}): {event_data['description']}"

        return None
    except Exception as e:
        print("Error:", e)
        return None
