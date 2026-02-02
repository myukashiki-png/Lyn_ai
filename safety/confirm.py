def confirm(action):
    speak(f"Konfirmasi. {action}. Ya atau tidak?")
    answer = listen()
    return "ya" in answer.lower()

