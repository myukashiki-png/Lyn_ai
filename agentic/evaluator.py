def evaluate(step: str, result: str) -> bool:
    """
    Evaluasi sederhana:
    - sukses / gagal
    - aman / tidak
    """
    if "error" in result.lower():
        return False
    return True
