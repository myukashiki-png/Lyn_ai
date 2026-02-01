import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengarkan...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="id-ID")
    except:
        return ""

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    return r.json()["response"]

if __name__ == "__main__":
    speak("lyn siap membantu.")
    while True:
        text = listen()
        if not text:
            continue

        print("Kamu:", text)

        if "keluar" in text.lower():
            speak("Sampai jumpa.")
            break

        reply = ask_ollama(text)
        print("lyn:", reply)
        speak(reply)
# test Mon Feb  2 02:38:05 WIB 2026
