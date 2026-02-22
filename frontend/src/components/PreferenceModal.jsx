import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import FloatingBubble from './FloatingBubble';

const PreferenceModal = ({ isOpen, onClose, onSelect }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Frosted Glass Backdrop */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={onClose}
                className="absolute inset-0 bg-stone-900/30 backdrop-blur-md"
            ></motion.div>

            {/* Modal Content */}
            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="relative z-10 w-full max-w-sm"
            >
                <h2 className="text-center text-white font-serif text-2xl mb-8 text-shadow">
                    How would you like to cook?
                </h2>

                <div className="grid grid-cols-2 gap-8 justify-items-center">
                    <FloatingBubble
                        label="Hands-Free"
                        icon="🎙️"
                        color="bg-sage text-white"
                        onClick={() => onSelect('hands-free')}
                    />
                    <FloatingBubble
                        label="Manual"
                        icon="👆"
                        color="bg-white text-charcoal"
                        onClick={() => onSelect('manual')}
                    />
                    {/* Placeholder for future options */}
                    {/* 
                    <FloatingBubble label="Record" icon="🔴" onClick={() => {}} />
                    <FloatingBubble label="Send" icon="📤" onClick={() => {}} /> 
                    */}
                </div>
            </motion.div>
        </div>
    );
};

export default PreferenceModal;
