import json
import os
import difflib

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

        # -----------------------------
        # Normalization helper
        # -----------------------------
        def normalize(text):
            text = text.lower().replace("-", "").replace(" ", "")

            # Number & ordinal mapping
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
        print(f"📚 School/Conclave query: '{query}' → '{norm_query}'")

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
        event_keys = list(conclave_data.keys())
        event_names = [event_data["event_name"] for event_data in conclave_data.values()]

        matched_event = None

        # Direct/normalized match
        for event_key, event_data in conclave_data.items():
            if (
                event_key.lower() in query_lower
                or normalize(event_key) in norm_query
                or event_data["event_name"].lower() in query_lower
                or normalize(event_data["event_name"]) in norm_query
            ):
                matched_event = event_data
                break

        # Fuzzy match (only if user likely meant an event)
        if not matched_event:
            all_names = event_keys + event_names
            close_matches = difflib.get_close_matches(query, all_names, n=1, cutoff=0.7)
            if close_matches:
                for event_key, event_data in conclave_data.items():
                    if (
                        close_matches[0].lower() == event_key.lower()
                        or close_matches[0].lower() == event_data["event_name"].lower()
                    ):
                        matched_event = event_data
                        break

        if matched_event:
            # Venue/location/where queries
            if any(word in query_lower for word in ["venue", "location", "where", "place", "hall"]):
                venue = (
                    matched_event.get("venue")
                    or matched_event.get("location")
                    or matched_event.get("place")
                    or matched_event.get("hall")
                    or "Venue details not available."
                )
                return f"Venue for {matched_event['event_name']}: {venue}"

            # Timing
            elif any(word in query_lower for word in ["time", "timing", "schedule", "when"]):
                return f"{matched_event['event_name']} will be held on {matched_event['day']} at {matched_event['timing']} in {matched_event['venue']}."

            # Rules
            elif "rule" in query_lower:
                return f"Rules for {matched_event['event_name']}: " + "; ".join(matched_event["rules"])

            # Prizes
            elif any(word in query_lower for word in ["prize", "award"]):
                return f"Prizes for {matched_event['event_name']}: " + ", ".join(matched_event["prizes"])

            # General info
            else:
                venue = matched_event.get("venue")
                if venue:
                    return f"{matched_event['event_name']} ({matched_event['class_range']}): {matched_event['description']}\nVenue: {venue}"
                else:
                    return f"{matched_event['event_name']} ({matched_event['class_range']}): {matched_event['description']}"

        # -----------------------------
        # 3. No match → fallback
        # -----------------------------
        print("❌ No school/conclave match found → fallback to API")
        return None

    except Exception as e:
        print("Error loading data:", e)
        return None
