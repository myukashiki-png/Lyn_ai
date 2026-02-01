import pvporcupine
import pyaudio
import struct
import pyttsx3
import requests

# ===== CONFIG =====
ACCESS_KEY = "ISI_ACCESS_KEY_KAMU_DI_SINI"
KEYWORD_PATH = "wakeword/hey-lyn.ppn"
MODEL_PATH = "wakeword/porcupine_params.pv"
OLLAMA_MODEL = "phi3"

# ===== TTS =====
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ===== OLLAMA =====
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    return r.json()["response"]

# ===== PORCUPINE INIT =====
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[KEYWORD_PATH],
    model_path=MODEL_PATH
)

pa = pyaudio.PyAudio()

stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("lyn aktif. Ucapkan 'Hey lyn'")
speak("lyn aktif. Ucapkan hey lyn.")

# ===== MAIN LOOP =====
try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word terdeteksi!")
            speak("Ya?")

            command = input("Perintah teks (sementara): ")
            if command.lower() == "keluar":
                speak("Kembali ke mode tidur.")
                continue

            response = ask_ollama(command)
            print("lyn:", response)
            speak(response)

except KeyboardInterrupt:
    print("Stop")

finally:
    stream.close()
    pa.terminate()
    porcupine.delete()
