import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import chat

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite Default Port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure assets directory exists
os.makedirs("assets/audio", exist_ok=True)

# Mount static files for audio playback
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Include Routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(tts.router, prefix="/api/tts", tags=["tts"]) # TODO: Port TTS
# app.include_router(stt.router, prefix="/api/stt", tags=["stt"]) # TODO: Port STT

@app.get("/")
def read_root():
    return {"message": "AI Cooking Assistant Backend is running!"}
