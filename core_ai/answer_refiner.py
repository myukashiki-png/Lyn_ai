from core_ai.ollama_client import ask_ollama

def refine_answer(answer: str, reflection: str) -> str:
    prompt = f"""
    Kamu adalah lyn.

    Berikut evaluasi internal:
    {reflection}

    Perbaiki jawaban berikut jika diperlukan:
    {answer}

    Aturan:
    - Tetap ringkas
    - Jangan menambah topik baru
    - Jangan menyebut evaluasi internal
    """

    return ask_ollama(prompt)
