import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text: str):
    print("🗣️ lyn:", text)
    engine.say(text)
    engine.runAndWait()
