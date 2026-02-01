import json
from pathlib import Path

BASE_PATH = Path("memory")
STM_PATH = BASE_PATH / "short_term.json"
LTM_PATH = BASE_PATH / "long_term.json"

MAX_STM = 6

def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- SHORT TERM ----------
def add_short_term(user, ai):
    data = load_json(STM_PATH)
    convo = data.get("conversation", [])

    convo.append({
        "user": user,
        "ai": ai
    })

    data["conversation"] = convo[-MAX_STM:]
    save_json(STM_PATH, data)

def get_short_term():
    return load_json(STM_PATH).get("conversation", [])

def clear_short_term():
    save_json(STM_PATH, {"conversation": []})

# ---------- LONG TERM ----------
def add_fact(fact):
    data = load_json(LTM_PATH)
    facts = data.get("facts", [])
    if fact not in facts:
        facts.append(fact)
    data["facts"] = facts
    save_json(LTM_PATH, data)

def add_preference(pref):
    data = load_json(LTM_PATH)
    prefs = data["profile"].get("preferences", [])
    if pref not in prefs:
        prefs.append(pref)
    data["profile"]["preferences"] = prefs
    save_json(LTM_PATH, data)

def get_long_term():
    return load_json(LTM_PATH)
