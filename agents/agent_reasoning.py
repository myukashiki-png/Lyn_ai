from agent_router import load_agent, select_agents
from ollama_client import ask_ollama

def run_agents(command, mode):
    agents = select_agents(mode)
    thoughts = []

    for name in agents:
        agent = load_agent(name)

        prompt = f"""
        Kamu berperan sebagai {agent['name']}.
        Tugas kamu:
        {agent['instruction']}

        Masalah user:
        {command}

        Berikan analisis singkat.
        """

        result = ask_ollama(prompt)
        thoughts.append(f"{agent['name']}: {result}")

    return thoughts
