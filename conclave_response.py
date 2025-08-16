import json

# Load Conclave data once
try:
    with open("conclave_data.json", "r", encoding="utf-8") as file:
        conclave_data = json.load(file)
    print("✅ Conclave data loaded successfully")
except Exception as e:
    conclave_data = {}
    print(f"❌ Error loading Conclave JSON: {e}")


def answer_conclave_query(query: str):
    """Answer queries related to Conclave events"""
    query = query.lower().strip()
    print(f"🎤 Conclave query: '{query}'")

    # Keyword groups
    keywords = {
        "rules": ["rules", "instructions", "regulations", "guidelines"],
        "prizes": ["prizes", "awards", "recognition", "winner", "reward"],
        "timing": ["time", "date", "schedule", "when", "timing", "duration"],
        "venue": ["venue", "location", "place", "hall"],
        "format": ["format", "structure", "rounds", "how", "process"],
        "description": ["description", "what is", "summary", "details", "about", "tell me"],
        "participants": ["who", "participants", "eligibility", "classes", "students"],
        "registration": ["registration", "register", "deadline", "apply", "entry"]
    }

    # --- STEP 1: Try to find a matching event ---
    matched_event = None
    for key, data in conclave_data.items():
        event_name = data.get("event_name", "").lower()

        if key.lower() in query or event_name in query:
            matched_event = data
            print(f"🎯 Matched event: {event_name}")
            break

    # If no direct match → fuzzy word matching
    if not matched_event:
        query_words = query.split()
        for key, data in conclave_data.items():
            event_name = data.get("event_name", "").lower()
            event_words = event_name.split()
            key_words = key.split()

            for word in query_words:
                if len(word) > 2:  # avoid matching short words
                    if word in event_words or word in key_words:
                        matched_event = data
                        print(f"🎯 Context match found: {event_name} via '{word}'")
                        break
            if matched_event:
                break

    # --- STEP 2: Return the requested section ---
    if matched_event:
        for section, triggers in keywords.items():
            if any(word in query for word in triggers):
                result = format_specific_section(matched_event, section)
                if result:
                    print(f"✅ Returning {section} for {matched_event['event_name']}")
                    return result

        # Default → full summary
        return format_full_summary(matched_event)

    # --- STEP 3: No match found ---
    print("❌ No matching event found for query")
    return None


def format_specific_section(data, section: str):
    """Format response for a specific section of event data"""
    if section == "rules":
        return f"📖 Rules for {data['event_name']}:\n" + "\n".join(f"• {r}" for r in data.get("rules", []))

    elif section == "prizes":
        return f"🏆 Prizes for {data['event_name']}:\n" + "\n".join(f"• {p}" for p in data.get("prizes", []))

    elif section == "timing":
        duration = data.get("duration", "N/A")
        return f"📅 {data['event_name']} is scheduled on {data['day']} at {data['timing']} (Duration: {duration})."

    elif section == "venue":
        venue = data.get("venue", "venue details not available")
        return f"📍 Venue for {data['event_name']}: {venue}"

    elif section == "format":
        return f"🎯 Format of {data['event_name']}:\n{data.get('format', 'N/A')}"

    elif section == "description":
        return f"ℹ️ About {data['event_name']}:\n{data.get('description', 'N/A')}"

    elif section == "participants":
        return f"👥 Eligible participants for {data['event_name']}: {data.get('class_range', 'N/A')}"

    elif section == "registration":
        deadline = data.get("registration_deadline")
        if deadline:
            return f"📝 Registration for {data['event_name']} closes on {deadline}."
        return f"📝 Registration details for {data['event_name']} are not available. Please contact the coordinator."

    return None


def format_full_summary(data):
    """Default: Return a summary of event"""
    lines = [
        f"📌 {data['event_name']} (Classes {data.get('class_range', 'N/A')})",
        f"🗓️ {data['day']} | ⏰ {data['timing']} | ⏳ Duration: {data.get('duration', 'N/A')}",
        f"📍 Venue: {data.get('venue', 'N/A')}",
        "",
        f"ℹ️ {data.get('description', 'N/A')}",
        "",
        "📖 Rules (sample):",
    ] + [f"• {rule}" for rule in data.get("rules", [])[:3]] + [
        "...",
        "",
        f"🏆 Awards: {', '.join(data.get('prizes', [])[:2])}..."
    ]
    return "\n".join(lines)
