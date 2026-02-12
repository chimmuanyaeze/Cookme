from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context_data: dict = None) -> str:
        """Generates a text response based on the prompt and optional context."""
        pass

class STTService(ABC):
    @abstractmethod
    def transcribe(self, audio_data: bytes) -> str:
        """Converts audio data (waves/bytes) to text."""
        pass

class TTSService(ABC):
    @abstractmethod
    def speak(self, text: str) -> bytes:
        """Converts text to audio data."""
        pass
