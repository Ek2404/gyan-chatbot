import json

# Load Conclave data once
try:
    with open("conclave_data.json", "r", encoding="utf-8") as file:
        conclave_data = json.load(file)
except Exception as e:
    conclave_data = {}
    print(f"❌ Error loading Conclave JSON: {e}")

def answer_conclave_query(query):
    query = query.lower().strip()

    # Define keyword groups
    keywords = {
        "rules": ["rules", "instructions", "regulations", "guidelines"],
        "prizes": ["prizes", "awards", "recognition", "winner"],
        "timing": ["time", "date", "schedule", "when"],
        "format": ["format", "structure", "rounds"],
        "description": ["description", "what is", "summary", "details", "about"]
    }

    # Try matching an event
    for key, data in conclave_data.items():
        if key in query:
            # Determine intent
            for section, triggers in keywords.items():
                if any(word in query for word in triggers):
                    return format_specific_section(data, section)

            # Default: return full summary
            return format_full_summary(data)

    return None  # No matching event

def format_specific_section(data, section):
    if section == "rules":
        return f"📖 Rules for {data['event_name']}:\n" + "\n".join(f"• {r}" for r in data["rules"])
    elif section == "prizes":
        return f"🏆 Prizes for {data['event_name']}:\n" + "\n".join(f"• {p}" for p in data["prizes"])
    elif section == "timing":
        return f"📅 {data['event_name']} is scheduled on {data['day']} at {data['timing']}."
    elif section == "format":
        return f"🎯 Format of {data['event_name']}:\n{data['format']}"
    elif section == "description":
        return f"ℹ️ About {data['event_name']}:\n{data['description']}"
    else:
        return None

def format_full_summary(data):
    lines = [
        f"📌 {data['event_name']} (Classes {data['class_range']})",
        f"🗓️ {data['day']} | ⏰ {data['timing']}",
        f"🎯 Format: {data['format']}",
        "",
        f"ℹ️ {data['description']}",
        "",
        "📖 Sample Rules:",
    ] + [f"• {rule}" for rule in data.get("rules", [])[:3]] + [
        "...",
        "",
        f"🏆 Awards: {', '.join(data.get('prizes', [])[:2])}..."
    ]
    return "\n".join(lines)
