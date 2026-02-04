def create_plan(goal, memory=None):
    prompt = f"Goal: {goal}"

    if memory and memory.failures:
        prompt += "\nPrevious failures:\n"
        for f in memory.failures:
            prompt += f"- Step {f['step']}: {f['reason']}\n"

    return generate_plan(prompt)
def plan_task(goal: str) -> list[str]:
    """
    Gunakan LLM hanya untuk MEMECAH tugas,
    bukan untuk menjalankan.
    """
    prompt = f"""
    Kamu adalah perencana tugas.
    Pecah tujuan berikut menjadi langkah kecil, aman, dan berurutan.
    Jangan sertakan perintah berbahaya.

    Tujuan: {goal}

    Jawab dalam bentuk daftar bernomor.
    """

    steps = call_llm(prompt)
    return parse_steps(steps)
