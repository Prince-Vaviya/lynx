import asyncio 
import subprocess
import edge_tts
import sounddevice as sd
import numpy as np
import select
import sys
import assemblyai as aai
import os
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")
transcriber = aai.Transcriber()


SAMPLE_RATE=16000
VOICE = "en-GB-SoniaNeural"

def speak(text):
    async def _generate():
        tts = edge_tts.Communicate(text, VOICE)
        await tts.save("speech.mp3")
    asyncio.run(_generate())
    subprocess.run(["afplay", "speech.mp3"])

def listen():
    #Press "Enter" to listen, Press "Enter" to STOP listening
    frames = []
    input("")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
        print("Recording... press Enter to Stop")
        while True:
            data, _ = stream.read(4096)
            frames.append(data.copy())
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                print("Stopping recording")
                sys.stdin.readline()
                break

    audio = np.concatenate(frames)
    if(len(audio) == 0):
        return ""
    sf.write("recording.wav", audio, SAMPLE_RATE)
    subprocess.run(["ffmpeg", "-y", "-i", "recording.wav", "recording.mp3"], check=True)
    transcript = transcriber.transcribe("recording.mp3")
    text = transcript.text.strip()
    print(text)
    return text



if __name__ == "__main__":
    speak("Good Evening, Welcome Mr. Eagle : I am Your Personal Voice Assistant...")
    speak(listen())

