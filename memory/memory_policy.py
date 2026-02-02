IMPORTANT_KEYWORDS = [
    "preferensi", "ingat", "jadwal", "proyek",
    "keuangan", "tujuan", "kerja", "kebiasaan"
]

def should_store(text: str) -> bool:
    if len(text) < 40:
        return False

    for k in IMPORTANT_KEYWORDS:
        if k in text.lower():
            return True

    return False
FORBIDDEN_MEMORY = [
    "password",
    "pin",
    "rekening",
    "otp"
]

def can_store(text):
    return not any(word in text.lower() for word in FORBIDDEN_MEMORY)
