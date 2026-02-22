import os
import sys
import uuid
import subprocess
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    gender: str = "female"

@router.post("/speak")
async def generate_speech(request: TTSRequest):
    """
    Generates speech audio from text using pyttsx3 in a subprocess.
    Returns the URL/path to the generated audio file.
    """
    try:
        # Generate a unique filename
        filename = f"speech_{uuid.uuid4().hex}.wav"
        output_path = os.path.join("assets", "audio", filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # We use a subprocess to run pyttsx3 to avoid COM/Threading issues in FastAPI
        # We will reuse the _legacy tts_worker.py logic but adapted here.
        # Actually, let's write a dedicated worker script for the backend to use.
        worker_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "tts_worker_script.py"))
        
        # Check if worker script exists, if not we need to create it (next step)
        
        cmd = [sys.executable, worker_script, "--text", request.text, "--gender", request.gender, "--output", output_path]
        
        # Run subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"TTS Worker Error: {stderr.decode()}")
            raise HTTPException(status_code=500, detail=f"TTS Generation failed: {stderr.decode()}")
            
        return {"audio_url": f"/assets/audio/{filename}", "filename": filename}

    except Exception as e:
        print(f"TTS Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
