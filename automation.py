import json
import os

# Load school + conclave data
def get_school_info(query):
    try:
        base_path = os.path.dirname(__file__)

        # Load school data
        with open(os.path.join(base_path, "school_data.json")) as f:
            school_data = json.load(f)

        # Load conclave data
        with open(os.path.join(base_path, "conclave_data.json")) as f:
            conclave_data = json.load(f)

        query_lower = query.lower()
        print(f"📚 School/Conclave query: '{query}'")

        # -----------------------------
        # 1. School Info Section
        # -----------------------------
        # Match location
        for key, value in school_data.get("locations", {}).items():
            if key.lower() in query_lower or query_lower in key.lower():
                return f"The location of {key} is as follows: {value}."

        # Infrastructure
        for key, value in school_data.get("infrastructure", {}).items():
            if key.lower() in query_lower:
                return f"{key}: {value}"

        # Co-curricular
        for key, value in school_data.get("co_curricular", {}).items():
            if key.lower() in query_lower:
                return f"{key} activity: {value}"

        # Mission & Vision
        mv = school_data.get("mission_vision", {})
        if "vision" in query_lower:
            return f"Our vision: {mv.get('vision')}"
        elif "mission" in query_lower:
            return f"Our mission: {mv.get('mission')}"
        elif "core values" in query_lower or "values" in query_lower:
            return "Our core values include: " + ", ".join(mv.get("core_values", []))

        # Staff queries
        staff = school_data.get("staff", {})
        if "principal" in query_lower:
            return f"The principal is {staff.get('principal')}"
        elif "teachers" in query_lower or "staff" in query_lower:
            return staff.get("teaching_staff_overview", "")
        elif "senior teacher" in query_lower or "faculty" in query_lower:
            return "Key faculty members include: " + ", ".join(staff.get("key_faculty_members", []))
        elif "teacher training" in query_lower:
            return staff.get("facilities_for_teacher_training", "")

        # -----------------------------
        # 2. Conclave Events Section
        # -----------------------------
        for event_key, event_data in conclave_data.items():
            # Match event name
            if event_key.lower() in query_lower or event_data["event_name"].lower() in query_lower:
                # Venue/location/where queries
                if "venue" in query_lower or "location" in query_lower or "where" in query_lower or "place" in query_lower or "hall" in query_lower:
                    venue = event_data.get("venue") or event_data.get("location") or event_data.get("place") or event_data.get("hall") or "Venue details not available."
                    return f"Venue for {event_data['event_name']}: {venue}"

                # If user asked about timing
                elif "time" in query_lower or "timing" in query_lower or "schedule" in query_lower:
                    return f"{event_data['event_name']} will be held on {event_data['day']} at {event_data['timing']} in {event_data['venue']}."

                # If user asked about rules
                elif "rule" in query_lower:
                    return f"Rules for {event_data['event_name']}: " + "; ".join(event_data["rules"])

                # If user asked about prizes
                elif "prize" in query_lower or "award" in query_lower:
                    return f"Prizes for {event_data['event_name']}: " + ", ".join(event_data["prizes"])

                # Otherwise general info
                else:
                    # Fallback: if event has venue, append it to general info
                    venue = event_data.get("venue")
                    if venue:
                        return f"{event_data['event_name']} ({event_data['class_range']}): {event_data['description']}\nVenue: {venue}"
                    else:
                        return f"{event_data['event_name']} ({event_data['class_range']}): {event_data['description']}"

        # -----------------------------
        # 3. No match
        # -----------------------------
        print("❌ No school/conclave match found")
        return None

    except Exception as e:
        print("Error loading data:", e)
        return None
