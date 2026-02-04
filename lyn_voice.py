import os
import pvporcupine
import pyaudio
import struct
import pyttsx3
import requests
import time
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from memory.memory_manager import (
    add_short_term,
    get_short_term,
    add_fact
)
from core_ai.risk_classifier import classify_risk
from core_ai.reflection import self_reflect
from core_ai.answer_refiner import refine_answer
from mode_manager import detect_mode, load_mode
from memory.memory_policy import should_store
from memory.vector_store import VectorStore
from skills.skill_router import route_skill
from safety.governor import SafetyGovernor
from safety.confirmations import require_confirmation

# ================= CONFIG =================
ACCESS_KEY = "ISI_ACCESS_KEY_PICOVOICE"  # Ganti dengan access key Picovoice Anda
KEYWORD_PATH = "wakeword/hey-lyn.ppn"
MODEL_PATH = "wakeword/porcupine_params.pv"
OLLAMA_MODEL = "phi3"
VOSK_MODEL_PATH = "vosk_model"

# ================= INITIALIZATION =================
memory_store = VectorStore()
governor = SafetyGovernor()

# TTS
engine = pyttsx3.init()
engine.setProperty("rate", 155)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# VOSK STT
vosk_model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, 16000)

def listen_command():
    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1
    ) as stream:
        speak("Saya mendengarkan.")
        start_time = time.time()

        while time.time() - start_time < 8:
            data, _ = stream.read(4000)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")

    return ""

# OLLAMA
def ask_ollama(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    return r.json()["response"]

# Generate LLM answer (placeholder, assuming it's defined elsewhere or use ask_ollama)
def generate_llm_answer(command):
    return ask_ollama(command)

# Process command with pipeline (simplified)
def process_command(command: str) -> str:
    # Check memory policy
    if should_store(command):
        memory_store.add(command)
    
    # Route to skill
    skill = route_skill(command)
    if skill:
        answer = skill(command)
    else:
        answer = generate_llm_answer(command)
    
    # Risk classification and refinement
    risk = classify_risk(command)
    if risk in ["medium", "high"]:
        reflection = self_reflect(answer, command)
        if "improve: ya" in reflection.lower():
            answer = refine_answer(answer, reflection)
    
    return answer

# Shutdown function
def shutdown():
    print("Shutting down...")
    stream.close()
    pa.terminate()
    porcupine.delete()
    exit(0)

# ================= PORCUPINE =================
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
print("lyn siap. Menunggu wake word.")
speak("lyn aktif. Ucapkan hey lyn.")

# ================= MAIN LOOP =================
try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            speak("Ya?")
            command = listen_command()

            if not command:
                speak("Saya tidak menangkap perintah.")
                continue

            print("Perintah:", command)

            if "keluar" in command:
                speak("Kembali ke mode tidur.")
                time.sleep(1)
                continue

            # Safety check
            risk = governor.check(command)
            if not require_confirmation(risk):
                speak("Perintah dibatalkan.")
                continue

            # Process command
            response = process_command(command)

            print("lyn:", response)
            speak(response)

            # Add to short-term memory
            add_short_term(command, response)

        # Check for shutdown file
        if os.path.exists("STOP"):
            shutdown()

except KeyboardInterrupt:
    print("Shutdown")

finally:
    shutdown()


