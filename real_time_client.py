import sounddevice as sd
import wavio
import requests
import os

SERVER_URL = "http://127.0.0.1:8000/transcribe/"

def record_and_send(duration=5, fs=16000):
    try:
        print("Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        filename = "temp.wav"
        wavio.write(filename, audio, fs, sampwidth=2)

        if not os.path.exists(filename):
            print("Error: temp.wav not found!")
            return

        with open(filename, "rb") as f:
            response = requests.post(SERVER_URL, files={"audio": f}, timeout=60)
            print("Server response:", response.json())

        os.remove(filename)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    record_and_send()

