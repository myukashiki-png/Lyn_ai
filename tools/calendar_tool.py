from datetime import datetime
import json

CAL_FILE = "memory/calendar.json"

def add_event(title, date):
    event = {
        "title": title,
        "date": date,
        "created": datetime.now().isoformat()
    }

    try:
        with open(CAL_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(event)

    with open(CAL_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return f"Acara '{title}' ditambahkan pada {date}."
