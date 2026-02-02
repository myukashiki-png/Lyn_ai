import vosk
import pyaudio
import json

model = vosk.Model("models/vosk-id")

def listen_command():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000,
    )

    recognizer = vosk.KaldiRecognizer(model, 16000)
    print("🎤 Silakan bicara...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            stream.close()
            pa.terminate()
            return text
