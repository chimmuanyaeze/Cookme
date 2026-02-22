import { useState, useCallback } from 'react';

// Mock Voice Hook - In real implementation this would use Web Speech API or Backend Stream
export const useVoice = () => {
    const [isListening, setIsListening] = useState(false);
    const [lastTranscript, setLastTranscript] = useState("");
    const [isSpeaking, setIsSpeaking] = useState(false);

    const speak = useCallback((text) => {
        setIsSpeaking(true);
        // Cancel any ongoing speech before speaking
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = () => setIsSpeaking(false);
        window.speechSynthesis.speak(utterance);
    }, []);

    const stopSpeaking = useCallback(() => {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
    }, []);

    const sendCommand = async (command, context = {}) => {
        try {
            const res = await fetch('http://localhost:8000/api/chat/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: command, context })
            });
            const data = await res.json();

            // Auto-speak response if in hands-free mode (handled by caller logic usually, but here for demo)
            if (data.text) {
                // speak(data.text); // Optional: Auto-speak
            }
            return data;
        } catch (error) {
            console.error("Voice Command Error:", error);
            return { text: "Sorry, I couldn't reach the backend." };
        }
    };

    const toggleListening = () => {
        // TODO: Implement actual STT (Web Speech API)
        setIsListening(prev => !prev);
        if (!isListening) {
            console.log("Started simulated listening...");
            // Simulate a command after 3 seconds for testing
            setTimeout(() => {
                setLastTranscript("Next step");
                setIsListening(false);
            }, 3000);
        }
    };

    return {
        isListening,
        lastTranscript,
        isSpeaking,
        speak,
        stopSpeaking,
        sendCommand,
        toggleListening
    };
};
