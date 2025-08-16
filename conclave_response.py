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
    
    print(f"🎤 Conclave query: '{query}'")

    # Define keyword groups with more specific triggers
    keywords = {
        "rules": ["rules", "instructions", "regulations", "guidelines"],
        "prizes": ["prizes", "awards", "recognition", "winner", "reward"],
        "timing": ["time", "date", "schedule", "when", "timing", "duration", "its timing", "when is it"],
        "format": ["format", "structure", "rounds", "how", "process"],
        "description": ["description", "what is", "summary", "details", "about", "tell me"],
        "participants": ["who", "participants", "eligibility", "classes", "students", "can participate"],
        "registration": ["registration", "register", "deadline", "apply", "entry"]
    }

    print(f"🎯 Checking for event matches in query: '{query}'")
    
    # First, try to find a matching event by name
    matched_event = None
    
    # Direct event name matching - check both key and event_name
    for key, data in conclave_data.items():
        event_name = data.get('event_name', '').lower()
        print(f"   Checking event: '{key}' (name: '{event_name}')")
        
        # Check if the event key is in the query
        if key.lower() in query:
            matched_event = data
            print(f"🎯 Direct key match found: {key}")
            break
            
        # Check if the event name is in the query
        if event_name in query:
            matched_event = data
            print(f"🎯 Direct name match found: {event_name}")
            break
    
    # If no direct match, try context-based matching with word-by-word analysis
    if not matched_event:
        print(f"   No direct match, trying context-based matching...")
        
        # Split query into words and check each word against event names
        query_words = query.split()
        print(f"   Query words: {query_words}")
        
        for key, data in conclave_data.items():
            event_name = data.get('event_name', '').lower()
            event_words = event_name.split()
            key_words = key.split()
            
            print(f"   Checking event '{key}' with words: {event_words}")
            
            # Check if any significant words from event name or key are in the query
            for word in query_words:
                if len(word) > 2:  # Reduced minimum length for better matching
                    # Check against event name words
                    if word in event_words:
                        matched_event = data
                        print(f"🎯 Context match found: {event_name} (via word '{word}' in event name)")
                        break
                    # Check against event key words
                    if word in key_words:
                        matched_event = data
                        print(f"🎯 Context match found: {key} (via word '{word}' in event key)")
                        break
            if matched_event:
                break
    
    # If we found an event, determine what information is being requested
    if matched_event:
        print(f"✅ Event found: {matched_event['event_name']}")
        # Determine intent
        for section, triggers in keywords.items():
            if any(word in query for word in triggers):
                result = format_specific_section(matched_event, section)
                print(f"✅ Returning {section} for {matched_event['event_name']}")
                return result

        # Default: return full summary
        print(f"✅ Returning full summary for {matched_event['event_name']}")
        return format_full_summary(matched_event)
    
    # If no event found, try to provide general information
    print("❌ No specific event found, checking for general queries")
    
    # REMOVED: Generic responses that interfere with context system
    # Let the context system handle these queries instead
    
    return None  # No matching event or general information

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
    elif section == "participants":
        class_range = data.get('class_range', 'N/A')
        return f"👥 {data['event_name']} is open to students in {class_range}."
    elif section == "registration":
        # If registration info exists, use it; otherwise provide general guidance
        if 'registration_deadline' in data:
            return f"📝 Registration for {data['event_name']} closes on {data['registration_deadline']}."
        else:
            return f"📝 For registration details about {data['event_name']}, please contact the event coordinator or check the school notice board."
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
