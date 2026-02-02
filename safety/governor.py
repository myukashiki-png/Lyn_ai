import yaml
from pathlib import Path

RULES_PATH = Path("safety/rules.yaml")

class SafetyGovernor:
    def __init__(self):
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)

    def check(self, command: str) -> str:
        text = command.lower()

        for word in self.rules["high_risk"]:
            if word in text:
                return "high"

        for word in self.rules["medium_risk"]:
            if word in text:
                return "medium"

        return "low"
