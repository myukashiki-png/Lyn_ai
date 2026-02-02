def adjust_tone(text: str, context: str) -> str:
    if "error" in context.lower():
        return "Tenang. " + text
    if "bingung" in context.lower():
        return "Saya bantu pelan-pelan. " + text
    return text

def adjust_tone(text: str, context: str) -> str:
    if "error" in context.lower():
        return "Tenang. " + text
    if "bingung" in context.lower():
        return "Saya bantu pelan-pelan. " + text
    return text

