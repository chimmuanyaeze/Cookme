from services.factory import ServiceFactory
import time

def test_services():
    print("Testing Service Factory and Mocks...")
    
    # 1. Test AI Service
    ai = ServiceFactory.get_ai_service("mock")
    response = ai.generate_response("Hello", context="Test")
    print(f"AI Response: {response}")
    assert "mock response" in response
    
    # 2. Test STT Service
    stt = ServiceFactory.get_stt_service("mock")
    text = stt.transcribe(b"audio")
    print(f"STT Transcription: {text}")
    assert text == "I want to cook Jollof Rice."
    
    # 3. Test TTS Service
    tts = ServiceFactory.get_tts_service("mock")
    audio = tts.speak("Hello world")
    print(f"TTS Audio Data Length: {len(audio)}")
    assert audio == b"MOCKED_AUDIO_DATA"
    
    print("All service tests passed!")

if __name__ == "__main__":
    test_services()
