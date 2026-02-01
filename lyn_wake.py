import speech_recognition as sr
import pyttsx3
import requests
import time

# ===== TTS =====
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ===== STT =====
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen_short(timeout=3):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
            return recognizer.recognize_google(audio, language="id-ID").lower()
        except:
            return ""

def listen_command():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="id-ID")
        except:
            return ""

# ===== OLLAMA =====
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    return r.json()["response"]

# ===== MAIN LOOP =====
if __name__ == "__main__":
    print("lyn dalam sleep mode...")
    speak("lyn aktif. Ucapkan hey lyn.")

    while True:
        heard = listen_short()

        if "hey lyn" in heard:
            speak("Ya?")
            print("Wake word terdeteksi")

            command = listen_command()
            if not command:
                speak("Saya tidak mendengar perintah.")
                continue

            print("Perintah:", command)

            if "keluar" in command.lower():
                speak("Mode tidur.")
                time.sleep(1)
                continue

            response = ask_ollama(command)
            print("lyn:", response)
            speak(response)

        time.sleep(0.3)
