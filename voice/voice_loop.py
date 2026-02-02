from voice.wake_word import wait_for_wake_word
from voice.listener import listen_command
from voice.speaker import speak
from lyn_core import process_command
from voice.personality import adjust_tone

context = command
response = process_command(command)
response = adjust_tone(response, context)
speak(response)
def run_voice_assistant():
    while True:
        wait_for_wake_word()
        command = listen_command()

        if not command:
            speak("Saya tidak mendengar perintah.")
            continue

        response = process_command(command)
        speak(response)
if os.path.exists("STOP"):
    shutdown()
from voice.personality import adjust_tone

context = command
response = process_command(command)
response = adjust_tone(response, context)
speak(response)

