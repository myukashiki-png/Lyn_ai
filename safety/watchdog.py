import time

def idle_guard(last_activity):
    if time.time() - last_activity > 1800:
        shutdown()


