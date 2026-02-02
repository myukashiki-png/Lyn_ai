from skills import SKILL_REGISTRY

def execute_step(step: str) -> str:
    for skill in SKILL_REGISTRY:
        if skill.can_handle(step):
            return skill.run(step)

    return "Langkah tidak dikenali, dilewati."

from tools.tool_registry import TOOLS

def execute_step(step):
    tool_name, args = parse_step(step)
    tool = TOOLS.get(tool_name)

    if not tool:
        return "Tool tidak tersedia."

    return tool(**args)
