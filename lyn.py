import speech_recognition as sr
import pyttsx3
import requests
import sys  # Added for sys.exit

engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Mendengarkan...")
            r.adjust_for_ambient_noise(source, duration=0.5)  # Added to reduce noise
            audio = r.listen(source, timeout=5, phrase_time_limit=10)  # Added timeouts
        return r.recognize_google(audio, language="id-ID")
    except sr.UnknownValueError:
        print("Tidak dapat mengenali suara.")
        return ""
    except sr.RequestError as e:
        print(f"Error dengan Google Speech Recognition: {e}")
        return ""
    except Exception as e:
        print(f"Error dalam mendengarkan: {e}")
        return ""

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()  # Raise error for bad status codes
        return r.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error dalam menghubungi Ollama: {e}")
        return "Maaf, saya tidak dapat memproses permintaan saat ini."
    except KeyError:
        print("Error: Respons dari Ollama tidak valid.")
        return "Maaf, terjadi kesalahan dalam respons."

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
