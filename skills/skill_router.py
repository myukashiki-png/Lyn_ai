import importlib
from skills.registry import SKILLS

def route_skill(text: str):
    text_lower = text.lower()

    for name, meta in SKILLS.items():
        for kw in meta["keywords"]:
            if kw in text_lower:
                module_path, func_name = meta["handler"].rsplit(".", 1)
                module = importlib.import_module(module_path)
                return getattr(module, func_name)

    return None
