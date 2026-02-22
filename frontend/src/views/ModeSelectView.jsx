import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ModeSelectView = ({ onStart, onBack }) => {
    const [selectedMode, setSelectedMode] = useState('manual'); // manual, voice_record, hands_free
    const [selectedVoice, setSelectedVoice] = useState('female'); // female, male

    const modes = [
        { id: 'manual', label: 'Manual', icon: '👆', desc: 'Tap to proceed step by step' },
        { id: 'voice_record', label: 'Voice Record', icon: '🎙️', desc: 'Tap to record and speak commands' },
        { id: 'hands_free', label: 'Hands-Free', icon: '🎧', desc: 'App listens continuously' }
    ];

    const showVoiceOptions = selectedMode === 'voice_record' || selectedMode === 'hands_free';

    const handleStart = () => {
        onStart({
            mode: selectedMode,
            voice: selectedVoice
        });
    };

    return (
        <div className="min-h-screen bg-beige p-6 pt-12 flex flex-col relative">
            <button
                onClick={onBack}
                className="absolute top-8 left-6 w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center text-charcoal"
            >
                ←
            </button>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-16 text-center mb-10"
            >
                <h1 className="text-3xl font-serif text-charcoal mb-4">How are we cooking today?</h1>
                <p className="text-stone-500">Select your preferred interaction mode</p>
            </motion.div>

            <div className="space-y-4 mb-8">
                {modes.map((mode) => (
                    <motion.div
                        key={mode.id}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setSelectedMode(mode.id)}
                        className={`p-5 rounded-2xl border-2 transition-all cursor-pointer flex items-center gap-4 ${selectedMode === mode.id
                            ? 'border-terracotta bg-white shadow-md'
                            : 'border-transparent bg-white/50 opacity-70 hover:opacity-100'
                            }`}
                    >
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${selectedMode === mode.id ? 'bg-terracotta/10 rounded-full' : 'bg-stone-100'
                            }`}>
                            {mode.icon}
                        </div>
                        <div className="text-left">
                            <h3 className={`font-bold ${selectedMode === mode.id ? 'text-charcoal' : 'text-stone-600'}`}>
                                {mode.label}
                            </h3>
                            <p className="text-xs text-stone-400">{mode.desc}</p>
                        </div>
                        {selectedMode === mode.id && (
                            <div className="ml-auto w-6 h-6 rounded-full bg-terracotta text-white flex items-center justify-center text-xs border-2 border-white shadow-sm">
                                ✓
                            </div>
                        )}
                    </motion.div>
                ))}
            </div>

            {/* Voice Preferences - Only show if a voice mode is selected */}
            <AnimatePresence>
                {showVoiceOptions && (
                    <motion.div
                        initial={{ opacity: 0, height: 0, overflow: 'hidden' }}
                        animate={{ opacity: 1, height: 'auto', overflow: 'visible' }}
                        exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
                        className="mb-8"
                    >
                        <h4 className="text-sm font-bold text-stone-500 uppercase tracking-wider mb-4 text-center">
                            Assistant Profile
                        </h4>
                        <div className="flex justify-center gap-4">
                            <button
                                onClick={() => setSelectedVoice('female')}
                                className={`flex-1 py-4 rounded-xl border-2 transition-all font-medium flex flex-col items-center gap-2 ${selectedVoice === 'female'
                                    ? 'border-sage bg-sage/5 text-sage'
                                    : 'border-transparent bg-white text-stone-500'
                                    }`}
                            >
                                <span className="text-2xl">👩‍🍳</span>
                                Female Voice
                            </button>
                            <button
                                onClick={() => setSelectedVoice('male')}
                                className={`flex-1 py-4 rounded-xl border-2 transition-all font-medium flex flex-col items-center gap-2 ${selectedVoice === 'male'
                                    ? 'border-sage bg-sage/5 text-sage'
                                    : 'border-transparent bg-white text-stone-500'
                                    }`}
                            >
                                <span className="text-2xl">👨‍🍳</span>
                                Male Voice
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex-1"></div>

            <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={handleStart}
                className="w-full bg-charcoal text-white py-5 rounded-2xl font-bold text-lg shadow-[0_8px_30px_rgba(47,47,47,0.3)] hover:shadow-xl mt-auto transition-shadow text-black"
            >
                Let's Make Magic
            </motion.button>
        </div>
    );
};

export default ModeSelectView;
