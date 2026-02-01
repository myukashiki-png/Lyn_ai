import yaml
from pathlib import Path

MODE_PATH = Path("modes")

def load_mode(mode_name):
    path = MODE_PATH / f"{mode_name}.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def detect_mode(text):
    t = text.lower()

    if any(k in t for k in ["python", "error", "kode", "function", "bug"]):
        return "coding"

    if any(k in t for k in ["uang", "budget", "pengeluaran", "tabungan", "investasi"]):
        return "finance"

    return "general"
