import yaml
from pathlib import Path

AGENT_PATH = Path("agents")

def load_agent(name):
    with open(AGENT_PATH / f"{name}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def select_agents(mode):
    if mode == "coding":
        return ["software_architect", "fullstack_dev", "qa_tester"]

    if mode == "finance":
        return ["finance_expert", "logical_strategist", "qa_tester"]

    return ["prompt_engineer", "logical_strategist"]

