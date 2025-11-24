from fastapi import FastAPI, UploadFile, File
import whisper
import os

app = FastAPI(title="Voice-to-Text API")

# Load model once (tiny)
model = whisper.load_model("tiny")

@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        contents = await audio.read()
        filename = "temp.wav"
        with open(filename, "wb") as f:
            f.write(contents)

        # Transcribe
        result = model.transcribe(filename)
        text = result["text"]

        # cleanup
        try:
            os.remove(filename)
        except Exception:
            pass

        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
