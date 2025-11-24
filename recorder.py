import sounddevice as sd
import soundfile as sf
import numpy as np

def record_chunk(seconds=3, sr=16000):
    print("Recording...")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1)
    sd.wait()
    audio = np.squeeze(audio)
    filename = "chunk.wav"
    sf.write(filename, audio, sr)
    return filename
