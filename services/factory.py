from services.interfaces import AIService, STTService, TTSService
from services.mocks import MockAIService, MockSTTService, MockTTSService
# Real services imported inside methods to avoid potential circular/init issues

class ServiceFactory:
    _stt_instance = None # Singleton for STT to avoid reloading model

    @staticmethod
    def get_ai_service(provider: str = "mock") -> AIService:
        if provider == "mock":
            return MockAIService()
        elif provider == "real":
            from services.real_services import RuleBasedAIService
            return RuleBasedAIService()
        raise ValueError(f"Unknown AI provider: {provider}")

    @staticmethod
    def get_stt_service(provider: str = "mock") -> STTService:
        if provider == "mock":
            return MockSTTService()
        elif provider == "real":
            # Lazy load STT as it takes time
            if ServiceFactory._stt_instance is None:
               from services.real_services import WhisperSTTService
               ServiceFactory._stt_instance = WhisperSTTService(model_size="base")
            return ServiceFactory._stt_instance
        raise ValueError(f"Unknown STT provider: {provider}")

    @staticmethod
    def get_tts_service(provider: str = "mock") -> TTSService:
        if provider == "mock":
            return MockTTSService()
        elif provider == "real":
            from services.real_services import GTTSService
            return GTTSService()
        raise ValueError(f"Unknown TTS provider: {provider}")
