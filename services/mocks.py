from services.interfaces import AIService, STTService, TTSService
import time

class MockAIService(AIService):
    def generate_response(self, prompt: str, context_data: dict = None) -> str:
        # Simulate latency
        time.sleep(1)
        return f"This is a mock response to: '{prompt}'. Context Data Provided: {context_data is not None}"

class MockSTTService(STTService):
    def transcribe(self, audio_data: bytes) -> str:
        # Simulate processing time
        time.sleep(0.5)
        return "I want to cook Jollof Rice."

class MockTTSService(TTSService):
    def speak(self, text: str) -> bytes:
        # Return dummy bytes (mimicking an empty audio file or similar)
        # In a real app, this would be MP3/WAV data.
        return b"MOCKED_AUDIO_DATA"
