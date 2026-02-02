def require_confirmation(risk_level: str) -> bool:
    if risk_level == "high":
        print("⚠️ Tindakan berisiko tinggi.")
        answer = input("Ketik 'YA' untuk melanjutkan: ")
        return answer.strip().upper() == "YA"

    if risk_level == "medium":
        print("⚠️ Tindakan berpotensi berisiko.")
        answer = input("Lanjutkan? (y/n): ")
        return answer.lower().startswith("y")

    return True
