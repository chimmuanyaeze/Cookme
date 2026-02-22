import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import StepCard from '../components/StepCard';
import { useVoice } from '../hooks/useVoice';

const CookingView = ({ recipe, mode, voiceGender, missingIngredients = [], onExit, onFinish }) => {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    const originalSteps = recipe?.steps || [];

    // Mock logic to adapt recipe steps based on missing optional ingredients
    const steps = originalSteps.map(step => {
        if (!step.instruction || missingIngredients.length === 0) return step;

        const lowerInstruction = step.instruction.toLowerCase();
        const missingMentioned = missingIngredients.filter(ing => {
            const name = (ing.ingredient_id || ing.name || '').toLowerCase();
            return name && name.length > 2 && lowerInstruction.includes(name); // Basic matching
        });

        if (missingMentioned.length > 0) {
            const names = missingMentioned.map(i => i.ingredient_id || i.name).join(', ');
            return {
                ...step,
                instruction: `(Adapted without ${names}): ${step.instruction}`
            };
        }
        return step;
    });

    const { isListening, lastTranscript, toggleListening, speak, stopSpeaking } = useVoice();

    // Auto-announce step when changes (if in voice modes)
    useEffect(() => {
        if ((mode === 'hands_free' || mode === 'voice_record') && steps[currentStepIndex]) {
            // Note: In a real app, you'd pass voiceGender to the TTS engine here
            console.log(`TTS using ${voiceGender} voice`);

            const stepNum = steps[currentStepIndex].step_number || currentStepIndex + 1;
            const instruction = steps[currentStepIndex].instruction;

            // Speak the step twice and prompt for completion
            const prompt = `Step ${stepNum}. ${instruction} I'll repeat that. Step ${stepNum}. ${instruction} Tell me when you are done so we can move to the next step.`;

            speak(prompt);
        }
    }, [currentStepIndex, mode, voiceGender, steps, speak]);

    // Handle Voice Commands
    useEffect(() => {
        if (!lastTranscript) return;

        const command = lastTranscript.toLowerCase();
        if (command.includes('next')) {
            handleNext();
        } else if (command.includes('back') || command.includes('previous')) {
            handleBack();
        } else if (command.includes('repeat')) {
            speak(steps[currentStepIndex]?.instruction || "");
        }
    }, [lastTranscript]);

    const handleNext = () => {
        stopSpeaking();
        if (currentStepIndex < steps.length - 1) {
            setCurrentStepIndex(prev => prev + 1);
        } else {
            onFinish();
        }
    };

    const handleBack = () => {
        stopSpeaking();
        if (currentStepIndex > 0) {
            setCurrentStepIndex(prev => prev - 1);
        } else {
            onExit();
        }
    };

    const handleExit = () => {
        stopSpeaking();
        onExit();
    };

    if (steps.length === 0) {
        return <div className="p-8 text-center text-stone-500">No steps available.</div>;
    }

    return (
        <div className="fixed inset-0 bg-beige z-50 flex flex-col">
            {/* Header */}
            <div className="p-6 flex justify-between items-center z-10">
                <button onClick={handleExit} className="text-stone-400 font-medium text-sm px-4 py-2 bg-white/50 rounded-full shadow-sm active:scale-95 transition-transform">
                    Quit
                </button>
                <div className="flex gap-1 flex-1 mx-6 justify-end">
                    {steps.map((_, i) => (
                        <div
                            key={i}
                            className={`h-1 flex-1 max-w-[20px] rounded-full transition-colors ${i <= currentStepIndex ? 'bg-sage' : 'bg-stone-200'}`}
                        />
                    ))}
                </div>
            </div>

            {/* Antigravity Step Cards */}
            <div className="flex-1 relative overflow-hidden">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStepIndex}
                        className="absolute inset-0"
                        initial={{ opacity: 0, y: 50, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -50, scale: 0.95 }}
                        transition={{ type: "spring", stiffness: 200, damping: 25 }}
                    >
                        <StepCard
                            step={steps[currentStepIndex]}
                            onComplete={handleNext}
                            onBack={handleBack}
                            isLast={currentStepIndex === steps.length - 1}
                        />
                    </motion.div>
                </AnimatePresence>
            </div>

            {/* Voice Status / Mic Button (Only for voice modes) */}
            {(mode === 'hands_free' || mode === 'voice_record') && (
                <div className="p-6 flex justify-center items-center gap-4 relative z-10 bg-gradient-to-t from-beige via-beige to-transparent pt-12">
                    <motion.button
                        whileTap={{ scale: 0.9 }}
                        onClick={toggleListening}
                        className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg border-2 border-white/50 ${isListening ? 'bg-terracotta animate-pulse' : 'bg-sage'}`}
                    >
                        <span className="text-2xl">{isListening ? '🛑' : '🎙️'}</span>
                    </motion.button>
                    {isListening && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="absolute right-6 top-1/2 -translate-y-1/2 bg-white px-4 py-2 rounded-xl shadow-sm border border-stone-100 text-sm text-stone-500 font-medium"
                        >
                            Listening...
                        </motion.div>
                    )}
                </div>
            )}

            {/* Manual Mode Footer Padding */}
            {mode === 'manual' && <div className="h-6"></div>}
        </div>
    );
};

export default CookingView;
