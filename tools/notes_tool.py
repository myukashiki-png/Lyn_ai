from datetime import datetime

NOTES_DIR = "memory/notes/"

def add_note(text):
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")
    with open(NOTES_DIR + filename, "w") as f:
        f.write(text)
    return "Catatan disimpan."

