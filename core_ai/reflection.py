from core_ai.ollama_client import ask_ollama

def reflect(task, result, evaluation, memory_store):
    if evaluation["verdict"] == "REJECT":
        memory_store.store(
            category="mistake",
            content=f"Task '{task}' gagal karena {evaluation['reason']}",
            confidence=0.9
        )

    if result.success:
        memory_store.store(
            category="preference",
            content=f"Pendekatan '{result.method}' berhasil",
            confidence=0.6
        )

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
