import json

# Load Conclave data once
try:
    with open("conclave_data.json", "r", encoding="utf-8") as file:
        conclave_data = json.load(file)
except Exception as e:
    conclave_data = {}
    print(f"❌ Error loading Conclave JSON: {e}")


def answer_conclave_query(query: str):
    query = query.lower().strip()
    print(f"🎤 Conclave query: '{query}'")

    # Define keyword groups
    keywords = {
        "rules": ["rules", "instructions", "regulations", "guidelines"],
        "prizes": ["prizes", "awards", "recognition", "winner", "reward"],
        "timing": ["time", "date", "schedule", "when", "timing", "duration", "its timing", "when is it"],
        "venue": ["venue", "location", "place", "hall", "where"],
        "format": ["format", "structure", "rounds", "how", "process"],
        "description": ["description", "what is", "summary", "details", "about", "tell me"],
        "participants": ["who", "participants", "eligibility", "classes", "students", "can participate"],
        "registration": ["registration", "register", "deadline", "apply", "entry"]
    }

    # 🔍 Step 1: Try to find event match
    matched_event = None
    for key, data in conclave_data.items():
        event_name = data.get("event_name", "").lower()
        if key.lower() in query or event_name in query:
            matched_event = data
            break

    # Step 2: Context-based matching if no direct match
    if not matched_event:
        query_words = query.split()
        for key, data in conclave_data.items():
            event_name = data.get("event_name", "").lower()
            event_words = event_name.split()
            key_words = key.split()
            for word in query_words:
                if len(word) > 2:
                    if word in event_words or word in key_words:
                        matched_event = data
                        break
            if matched_event:
                break

    # Step 3: Return info if event matched
    if matched_event:
        for section, triggers in keywords.items():
            if any(word in query for word in triggers):
                return format_specific_section(matched_event, section)
        return format_full_summary(matched_event)  # default summary

    # Step 4: No match found
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
        venue = (
            data.get("venue")
            or data.get("location")
            or data.get("place")
            or data.get("hall")
            or "venue details not available"
        )
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
    venue = (
        data.get("venue")
        or data.get("location")
        or data.get("place")
        or data.get("hall")
        or "N/A"
    )

    lines = [
        f"📌 {data['event_name']} (Classes {data.get('class_range', 'N/A')})",
        f"🗓️ {data['day']} | ⏰ {data['timing']} | ⏳ Duration: {data.get('duration', 'N/A')}",
        f"📍 Venue: {venue}",
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
