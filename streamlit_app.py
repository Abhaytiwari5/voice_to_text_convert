import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import whisper
import numpy as np
import time
import io

# Load Whisper model once
model = whisper.load_model("base")

st.set_page_config(page_title="Speech to Text", layout="centered")

st.title("🎤 Speech to Text Conversion")
st.write("Convert your voice or audio file into text using Whisper.")



#  AUDIO RECORDING FUNCTION

def record_audio(duration=5, fs=44100):
    st.info("Recording started... Speak now.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    st.success("Recording finished!")
    
    # Save to temporary WAV file
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_wav.name, fs, recording)
    return temp_wav.name

#  TRANSCRIBE FUNCTION

def transcribe_audio(file_path):
    result = model.transcribe(file_path, word_timestamps=True)
    return result



#  RECORD SECTION (MIC)

st.subheader("🎙️ Record using Microphone")

duration = st.slider("Select Recording Duration (seconds)", 3, 20, 5)

if st.button("Start Recording"):
    wav_path = record_audio(duration)
    with st.spinner("Transcribing..."):
        result = transcribe_audio(wav_path)

    st.subheader("📄 Transcript")
    st.info(result["text"])


    # Show timestamps
    st.subheader("⏱️ Timestamps")
    for s in result["segments"]:
        t = time.strftime('%H:%M:%S', time.gmtime(s['start']))
        st.write(f"[{t}] {s['text']}")

    # Download Button
    txt_data = io.StringIO(result["text"])
    st.download_button("Download Transcript", txt_data.getvalue(), "transcript.txt")



#  FILE UPLOAD SECTION

st.subheader("📁 Upload Audio File")

audio_file = st.file_uploader("Upload WAV/MP3 file", type=["wav", "mp3", "m4a"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_file.read())
        temp_path = f.name

    with st.spinner("Transcribing uploaded file..."):
        result = transcribe_audio(temp_path)

    st.subheader("📄 Transcript")
    st.write(result["text"])

    st.subheader("⏱️ Timestamps")
    for s in result["segments"]:
        t = time.strftime('%H:%M:%S', time.gmtime(s['start']))
        st.write(f"[{t}] {s['text']}")

    txt_data = io.StringIO(result["text"])
    st.download_button("Download Transcript", txt_data.getvalue(), "transcript.txt")


