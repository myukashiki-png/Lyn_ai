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
    add_fact)
from core_ai.risk_classifier import classify_risk
from core_ai.reflection import self_reflect
from core_ai.answer_refiner import refine_answer
from mode_manager import detect_mode, load_mode
from memory.memory_policy import should_store
from memory.vector_store import VectorStore

memory_store = VectorStore()

if should_store(command):
    memory_store.add(command)
from skills.skill_router import route_skill

skill = route_skill(command)

if skill:
    answer = skill(command)
else:
    answer = generate_llm_answer(command)
from safety.governor import SafetyGovernor
from safety.confirmations import require_confirmation

governor = SafetyGovernor()

risk = governor.check(command)

if not require_confirmation(risk):
    speak("Perintah dibatalkan.")
    return
def process_command(command: str) -> str:
    # intent → safety → skill → llm
    return handle_with_v24_pipeline(command)

# ================= CONFIG =================
ACCESS_KEY = "ISI_ACCESS_KEY_PICOVOICE"  # Ganti dengan access key Picovoice Anda
KEYWORD_PATH = "wakeword/hey-lyn.ppn"
MODEL_PATH = "wakeword/porcupine_params.pv"
OLLAMA_MODEL = "phi3"
VOSK_MODEL_PATH = "vosk_model"
answer = generate_answer(command)

risk = classify_risk(command)

if risk in ["medium", "high"]:
    reflection = self_reflect(answer, command)

    if "improve: ya" in reflection.lower():
        answer = refine_answer(answer, reflection)

speak(answer)
# ================= TTS =================
engine = pyttsx3.init()
engine.setProperty("rate", 155)

def speak(text):
    engine.say(text)
    engine.runAndWait()
def speak(text):
    engine.say(text)
    engine.runAndWait()
# ================= VOSK STT =================
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

# ================= OLLAMA =================
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

            # Dapatkan konteks short-term memory
            context = get_short_term()
            memory_prompt = ""
            for c in context:
                memory_prompt += f"User: {c['user']}\nAI: {c['ai']}\n"

            # Deteksi mode berdasarkan perintah
            mode_name = detect_mode(command)
            mode = load_mode(mode_name)

            # Jika mode memiliki system_prompt, gunakan itu; jika tidak, gunakan prompt default
            if mode and 'system_prompt' in mode:
                full_prompt = f"""
{mode['system_prompt']}

Konteks percakapan:
{memory_prompt}

Permintaan user:
{command}

Jawab sesuai peran kamu.
"""
            else:
                # Prompt default jika tidak ada mode
                full_prompt = f"""
Konteks sebelumnya:
{memory_prompt}

Perintah user sekarang:
{command}

Jawab dengan singkat, jelas, dan praktis.
"""

            # Jika ada fungsi run_agents dan synthesize, gunakan; jika tidak, langsung ke Ollama
            # Asumsi: Jika mode memiliki 'agents', jalankan agents; jika tidak, langsung ask_ollama
            if mode and 'agents' in mode:
                # Asumsi fungsi run_agents dan synthesize ada di mode_manager atau didefinisikan
                thoughts = run_agents(command, mode)
                response = synthesize(thoughts, command)
            else:
                response = ask_ollama(full_prompt)

            print("lyn:", response)
            speak(response)

            # Tambahkan ke short-term memory
            add_short_term(command, response)

except KeyboardInterrupt:
    print("Shutdown")

finally:
    stream.close()
    pa.terminate()
    porcupine.delete()
if os.path.exists("STOP"):
    shutdown()
