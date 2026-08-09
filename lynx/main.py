from .audio import listen, speak
from .brain import brain
import random

slangs = ["You said : nothing", "why have you become a    silent monk", "dont play, please speak something", "ok, dont speak - stay silent whatever"]

def main():
    speak("Hello, I'm Lynx - Your Personal Voice Assistant!")
    while True:
        user_text = listen()
        if not user_text:
            user_text = slangs[random.randint(0, 4)]
        if "exit" in user_text.lower():
            speak("Goodbye!")
            break

        reply = brain(user_text)
        speak(reply)