from core_ai.ollama_client import ask_ollama

def self_reflect(answer: str, command: str) -> str:
    prompt = f"""
    Kamu adalah modul refleksi internal lyn.

    Tugas:
    - Jangan menjawab user
    - Jangan menambah fitur baru
    - Hanya menilai kualitas jawaban

    Pertanyaan user:
    {command}

    Jawaban saat ini:
    {answer}

    Nilai secara singkat:
    1. Apakah jelas?
    2. Apakah ada risiko?
    3. Apakah perlu klarifikasi?

    Balas dalam format:
    clarity: ok / kurang
    risk: rendah / sedang / tinggi
    improve: ya / tidak
    note: (1 kalimat)
    """

    return ask_ollama(prompt)
