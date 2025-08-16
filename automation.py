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

        # Normalization helper (removes spaces, dashes, lowercase)
        def normalize(text):
            return text.lower().replace("-", "").replace(" ", "")

        query_lower = query.lower()
        norm_query = normalize(query)
        print(f"📚 School/Conclave query: '{query}'")

        # -----------------------------
        # 1. School Info Section
        # -----------------------------
        # Match location
        for key, value in school_data.get("locations", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
                return f"The location of {key} is as follows: {value}."

        # Infrastructure
        for key, value in school_data.get("infrastructure", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
                return f"{key}: {value}"

        # Co-curricular
        for key, value in school_data.get("co_curricular", {}).items():
            if key.lower() in query_lower or normalize(key) in norm_query:
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

        if "contactdetails" in norm_query:
            contacts = staff.get("contact details", [])
            if contacts:
                return "Contact Details:\n" + "\n".join(contacts)
            else:
                return "No contact details found."

        # ✅ Specific before generic
        if "assistantviceprincipal" in norm_query or "asstviceprincipal" in norm_query:
            return f"The Assistant Vice Principal is {staff.get('assistant vice principal')}"
        elif "viceprincipal" in norm_query:
            return f"The Vice Principal is {staff.get('vice principal')}"
        elif "principal" in norm_query:
            return f"The Principal is {staff.get('principal')}"
        elif "coordinator" in norm_query or "coordinator" in query_lower:
            return f"The School Co-ordinator is {staff.get('school co-ordinator')}"
        elif "outsideschoolincharge" in norm_query:
            return f"The Outside School Incharge is {staff.get('outside school incharge')}"
        elif "eventincharge" in norm_query or "eventsincharge" in norm_query:
            return f"The Events Incharge is {staff.get('events incharge')}"
        elif "registrationincharge" in norm_query:
            return f"The Registration Incharge is {staff.get('registration incharge')}"
        elif "schoolvicecaptain" in norm_query or "vicecaptain" in norm_query:
            return f"The School Vice Captain is {staff.get('school vice captain')}"
        elif "schoolcaptain" in norm_query or ("captain" in norm_query and "vice" not in norm_query):
            return f"The School Captain is {staff.get('school captain')}"

        elif (
            "studentvolunteer" in norm_query
            or "volunteer" in norm_query
            or "studenthelper" in norm_query
            or "studentassistant" in norm_query
            or "studentsupport" in norm_query
        ):
            volunteers = staff.get("student volunteers", [])
            emails = staff.get("student volunteers email ids", [])
            if volunteers:
                info = "Student Volunteers: " + ", ".join(volunteers)
                if emails:
                    info += "\nEmails: " + ", ".join(emails)
                return info
            else:
                return "No student volunteers found."

        elif "teachers" in query_lower or "staff" in query_lower:
            return staff.get("teaching_staff_overview", "")
        elif "seniorteacher" in norm_query or "faculty" in norm_query:
            return "Key faculty members include: " + ", ".join(staff.get("key_faculty_members", []))
        elif "teachertraining" in norm_query:
            return staff.get("facilities_for_teacher_training", "")
        elif "chatbotdeveloper" in norm_query or "developer" in norm_query or "ekanshgarg" in norm_query:
            dev = staff.get("chatbot-developer", {})
            name = dev.get("name", "Ekansh Garg")
            email = dev.get("email", "ekansh.6874@birlaschoolkalyan.com")
            return f"Chatbot Developer: {name} ({email})"

        # -----------------------------
        # 2. Conclave Events Section
        # -----------------------------
        for event_key, event_data in conclave_data.items():
            if (
                event_key.lower() in query_lower
                or normalize(event_key) in norm_query
                or event_data["event_name"].lower() in query_lower
                or normalize(event_data["event_name"]) in norm_query
            ):
                # Venue/location/where queries
                if (
                    "venue" in query_lower
                    or "location" in query_lower
                    or "where" in query_lower
                    or "place" in query_lower
                    or "hall" in query_lower
                ):
                    venue = (
                        event_data.get("venue")
                        or event_data.get("location")
                        or event_data.get("place")
                        or event_data.get("hall")
                        or "Venue details not available."
                    )
                    return f"Venue for {event_data['event_name']}: {venue}"

                # Timing
                elif "time" in query_lower or "timing" in query_lower or "schedule" in query_lower:
                    return f"{event_data['event_name']} will be held on {event_data['day']} at {event_data['timing']} in {event_data['venue']}."

                # Rules
                elif "rule" in query_lower:
                    return f"Rules for {event_data['event_name']}: " + "; ".join(event_data["rules"])

                # Prizes
                elif "prize" in query_lower or "award" in query_lower:
                    return f"Prizes for {event_data['event_name']}: " + ", ".join(event_data["prizes"])

                # General info
                else:
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
