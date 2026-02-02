from ollama_client import ask_ollama

def reflect(answer):
    prompt = f"""
    Evaluasi jawaban berikut:
    {answer}

    Nilai:
    - Kejelasan
    - Risiko
    - Apakah perlu klarifikasi lanjutan

    Jawab singkat.
    """
    return ask_ollama(prompt)
