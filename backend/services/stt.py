import io
from fastapi import APIRouter, UploadFile, File, HTTPException
import speech_recognition as sr

router = APIRouter()

HAS_SR = True
try:
    import speech_recognition as sr
except ImportError:
    HAS_SR = False
    print("SpeechRecognition not found. STT will be disabled.")

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribes uploaded audio file to text using Google Web Speech API.
    Streamlit/Frontend should send a WAV/Blob.
    """
    if not HAS_SR:
        raise HTTPException(status_code=503, detail="Speech Recognition library not available.")
    
    recognizer = sr.Recognizer()
    
    try:
        # Read file contents
        content = await file.read()
        audio_file = io.BytesIO(content)
        
        with sr.AudioFile(audio_file) as source:
            # Record the audio data from the file
            audio = recognizer.record(source)
            
        # Recognize using Google Web Speech API
        text = recognizer.recognize_google(audio)
        return {"text": text}
        
    except sr.UnknownValueError:
        return {"text": "", "error": "Could not understand audio"}
    except sr.RequestError as e:
        print(f"STT API Error: {e}")
        raise HTTPException(status_code=502, detail=f"STT API Error: {e}")
    except Exception as e:
        print(f"STT Error: {e}")
        # Only return error details in debug mode or logs
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
