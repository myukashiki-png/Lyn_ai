def classify_risk(text: str) -> str:
    high_risk_keywords = [
        "hapus", "delete", "bayar", "transfer",
        "uang", "password", "otomatis"
    ]

    for word in high_risk_keywords:
        if word in text.lower():
            return "high"

    if len(text) > 200:
        return "medium"

    return "low"

